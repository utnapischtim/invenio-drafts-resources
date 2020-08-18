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
    """Return (<index alias>, <doc_type>) for records and drafts based objects.

    NOTE: document type is required for ES 6 suppport and will be removed when
          unsupported.
    TODO: Use $schema to fill index per issue #27
    """
    if isinstance(record, DraftBase):
        return 'drafts', "_doc"
    if isinstance(record, RecordBase):
        return 'records', "_doc"
    else:
        return None, None
