# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.


"""Search/Indexer module."""

from invenio_records.api import RecordBase

from ..drafts import DraftBase


def draft_record_to_index(record):
    """Return the index alias for records and drafts based objects.

    Note: document type is deprecated and therefore returned as None
    """
    if isinstance(record, DraftBase):
        return 'drafts', None
    if isinstance(record, RecordBase):
        return 'records', None
    else:
        return None, None
