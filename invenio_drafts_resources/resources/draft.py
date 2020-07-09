# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio Drafts Resources module to create REST APIs."""

from flask import g
from flask_resources import CollectionResource
from flask_resources.context import resource_requestctx
from flask_resources.loaders import RequestLoader
from flask_resources.resources import ResourceConfig

from ..responses import RecordResponse
from ..schemas import RecordSchemaJSONV1
from ..serializers import RecordJSONSerializer
from ..service import RecordService


# TODO: Get rid of them when implementation is done
STUB_ITEM_RESULT = ({"TODO": "IMPLEMENT ME"}, 200)
STUB_LIST_RESULT = ([{"TODO": "IMPLEMENT ME"}], 200)


class DraftResourceConfig(ResourceConfig):
    """Draft resource config."""

    item_route = "/records/<pid_value>/draft"
    # WARNING: Needed for creation, but breaks read / search!
    list_route = "/records/<pid_value>/draft"


class DraftResource(CollectionResource):
    """Record resource."""

    default_config = DraftResourceConfig

    def read(self, *args, **kwargs):
        """Read an item."""
        return STUB_ITEM_RESULT

    # WARNING: Create was only meant for list_route! Flask-Resource doesn't
    #          support item_route creation, so this is ... strange
    def create(self, *args, **kwargs):
        """Create an item."""
        return STUB_ITEM_RESULT

    def update(self, *args, **kwargs):
        """Update an item."""
        return STUB_ITEM_RESULT

    def delete(self, *args, **kwargs):
        """Delete an item."""
        return STUB_ITEM_RESULT


class DraftVersionResourceConfig(ResourceConfig):
    """Draft resource config."""

    list_route = "/records/<pid_value>/versions"


class DraftVersionResource(CollectionResource):
    """Draft version resource."""

    default_config = DraftVersionResourceConfig

    def search(self, *args, **kwargs):
        """Perform a search over the items."""
        # TODO: THIS IS A STUB. CHANGE ME FOR ACTUAL BUSINESS LOGIC
        return STUB_LIST_RESULT

    def create(self, *args, **kwargs):
        """Create an item."""
        # TODO: THIS IS A STUB. CHANGE ME FOR ACTUAL BUSINESS LOGIC
        return STUB_ITEM_RESULT
