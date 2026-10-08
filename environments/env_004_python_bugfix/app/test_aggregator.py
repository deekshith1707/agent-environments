"""
Existing tests for dataproc.aggregator — DO NOT modify or delete these.
The agent must add new tests below the existing ones.
"""
import pytest
from dataproc.aggregator import summarise_records


# ── Existing tests ────────────────────────────────────────────────────────────

def test_basic_summary():
    records = [
        {"name": "alpha", "value": 10.0, "count": 2},
        {"name": "beta",  "value": 5.0,  "count": 4},
    ]
    result = summarise_records(records)
    assert result["total_value"] == 40.0    # 10*2 + 5*4
    assert result["total_count"] == 6
    assert result["record_count"] == 2
    assert abs(result["average_value"] - (40.0 / 6)) < 1e-9


def test_single_record():
    records = [{"name": "solo", "value": 7.5, "count": 3}]
    result = summarise_records(records)
    assert result["total_value"] == 22.5
    assert result["average_value"] == 7.5
    assert result["record_count"] == 1
    assert result["total_count"] == 3


def test_empty_records():
    """An empty list should return zeros without raising."""
    result = summarise_records([])
    assert result["total_value"] == 0
    assert result["total_count"] == 0
    assert result["record_count"] == 0
    # average_value is undefined for empty input; we accept 0 or None
    assert result.get("average_value") in (0, None, 0.0)


# ── Agent must add tests below this line ─────────────────────────────────────
# Required:
#   1. test_zero_count_records — ensures zero-count records are skipped, no ZeroDivisionError
#   2. test_negative_value_records — ensures negative values are included in the summary
