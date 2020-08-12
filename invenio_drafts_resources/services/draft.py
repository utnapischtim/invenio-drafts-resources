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
from invenio_records_resources.services import MarshmallowDataValidator, \
    RecordService, RecordServiceConfig

from .permissions import DraftPermissionPolicy
from .pid_manager import PIDManager
from .schemas import DraftMetadataSchemaJSONV1
from .search import draft_record_to_index


class RecordDraftServiceConfig(RecordServiceConfig):
    """Draft Service configuration."""

    # Service configuration
    permission_policy_cls = DraftPermissionPolicy
    pid_manager = PIDManager()

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

    @property
    def pid_manager(self):
        """Factory for the pid manager."""
        return self.config.pid_manager

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

    # High-level API
    # Inherits record read, search, create, delete and update

    def read_draft(self, id_, identity):
        """Retrieve a record."""
        pid, draft = self.pid_manager.resolve(id_, draft=True)
        self.require_permission(identity, "read", record=draft)
        # Todo: how do we deal with tombstone pages
        return self.resource_unit(pid=pid, record=draft, links=None)

    def update_draft(self, id_, data, identity):
        """Replace a record."""
        # TODO: etag and versioning
        pid, draft = self.pid_manager.resolve(id_, draft=True)
        # Permissions
        self.require_permission(identity, "update", record=draft)
        validated_data = self.draft_data_validator.validate(data)
        # FIXME: extract somewhere else
        self._patch_data(draft, validated_data)
        draft.update(draft.dumps())
        draft.commit()

        if self.indexer:
            self.indexer.index(draft)

        return self.resource_unit(pid=pid, record=draft, links=None)

    def create(self, data, identity):
        """Create a draft for a new record.

        It does not eagerly create the associated record.
        """
        self.require_permission(identity, "create")
        validated_data = self.draft_data_validator.validate(data)
        rec_uuid = uuid.uuid4()
        pid = self.pid_manager.mint(record_uuid=rec_uuid, data=validated_data)
        draft = self.draft_cls.create(validated_data, id_=rec_uuid)

        db.session.commit()  # Persist DB
        if self.indexer:
            self.indexer.index(draft)

        return self.resource_unit(pid=pid, record=draft, links=None)

    def _patch_data(self, record, data):
        """Temporarily here until the merge strategy is set."""
        # TODO: Implement better update/merge strategy
        for key in data.keys():
            record[key] = data[key]

    def edit(self, id_, data, identity):
        """Create a new revision or a draft for an existing record.

        :param id_: record PID value.
        """
        pid, record = self.pid_manager.resolve(id_)
        self.require_permission(identity, "create")
        validated_data = self.draft_data_validator.validate(data)
        self._patch_data(record, validated_data)
        draft = self.draft_cls.create(record.dumps(), id_=record.id,
                                      fork_version_id=record.revision_id)
        db.session.commit()  # Persist DB
        if self.indexer:
            self.indexer.index(draft)

        return self.resource_unit(pid=pid, record=draft, links=None)

    def _publish_revision(self, validated_data, pid):
        """Publish draft of existing record (edition)."""
        pid, record = self.pid_manager.resolve(pid.pid_value)
        record.clear()
        record.update(validated_data)
        record.commit()

        return record

    def _publish_new_version(self, validated_data, draft):
        """Publish draft of a new record."""
        record = self.record_cls.create(validated_data, id_=draft.id)
        conceptrecid = record['conceptrecid']

        # FIXME: This implies two db queries for the same in pid_manager
        if self.pid_manager.is_first_version(
            pid_value=conceptrecid
        ):
            self.pid_manager.register_pid(record['conceptrecid'])

        self.pid_manager.register_pid(record['recid'])

        return record

    def publish(self, id_, identity):
        """Publish a draft."""
        self.require_permission(identity, "publish")
        # Get draft
        pid, draft = self.pid_manager.resolve(id_, draft=True)
        # Validate against record schema
        validated_data = self.data_validator.validate(draft.dumps())
        # Publish it
        if self.pid_manager.is_published(pid):  # Then we publish a revision
            record = self._publish_revision(validated_data, pid)
        else:
            record = self._publish_new_version(validated_data, draft)
        # Remove draft
        draft.delete(force=True)
        db.session.commit()  # Persist DB
        # Index the record
        if self.indexer:
            self.indexer.delete(draft)
            self.indexer.index(record)

        return self.resource_unit(pid=pid, record=record, links=None)

    def new_version(self, id_, identity):
        """Create a new version of a record."""
        self.require_permission(identity, "create")
        # Get record
        pid, record = self.pid_manager.resolve(id_)
        # Validate and create a draft, register PID
        data = record.dumps()
        # Validate against record schema
        validated_data = self.draft_data_validator.validate(data)
        # Create new record (relation done by minter)
        rec_uuid = uuid.uuid4()
        pid = self.pid_manager.mint(
            record_uuid=rec_uuid,
            data=validated_data
        )
        draft = self.draft_cls.create(
            data=validated_data,
            id_=rec_uuid
        )
        db.session.commit()  # Persist DB
        # Index the record
        if self.indexer:
            self.indexer.index(draft)

        return self.resource_unit(pid=pid, record=draft, links=None)
