# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Records-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""PIDManager."""

from invenio_pidrelations.contrib.versioning import PIDNodeVersioning
from invenio_pidstore.models import PersistentIdentifier, PIDStatus
from invenio_pidstore.resolver import Resolver
from invenio_records.api import Record

from .minter import versioned_recid_minter_v2


class PIDManagerConfig:
    """PID manager config."""

    record_cls = Record  # FIXME: This is duplicated with RecordServiceConfig
    resolver_cls = Resolver
    resolver_obj_type = "rec"
    resolver_pid_type = "recid"  # PID type for resolver and fetch
    minter_pid_type = "recid_v2"  # FIXME: Unused
    draft_cls = None  # FIXME: This is duplicated with the user set one


class PIDManager:
    """PID manager."""

    default_config = PIDManagerConfig

    def __init__(self, config=None):
        """Constructor."""
        self.config = config or self.default_config

    @property
    def resolver(self):
        """Factory for creating a draft resolver instance."""
        return self.config.resolver_cls(
            pid_type=self.config.resolver_pid_type,
            getter=self.config.record_cls.get_record,
            registered_only=False
        )

    @property
    def draft_resolver(self):
        """Factory for creating a draft resolver instance."""
        return self.config.resolver_cls(
            pid_type=self.config.resolver_pid_type,
            getter=self.config.draft_cls.get_record,
            registered_only=False
        )

    @property
    def minter(self):
        """Returns the minter function."""
        return versioned_recid_minter_v2

    @classmethod
    def is_published(cls, pid):
        """Confirms if a pid is registered."""
        return pid.status == PIDStatus.REGISTERED

    def fetch_pid_db(self, pid_value):
        """Fetch a PID from DB."""
        return PersistentIdentifier.get(
            pid_type=self.config.resolver_pid_type,
            pid_value=pid_value
        )

    def is_first_version(self, pid=None, pid_value=None):
        """Returns if the pid is the firts version of the record.

        If the pid is None, it assumes a pid_value.
        """
        if not pid:
            pid = self.fetch_pid_db(pid_value)

        pv = PIDNodeVersioning(pid=pid)
        return pv.children.count() == 0

    def register_pid(self, pid_value):
        """Register the conceptrecid."""
        pid = self.fetch_pid_db(pid_value)
        pid.register()

        return pid

    def resolve(self, id_, draft=False):
        """Resolve a persistent identifier to a record or a draft."""
        _resolver = self.draft_resolver if draft else self.resolver

        return _resolver.resolve(id_)

    def mint(self, record_uuid, data):
        """Mint a record."""
        return self.minter(record_uuid=record_uuid, data=data)
