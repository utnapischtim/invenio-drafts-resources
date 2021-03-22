# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-Records-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio Record File Resources."""

# from flask import abort, g
from flask_resources import CollectionResource
from invenio_records_resources.resources import FileActionResource, \
    FileResource
from invenio_records_resources.resources.actions import ActionResource


class RecordFileResource(CollectionResource):
    """Record file resource.

    It does not inherit from Invenio-Records-Resources::FileResource to
    disable the queries to any other endpoint (e.g. create), which otherwise
    would need to be overwritten. Here they are merely not implemented.
    """

    def __init__(self, config=None, service=None):
        """Constructor."""
        super().__init__(config=config)
        self.service = service

    # ListView GET
    def search(self):
        """List files."""
        return None, 200

    # ItemView GET
    def read(self):
        """Read a single file."""
        return None, 200


# TODO: Remove - already removed default_config
class RecordFileActionResource(ActionResource):
    """Record file action resource."""


# TODO: Remove - already removed default_config
class DraftFileResource(FileResource):
    """File resource."""

    # TODO: No constructor for now.
    # Required when service level implementation.


# TODO: Remove - already removed default_config
class DraftFileActionResource(FileActionResource):
    """File action resource.

    NOTE: `Commit` exists as an action to avoid having to split the
    `FileResource` into Collection + Singleton to have to POST operations.
    """
