from __future__ import annotations

from datetime import datetime

from enterprise_synthetic_data_hub.models.dataset_metadata import DatasetMetadata


def test_dataset_metadata_counts():
    metadata = DatasetMetadata(
        dataset_version="v0.1",
        generated_at=datetime(2024, 6, 1, 0, 0, 0),
        record_count_persons=1,
        record_count_vehicles=1,
        notes="placeholder",
    )

    assert metadata.record_count_persons >= 0
    assert metadata.record_count_vehicles >= 0
    assert metadata.dataset_version == "v0.1"
