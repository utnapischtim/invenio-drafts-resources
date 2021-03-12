"""Example of a record draft API."""

from invenio_records.systemfields import ConstantField
from invenio_records_resources.records.systemfields import IndexField

from invenio_drafts_resources.records.api import Draft as DraftBase
from invenio_drafts_resources.records.api import \
    ParentRecord as ParentRecordBase
from invenio_drafts_resources.records.api import Record as RecordBase

from .models import DraftMetadata, ParentRecordMetadata, ParentState, \
    RecordMetadata


class ParentRecord(ParentRecordBase):
    """Example parent record."""

    # Configuration
    model_cls = ParentRecordMetadata

    # System fields
    schema = ConstantField(
        '$schema', 'http://localhost/schemas/records/parent-v1.0.0.json')


class Record(RecordBase):
    """Example record API."""

    # Configuration
    model_cls = RecordMetadata
    versions_model_cls = ParentState
    parent_record_cls = ParentRecord

    # System fields
    schema = ConstantField(
        '$schema', 'http://localhost/schemas/records/record-v1.0.0.json')

    index = IndexField(
        'draftsresources-records-record-v1.0.0',
        search_alias='draftsresources-records'
    )


class Draft(DraftBase):
    """Example record API."""

    # Configuration
    model_cls = DraftMetadata
    versions_model_cls = ParentState
    parent_record_cls = ParentRecord

    # System fields
    schema = ConstantField(
        '$schema', 'http://localhost/schemas/records/record-v1.0.0.json')

    index = IndexField(
        'draftsresources-drafts-draft-v1.0.0',
        search_alias='draftsresources-drafts'
    )
