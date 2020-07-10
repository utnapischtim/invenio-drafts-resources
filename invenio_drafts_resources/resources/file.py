# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Draft File Resource."""

from flask_resources import CollectionResource, SingletonResource
from flask_resources.context import resource_requestctx
# TODO: expose correctly in flask-resources
from flask_resources.resources import ResourceConfig

# TODO: Get rid of them when implementation is done
STUB_ITEM_RESULT = ({"TODO": "IMPLEMENT ME"}, 200)
STUB_LIST_RESULT = ([{"TODO": "IMPLEMENT ME"}], 200)


class DraftFileResourceConfig(ResourceConfig):
    """Draft file resource config."""

    list_route = "/records/<pid_value>/draft/files"
    item_route = "/records/<pid_value>/draft/files/<key>"


class DraftFileResource(CollectionResource):
    """Draft file resource."""

    default_config = DraftFileResourceConfig

    # List level
    def search(self, *args, **kwargs):
        """Search over items."""
        return STUB_ITEM_RESULT

    def create(self, *args, **kwargs):
        """Create an item."""
        return STUB_ITEM_RESULT

    def update_all(self, *args, **kwargs):
        """Delete an item."""
        return STUB_ITEM_RESULT

    def delete_all(self, *args, **kwargs):
        """Delete an item."""
        return STUB_ITEM_RESULT

    # Item level
    def read(self, *args, **kwargs):
        """Read an item."""
        return STUB_ITEM_RESULT

    def update(self, *args, **kwargs):
        """Update an item."""
        return STUB_ITEM_RESULT

    def delete(self, *args, **kwargs):
        """Delete an item."""
        return STUB_ITEM_RESULT


class DraftFileActionResourceConfig(ResourceConfig):
    """Draft file action resource config."""

    # QUESTIONs:
    # 1- Should the item_route be used for SingletonResource actually? Change
    #    in Flask-Resource would be needed
    # 2- Should the list_route instead precede download with "actions" to be in
    #    keeping with other actions endpoints?
    list_route = "/records/<pid_value>/draft/files/<key>/<action>"


class DraftFileActionResource(SingletonResource):
    """Draft file action resource."""

    default_config = DraftFileResourceConfig

    def read(self, *args, **kwargs):
        """Read an item."""
        if resource_requestctx.route["action"] == "download":
            return STUB_ITEM_RESULT
        return {}, 200
