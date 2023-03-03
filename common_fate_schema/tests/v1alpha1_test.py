from pathlib import Path
import json
import pytest
from common_fate_schema.provider import v1alpha1
from syrupy.extensions.json import JSONSnapshotExtension
from syrupy.location import PyTestLocation
from syrupy.types import SnapshotIndex


class SchemaOutputExtension(JSONSnapshotExtension):
    @classmethod
    def dirname(cls, *, test_location: "PyTestLocation") -> str:
        return str(
            Path(test_location.filepath).parent.parent.parent.joinpath(
                "output/provider"
            )
        )

    @classmethod
    def get_snapshot_name(
        cls, *, test_location: "PyTestLocation", index: "SnapshotIndex"
    ) -> str:
        original_name = JSONSnapshotExtension.get_snapshot_name(
            test_location=test_location, index=index
        )
        return original_name.removeprefix("test_")


@pytest.fixture
def snapshot_json(snapshot):
    """use JSON, rather than AmberSnapshotExtension as our schema is serialized as JSON"""
    return snapshot.use_extension(SchemaOutputExtension)


def test_v1alpha1(snapshot_json):
    schema_str = v1alpha1.Schema.schema_json()
    actual = json.loads(schema_str)
    assert actual == snapshot_json
