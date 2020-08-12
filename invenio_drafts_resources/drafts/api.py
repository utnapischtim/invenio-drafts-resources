# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Draft API."""

from invenio_db import db
from invenio_records.api import Record


class DraftBase(Record):
    """Draft base API for metadata creation and manipulation."""

    # WHY: We want to force the model_cls to be specified by the user
    # No default one is given, only the base.
    model_cls = None

    @property
    def expires_at(self):
        """Get model identifier."""
        return self.model.expires_at if self.model else None

    @property
    def fork_id(self):
        """Get revision identifier."""
        return self.model.fork_id if self.model else None

    @classmethod
    def create(cls, data, id_, fork_version_id=None, **kwargs):
        """Create a new draft instance and store it in the database."""
        with db.session.begin_nested():
            draft = cls(data)

            draft.validate(**kwargs)

            draft.model = cls.model_cls(
                id=id_,
                fork_version_id=fork_version_id,
                expires_at=draft.expires_at,
                json=draft,
            )

            db.session.add(draft.model)

        return draft
