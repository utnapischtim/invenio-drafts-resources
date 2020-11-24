# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Records-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio Resources module to create REST APIs"""

import pytest

BASE_RECORDS_FILES_ENDPOINT = "/mocks/12345-ABCD/files"
BASE_DRAFTS_FILES_ENDPOINT = "/mocks/12345-ABCD/draft/files"


# TODO: Test when file components controlling publish/edit work
@pytest.mark.skip()
def test_status_codes(client, es_clear, headers):
    """Test record creation."""
    h = headers
    # On a draft record
    # Initialize files upload
    response = client.post(BASE_DRAFTS_FILES_ENDPOINT, headers=h)
    assert response.status_code == 201
    # Upload a file
    response = client.put(
        f"{BASE_DRAFTS_FILES_ENDPOINT}/file.pdf/content", headers=h)
    # Temporary until service is implemented then 202
    assert response.status_code == 500
    # Commit the uploaded file
    response = client.post(
        f"{BASE_DRAFTS_FILES_ENDPOINT}/file.pdf/commit", headers=h)
    # Temporary until service is implemented then 202
    assert response.status_code == 500
    # Download the uploaded file
    response = client.get(
        f"{BASE_DRAFTS_FILES_ENDPOINT}/file.pdf/content", headers=h)
    # Temporary until service is implemented then 202
    assert response.status_code == 500
    # Update file metadata a second file
    response = client.put(f"{BASE_DRAFTS_FILES_ENDPOINT}/file.pdf", headers=h)
    assert response.status_code == 200
    # Read a file
    response = client.get(f"{BASE_DRAFTS_FILES_ENDPOINT}/file.pdf", headers=h)
    assert response.status_code == 200
    # Get all files a file
    response = client.get(BASE_DRAFTS_FILES_ENDPOINT, headers=h)
    assert response.status_code == 200
    # Delete a file
    response = client.delete(
        f"{BASE_DRAFTS_FILES_ENDPOINT}/file.pdf", headers=h)
    assert response.status_code == 204
    # Delete all files
    response = client.delete(BASE_DRAFTS_FILES_ENDPOINT, headers=h)
    assert response.status_code == 204

    # On a published record
    # Read a fil
    response = client.get(f"{BASE_RECORDS_FILES_ENDPOINT}/file.pdf", headers=h)
    assert response.status_code == 200
    # Get all files a file
    response = client.get(BASE_RECORDS_FILES_ENDPOINT, headers=h)
    assert response.status_code == 200
    # Download the uploaded file
    response = client.get(
        f"{BASE_RECORDS_FILES_ENDPOINT}/file.pdf/content", headers=h)
    # Temporary until service is implemented then 202
    assert response.status_code == 500
