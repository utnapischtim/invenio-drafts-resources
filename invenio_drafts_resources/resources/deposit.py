# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio Deposits Resources."""

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


# Proposal: "Deposits" is the term to talk about entities that are either
#           draft or published records
class DepositResourceConfig(ResourceConfig):
    """Deposit resource config."""

    list_route = "/user/records"


class DepositResource(CollectionResource):
    """Record resource."""

    default_config = DepositResourceConfig

    def search(self, *args, **kwargs):
        """Perform a search over the items."""
        # TODO: THIS IS A STUB. CHANGE ME FOR ACTUAL BUSINESS LOGIC
        return STUB_LIST_RESULT
