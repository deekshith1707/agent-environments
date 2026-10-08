"""
dataproc/aggregator.py — BUGGY version seeded for env_004.

Known bugs:
  1. ZeroDivisionError when any record has count == 0.
  2. Records with negative value are silently filtered out (unintentional).
"""
from __future__ import annotations
from typing import TypedDict


class Record(TypedDict):
    name: str
    value: float
    count: int


def summarise_records(records: list[Record]) -> dict:
    """
    Given a list of records, return a summary dict:
      {
        "total_value": float,      # sum of (value * count) for each record
        "average_value": float,    # total_value / total_count
        "record_count": int,       # number of records processed
        "total_count": int,        # sum of count fields
      }

    Records with count == 0 should be skipped.
    Records with negative value are valid and must be included.
    """
    # BUG 1: no guard for count == 0  → ZeroDivisionError below
    # BUG 2: filters out negative values unintentionally
    filtered = [r for r in records if r["value"] > 0]   # BUG: should be >= or no filter

    total_value = sum(r["value"] * r["count"] for r in filtered)
    total_count = sum(r["count"] for r in filtered)

    # BUG 1 manifests here when total_count == 0 due to a zero-count record
    average_value = total_value / total_count

    return {
        "total_value": total_value,
        "average_value": average_value,
        "record_count": len(filtered),
        "total_count": total_count,
    }
