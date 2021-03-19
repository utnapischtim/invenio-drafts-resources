# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio Drafts Resources module to create REST APIs."""

from invenio_records_resources.resources import RecordResourceConfig
from invenio_records_resources.resources.actions import ActionResourceConfig
from invenio_records_resources.resources.records.schemas_links import \
    ItemLink, ItemLinksSchema


class DraftResourceConfig(RecordResourceConfig):
    """Draft resource config."""

    list_route = "/records/<pid_value>/draft"
    item_route = None

    links_config = {
        "record": ItemLinksSchema.create(links={
            "self": ItemLink(
                template="/api/records/{pid_value}/draft"
            ),
            "publish": ItemLink(
                template="/api/records/{pid_value}/draft/actions/publish",
                permission="publish",
            ),
        })
    }


class DraftActionResourceConfig(ActionResourceConfig):
    """Draft action resource config."""

    list_route = "/records/<pid_value>/draft/actions/<action>"
    item_route = None  # To avoid issues, due to inheritance.

    action_commands = {
        "create": {
            "publish": "publish",
        }
    }

    record_links_config = {
        "record": ItemLinksSchema.create(links={
            "self": ItemLink(
                template="/api/records/{pid_value}"
            ),
        })
    }
