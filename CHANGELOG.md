# Changelog

## Unreleased — 2026-11-03

### Fixed

- Validate date ordering and uniqueness when `analyze()` is called directly from Python, instead of only relying on checks performed by CSV loading.
- Reject negative, non-finite, non-numeric, and boolean inflow values before statistical calculations.
- Reject malformed date objects with actionable `ValueError` messages.

### Tests

- Add regression tests for out-of-order and duplicated dates, invalid measurements, direct API calls, and missing calendar days.

No new field dataset, experimental validation, user adoption, or production-readiness is claimed.
