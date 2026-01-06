from __future__ import annotations

import time

import pytest

from enterprise_synthetic_data_hub.generation.generator import generate_snapshot_bundle


@pytest.mark.smoke
@pytest.mark.demo
def test_generator_rejects_zero_records():
    with pytest.raises(ValueError):
        generate_snapshot_bundle(num_records=0)


@pytest.mark.smoke
@pytest.mark.demo
def test_generate_1000_records_performance():
    start = time.perf_counter()
    bundle = generate_snapshot_bundle(num_records=1000)
    elapsed = time.perf_counter() - start
    assert bundle.metadata.record_count_persons == 1000
    assert bundle.metadata.record_count_vehicles == 1000
    # Keep performance expectations reasonable for CI runners.
    assert elapsed < 5
