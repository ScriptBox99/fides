from os import path

import pytest

from fidesctl.core import export
from fideslang.models import (
    Dataset,
    DatasetCollection,
    DatasetField,
    Organization,
    PrivacyDeclaration,
    System,
)


@pytest.fixture()
def test_sample_system_taxonomy():
    yield [
        System(
            fides_key="test_system",
            system_type="test",
            system_name="test system",
            system_description="system used for testing exports",
            privacy_declarations=[
                PrivacyDeclaration(
                    name="privacy_declaration_1",
                    data_categories=["account.contact.email", "account.contact.name"],
                    data_use="provide.system",
                    data_qualifier="aggregated.anonymized",
                    data_subjects=["customer"],
                    dataset_references=["users_dataset"],
                )
            ],
        )
    ]


@pytest.fixture()
def test_sample_dataset_taxonomy():
    yield [
        Dataset(
            fides_key="test_dataset",
            name="test dataset",
            description="dataset for testing",
            dataset_categories=[],
            collections=[
                DatasetCollection(
                    name="test_collection",
                    data_categories=[],
                    fields=[
                        DatasetField(
                            name="test_field_1",
                            data_categories=["test_category_1"],
                            data_qualifier="aggregated.anonymized",
                            retention="No retention policy",
                        ),
                        DatasetField(
                            name="test_field_2",
                            data_categories=["test_category_2", "test_category_3"],
                            data_qualifier="aggregated.anonymized",
                        ),
                        DatasetField(
                            name="test_field_3",
                            data_categories=["test_category_3"],
                            data_qualifier="aggregated.anonymized",
                        ),
                        DatasetField(
                            name="test_field_4",
                            data_categories=["test_category_2"],
                            data_qualifier="aggregated.anonymized",
                        ),
                    ],
                )
            ],
        )
    ]


@pytest.mark.unit
def test_system_records_to_export(test_sample_system_taxonomy, test_config):
    """
    Asserts that unique records are returned properly (including
    the header row)
    """
    output_list = export.generate_system_records(
        test_sample_system_taxonomy,
        url=test_config.cli.server_url,
        headers=test_config.user.request_headers,
    )
    print(output_list)
    assert len(output_list) == 3


@pytest.mark.unit
def test_dataset_records_to_export(test_sample_dataset_taxonomy):
    """
    Asserts that unique records are returned properly (including
    the header row)
    """

    output_list = export.generate_dataset_records(test_sample_dataset_taxonomy)

    assert len(output_list) == 4


@pytest.mark.unit
def test_organization_records_to_export():
    """
    Asserts the default organization is successfully exported
    """

    output_list = export.generate_contact_records(
        [Organization(fides_key="default_organization")]
    )
    assert len(output_list) == 5
