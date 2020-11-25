# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Records service copmonent base classes."""

from invenio_records_resources.services.records.components import \
    FilesComponent, MetadataComponent, ServiceComponent


class DraftFilesComponent(FilesComponent):
    """Draft files service component."""

    # TODO: Add tests for publishing a draft with files
    def publish(self, draft=None, record=None):
        """Copy bucket and files to record."""
        draft_files = draft.files
        bucket = draft_files.bucket
        if bucket:
            # Set the draft bucket on the record also
            record.bucket = bucket
            record.bucket_id = bucket.id
            # Lock the bucket
            bucket.locked = True
            # TODO: actually "sync"
            # Copy over the files
            for key, df in draft_files.items():
                # TODO: Fix __setitem__ in FilesField, to support `None` for
                # metadata
                if df.metadata is not None:
                    record.files[key] = df.object_version, df.metadata
                else:
                    record.files[key] = df.object_version


class RelationsComponent(ServiceComponent):
    """Service component for PID relations integration."""

    # PIDNodeVersioning(pid=conceptrecid).insert_draft_child(child_pid=recid)


class DraftMetadataComponent(MetadataComponent):
    """Service component for draft metadata integration."""

    def update_draft(self, *args, **kwargs):
        """Update draft metadata."""
        self.update(*args, **kwargs)
