#!/usr/bin/env sh
# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

pydocstyle invenio_drafts_resources tests docs && \
isort invenio_drafts_resources tests --check-only --diff && \
# check-manifest --ignore ".travis-*" && \
sphinx-build -qnNW docs docs/_build/html && \
pytest
