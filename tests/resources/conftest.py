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
from mock_module.resource import DraftActionResource, \
    DraftActionResourceConfig, DraftFileActionResourceConfig, \
    DraftFileResourceConfig, DraftResourceConfig, \
    RecordFileActionResourceConfig, RecordFileResourceConfig, \
    RecordResourceConfig, RecordVersionsResourceConfig
from mock_module.service import ServiceConfig

from invenio_drafts_resources.resources import DraftFileActionResource, \
    DraftFileResource, DraftResource, RecordFileActionResource, \
    RecordFileResource, RecordResource, RecordVersionsResource
from invenio_drafts_resources.services.records import RecordDraftService


@pytest.fixture(scope="module")
def service(appctx):
    """Service instance."""
    return RecordDraftService(ServiceConfig)


@pytest.fixture(scope="module")
def record_resource(service):
    """Record resource."""
    return RecordResource(config=RecordResourceConfig, service=service)


@pytest.fixture(scope="module")
def record_file_resource(service):
    """Record file resource."""
    return RecordFileResource(config=RecordFileResourceConfig, service=service)


@pytest.fixture(scope="module")
def record_file_action_resource(service):
    """Record file action resource."""
    return RecordFileActionResource(
        config=RecordFileActionResourceConfig, service=service)


@pytest.fixture(scope="module")
def draft_resource(service):
    """Draft resource."""
    return DraftResource(config=DraftResourceConfig, service=service)


@pytest.fixture(scope="module")
def draft_action_resource(service):
    """Draft action resource."""
    return DraftActionResource(
        config=DraftActionResourceConfig, service=service)


@pytest.fixture(scope="module")
def version_resource(service):
    """Draft version Resource."""
    return RecordVersionsResource(
        config=RecordVersionsResourceConfig, service=service)


@pytest.fixture(scope="module")
def draft_file_resource(service):
    """Draft file resource."""
    return DraftFileResource(config=DraftFileResourceConfig, service=service)


@pytest.fixture(scope="module")
def draft_file_action_resource(service):
    """Draft file action resource."""
    return DraftFileActionResource(
        config=DraftFileActionResourceConfig, service=service)


@pytest.fixture(scope="module")
def base_app(
        base_app, record_resource, record_file_resource,
        record_file_action_resource, draft_resource, draft_action_resource,
        version_resource, draft_file_resource, draft_file_action_resource):
    """Application factory fixture."""
    # records
    base_app.register_blueprint(record_resource.as_blueprint('mock_record'))
    # record files
    base_app.register_blueprint(
        record_file_resource.as_blueprint('mock_record_files'))
    base_app.register_blueprint(
        record_file_action_resource.as_blueprint('mock_record_files_action'))
    # drafts
    base_app.register_blueprint(draft_resource.as_blueprint('mock_draft'))
    base_app.register_blueprint(
        draft_action_resource.as_blueprint('mock_draft_action'))
    base_app.register_blueprint(version_resource.as_blueprint('mock_version'))
    # draft files
    base_app.register_blueprint(
        draft_file_resource.as_blueprint('mock_draft_files'))
    base_app.register_blueprint(
        draft_file_action_resource.as_blueprint('mock_draft_files_action'))
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
