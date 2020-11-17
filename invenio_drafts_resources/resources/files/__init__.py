# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio Resources module to create REST APIs."""

from .config import DraftFileResourceConfig, DraftFileActionResourceConfig, \
    RecordFileResourceConfig, RecordFileActionResourceConfig
from .resource import DraftFileResource, DraftFileActionResource, \
    RecordFileResource, RecordFileActionResource

__all__ = (
    "DraftFileResourceConfig",
    "DraftFileResource",
    "DraftFileActionResourceConfig",
    "DraftFileActionResource",
    "RecordFileResourceConfig",
    "RecordFileActionResourceConfig",
    "RecordFileResource",
    "RecordFileActionResource",
)
