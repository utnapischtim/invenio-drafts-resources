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
from flask_resources import SingletonResource
from flask_resources.context import resource_requestctx
from invenio_records_resources.resources.actions import ActionResource


class DraftResource(SingletonResource):
    """Draft resource."""

    def __init__(self, config=None, service=None):
        """Constructor."""
        super().__init__(config=config)
        self.service = service

    def read(self):
        """Edit a draft.

        GET /records/:pid_value/draft
        """
        item = self.service.read_draft(
            resource_requestctx.route["pid_value"],
            g.identity,
            links_config=self.config.links_config,
        )
        return item.to_dict(), 200

    def create(self):
        """Edit a record.

        POST /records/:pid_value/draft
        """
        item = self.service.edit(
            resource_requestctx.route["pid_value"],
            g.identity,
            links_config=self.config.links_config,
        )
        return item.to_dict(), 201

    def update(self):
        """Update a draft.

        PUT /records/:pid_value/draft
        """
        data = resource_requestctx.request_content
        item = self.service.update_draft(
            resource_requestctx.route["pid_value"],
            g.identity,
            data,
            links_config=self.config.links_config,
            revision_id=resource_requestctx.headers.get("if_match"),
        )
        return item.to_dict(), 200

    def delete(self):
        """Delete a draft.

        DELETE /records/:pid_value/draft
        """
        self.service.delete_draft(
            resource_requestctx.route["pid_value"],
            g.identity,
            revision_id=resource_requestctx.headers.get("if_match"),
        )
        return None, 204


class DraftActionResource(ActionResource):
    """Draft action resource."""

    def __init__(self, config=None, service=None):
        """Constructor."""
        super().__init__(config=config)
        self.service = service

    def create_publish(self, action, operation):
        """Publish the draft."""
        cmd_func = self._get_cmd_func(action, operation)
        item = cmd_func(
            resource_requestctx.route["pid_value"],
            g.identity,
            links_config=self.config.record_links_config
        )
        return item.to_dict(), 202
