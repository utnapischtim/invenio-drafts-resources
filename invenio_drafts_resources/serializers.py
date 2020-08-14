# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio Resources module to create REST APIs."""

import json

import pytz
from flask_resources.serializers import SerializerMixin
from invenio_records_resources.serializers import RecordJSONSerializer

from .services.schemas import RecordDraftSchemaJSONV1


class RecordDraftJSONSerializer(RecordJSONSerializer):
    """Drafts JSON serializer implementation."""

    def __init__(self, schema=None):
        """Constructor."""
        self.schema = RecordDraftSchemaJSONV1

    def _process_record(self, record_unit, *args, **kwargs):
        record_draft_dict = \
            super(RecordDraftJSONSerializer, self)._process_record(
                record_unit, *args, **kwargs
            )

        if hasattr(record_unit.record, 'expires_at'):
            expires_at = record_unit.record.expires_at
            record_draft_dict["expires_at"] = (
                pytz.utc.localize(expires_at).isoformat()
                if expires_at and not expires_at.tzinfo
                else None
            )

        return record_draft_dict
