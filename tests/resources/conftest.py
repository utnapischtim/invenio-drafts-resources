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
    DraftActionResourceConfig, DraftFileActionResource, \
    DraftFileActionResourceConfig, DraftFileResource, \
    DraftFileResourceConfig, DraftResource, DraftResourceConfig, \
    DraftVersionResource, DraftVersionResourceConfig, \
    RecordFileActionResource, RecordFileActionResourceConfig, \
    RecordFileResource, RecordFileResourceConfig, RecordResource, \
    RecordResourceConfig
from mock_module.service import Service, ServiceConfig


@pytest.fixture(scope="module")
def record_resource():
    """Record resource."""
    # FIXME
    # This should work but doesn't because the application context is checked
    # to see if it's been overridden in the config.
    # return Resource(service=Service())
    return RecordResource(
        config=RecordResourceConfig,
        service=Service(config=ServiceConfig)
    )


@pytest.fixture(scope="module")
def record_file_resource():
    """Record file resource."""
    return RecordFileResource(
        config=RecordFileResourceConfig,
        service=Service(config=ServiceConfig)
    )


@pytest.fixture(scope="module")
def record_file_action_resource():
    """Record file action resource."""
    return RecordFileActionResource(
        config=RecordFileActionResourceConfig,
        service=Service(config=ServiceConfig)
    )


@pytest.fixture(scope="module")
def draft_resource():
    """Draft resource."""
    # FIXME
    # This should work but doesn't because the application context is checked
    # to see if it's been overridden in the config.
    # return Resource(service=Service())
    return DraftResource(
        config=DraftResourceConfig,
        service=Service(config=ServiceConfig)
    )


@pytest.fixture(scope="module")
def draft_action_resource():
    """Draft action resource."""
    # FIXME
    # This should work but doesn't because the application context is checked
    # to see if it's been overridden in the config.
    # return Resource(service=Service())
    return DraftActionResource(
        config=DraftActionResourceConfig,
        service=Service(config=ServiceConfig)
    )


@pytest.fixture(scope="module")
def version_resource():
    """Draft version Resource."""
    # FIXME
    # This should work but doesn't because the application context is checked
    # to see if it's been overridden in the config.
    # return Resource(service=Service())
    return DraftVersionResource(
        config=DraftVersionResourceConfig,
        service=Service(config=ServiceConfig)
    )


@pytest.fixture(scope="module")
def draft_file_resource():
    """Draft file resource."""
    return DraftFileResource(
        config=DraftFileResourceConfig,
        service=Service(config=ServiceConfig)
    )


@pytest.fixture(scope="module")
def draft_file_action_resource():
    """Draft file action resource."""
    return DraftFileActionResource(
        config=DraftFileActionResourceConfig,
        service=Service(config=ServiceConfig)
    )


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
    # FIXME: Why is this commented out? Also in records-resources
    # base_app.register_error_handler(HTTPException, handle_http_exception)
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
