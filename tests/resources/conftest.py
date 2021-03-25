# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Pytest configuration.

See https://pytest-invenio.readthedocs.io/ for documentation on which test
fixtures are available.
"""

import pytest
from flask_principal import Identity, Need, UserNeed
from invenio_records_resources.resources import FileResource
from mock_module.resource import DraftFileResourceConfig, FileResourceConfig, \
    RecordResourceConfig
from mock_module.service import ServiceConfig

from invenio_drafts_resources.resources import RecordResource
from invenio_drafts_resources.services.records import RecordService


@pytest.fixture(scope="module")
def service(appctx):
    """Service instance."""
    return RecordService(ServiceConfig)


@pytest.fixture(scope="module")
def record_resource(service):
    """Record resource."""
    return RecordResource(config=RecordResourceConfig, service=service)


@pytest.fixture(scope="module")
def file_resource(service):
    """File resource."""
    return FileResource(config=FileResourceConfig, service=service)


@pytest.fixture(scope="module")
def draft_file_resource(service):
    """Draft file resource."""
    return FileResource(config=DraftFileResourceConfig, service=service)


@pytest.fixture(scope="module")
def base_app(
        base_app, record_resource, file_resource, draft_file_resource):
    """Application factory fixture."""
    base_app.register_blueprint(record_resource.as_blueprint())
    base_app.register_blueprint(file_resource.as_blueprint())
    base_app.register_blueprint(draft_file_resource.as_blueprint())
    yield base_app


@pytest.fixture(scope="module")
def identity_simple():
    """Simple identity fixture."""
    i = Identity(1)
    i.provides.add(UserNeed(1))
    i.provides.add(Need(method='system_role', value='any_user'))
    return i


@pytest.fixture(scope="module")
def headers():
    """Default headers for making requests."""
    return {
        'content-type': 'application/json',
        'accept': 'application/json',
    }
