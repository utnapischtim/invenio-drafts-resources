# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.


"""Draft Service."""

import uuid

from invenio_db import db
from invenio_pidrelations.contrib.versioning import PIDNodeVersioning
from invenio_pidstore.models import PersistentIdentifier
from invenio_records_resources.services import MarshmallowDataValidator, \
    RecordService, RecordServiceConfig

from ..resource_units import IdentifiedRecordDraft
from .minter import versioned_recid_minter_v2
from .permissions import DraftPermissionPolicy
from .schemas import DraftMetadataSchemaJSONV1
from .search import draft_record_to_index


class RecordDraftServiceConfig(RecordServiceConfig):
    """Draft Service configuration."""

    # Service configuration
    permission_policy_cls = DraftPermissionPolicy

    # RecordService configuration
    resource_unit_cls = IdentifiedRecordDraft

    # DraftService configuration.
    record_to_index = draft_record_to_index
    # WHY: We want to force user input choice here.
    draft_cls = None
    draft_data_validator = MarshmallowDataValidator(
        schema=DraftMetadataSchemaJSONV1
    )


class RecordDraftService(RecordService):
    """Draft Service interface.

    This service includes verioning.
    """

    default_config = RecordDraftServiceConfig

    # Overwrite resolver because default status is a class attr
    @property
    def resolver(self):
        """Factory for creating a draft resolver instance."""
        return self.config.resolver_cls(
            pid_type=self.config.resolver_pid_type,
            getter=self.record_cls.get_record,
            registered_only=False
        )

    # Overwrite minter to use versioning
    @property
    def minter(self):
        """Returns the minter function."""
        return versioned_recid_minter_v2

    @property
    def indexer(self):
        """Factory for creating an indexer instance."""
        return self.config.indexer_cls(
            record_to_index=self.config.record_to_index
        )

    # Draft attrs
    @property
    def draft_cls(self):
        """Factory for creating a record class."""
        return self.config.draft_cls

    @property
    def draft_data_validator(self):
        """Returns an instance of the draft data validator."""
        return self.config.draft_data_validator

    @property
    def draft_resolver(self):
        """Factory for creating a draft resolver instance."""
        return self.config.resolver_cls(
            pid_type=self.config.resolver_pid_type,
            getter=self.draft_cls.get_record,
            registered_only=False
        )

    def resolve_draft(self, id_):
        """Resolve a persistent identifier to a record draft."""
        return self.draft_resolver.resolve(id_)

    # FIXME: This should be moved to the PID wrapper when it is done.
    def _fetch_pid_db(self, pid_value):
        """Fetch a PID from DB."""
        return PersistentIdentifier.get(
            pid_type=self.config.resolver_pid_type,
            pid_value=pid_value
        )

    # FIXME: This should be moved to the PID wrapper when it is done.
    def _register_pid(self, pid_value):
        """Register the conceptrecid."""
        pid = self._fetch_pid_db(pid_value)
        pid.register()

    # High-level API
    # Inherits record read, search, create, delete and update

    def read_draft(self, id_, identity):
        """Retrieve a record."""
        pid, record = self.resolve_draft(id_)
        self.require_permission(identity, "read", record=record)
        # Todo: how do we deal with tombstone pages
        return self.resource_unit(pid=pid, record=record)

    def update_draft(self, id_, data, identity):
        """Replace a record."""
        # TODO: etag and versioning
        pid, draft = self.resolve_draft(id_)
        # Permissions
        self.require_permission(identity, "update", record=draft)
        # TODO: Data validation

        validated_data = self.draft_data_validator.validate(data)
        # FIXME: extract somewhere else
        self._patch_data(draft, validated_data)
        draft.update(draft.dumps())
        draft.commit()

        if self.indexer:
            self.indexer.index(draft)

        return self.resource_unit(pid=pid, record=draft)

    def create(self, data, identity):
        """Create a draft for a new record.

        It does not eagerly create the associated record.
        """
        self.require_permission(identity, "create")
        validated_data = self.draft_data_validator.validate(data)
        rec_uuid = uuid.uuid4()
        pid = self.minter(record_uuid=rec_uuid, data=validated_data)
        draft = self.draft_cls.create(validated_data, id_=rec_uuid)

        db.session.commit()  # Persist DB
        if self.indexer:
            self.indexer.index(draft)

        return self.config.resource_unit_cls(pid=pid, record=draft)

    def _patch_data(self, record, data):
        """Temporarily here until the merge strategy is set."""
        for key in data.keys():
            record[key] = data[key]

    def edit(self, id_, data, identity):
        """Create a new revision or a draft for an existing record.

        :param id_: record PID value.
        """
        # FIXME: for now it assumes always new revision (no files changes)
        pid, record = self.resolve(id_)
        self.require_permission(identity, "create")
        validated_data = self.draft_data_validator.validate(data)
        # FIXME: extract somewhere else
        self._patch_data(record, validated_data)
        draft = self.draft_cls.create(record.dumps(), id_=record.id,
                                      fork_version_id=record.revision_id)
        db.session.commit()  # Persist DB
        if self.indexer:
            self.indexer.index(draft)

        return self.config.resource_unit_cls(pid=pid, record=draft)

    def _publish_new_record(self, validated_data, draft):
        """Publish draft of a new record."""
        # Use same UUID
        record = self.record_cls.create(validated_data, id_=draft.id)
        self._register_pid(record['conceptrecid'])
        self._register_pid(record['recid'])

        return record

    def _publish_edited(self, validated_data, pid):
        """Publish draft of existing record (new version or revision).

        NOTE: For now it only contemplates revision since files cannot
        be edited (not supported).
        """
        pid, record = self.resolve(pid.pid_value)
        record.clear()
        record.update(validated_data)
        record.commit()

        return record

    def _publish_new_version(self, validated_data, draft):
        """Publish draft of a new record."""
        # FIXME: This should be refactored, too much similarities with
        # `_publish_new_record`.
        # Use same UUID
        record = self.record_cls.create(validated_data, id_=draft.id)
        self._register_pid(record['recid'])

        return record

    def _is_new_version(self, data, draft):
        """Checks if the publishing should be a new version or revision."""
        # NOTE: Until files is implemented we use a metadata field "_files"
        return data.get("_files", False)

    def publish(self, id_, identity):
        """Publish a draft."""
        self.require_permission(identity, "publish")
        # Get draft
        pid, draft = self.resolve_draft(id_=id_)
        # Validate and create record, register PID
        data = draft.dumps()
        # Validate against record schema
        validated_data = self.data_validator.validate(data)
        # Publish it
        conceptrecid = self._fetch_pid_db(validated_data["conceptrecid"])
        pv = PIDNodeVersioning(pid=conceptrecid)
        # children return only registered pids
        is_new_record = pv.children.count() > 0
        if not is_new_record:
            record = self._publish_new_record(validated_data, draft)
        else:
            if self._is_new_version(validated_data, draft):
                record = self._publish_new_version(validated_data, draft)
            else:
                record = self._publish_edited(validated_data, pid)

        # Remove draft
        draft.delete(force=True)
        db.session.commit()  # Persist DB
        # Index the record
        if self.indexer:
            self.indexer.delete(draft)
            self.indexer.index(record)

        return self.resource_unit(pid=pid, record=record)

    def version(self, id_, identity):
        """Create a new version of a record."""
        self.require_permission(identity, "create")
        # Get draft
        pid, record = self.resolve(id_=id_)
        # Validate and create a draft, register PID
        data = record.dumps()
        # Validate against record schema
        validated_data = self.draft_data_validator.validate(data)
        # Create new record (relation done by minter)
        rec_uuid = uuid.uuid4()
        pid = self.minter(record_uuid=rec_uuid, data=validated_data)
        draft = self.draft_cls.create(
            data=validated_data,
            id_=rec_uuid
        )
        db.session.commit()  # Persist DB
        # Index the record
        if self.indexer:
            self.indexer.index(draft)

        return self.resource_unit(pid=pid, record=draft)
