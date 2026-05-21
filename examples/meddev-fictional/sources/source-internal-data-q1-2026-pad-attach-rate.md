---
id: source-internal-data-q1-2026-pad-attach-rate
title: "Internal Data: Q1 2026 Pad Attach Rate Cohort"
type: source
namespace: internal-data
summary: "Internal data: 14-patient pilot cohort at Northstar Cardiology, Q1 2026; day-1 attach rate and pad-failure timing observations."
auto_inject: false
applicable_when: null
confidence: 0.85
verified_at: 2026-05-21
verified_by: nemock
staleness_signal: "Frozen — Q1 2026 cohort. New cohorts become their own source nodes."
tags: [internal-data, cohort]
source_kind: internal-data
edges: []
related: []
source_url: null
controlled_document: false
---

# Internal Data: Q1 2026 Pad Attach Rate Cohort

## Summary

The Q1 2026 trial cohort at Northstar Cardiology — 14 patients, 7-day monitoring episodes, day-1 attach rate and failure-timing observations. Underlies the pattern node and the metric snapshots.

## Key Claims (from the data)

- Day-1 attach rate: ~89% over the cohort (12/14 patients with continuous data through hour 24).
- Failures clustered between days 8-11 for the two patients who had partial pad lift.
- No patient required clinic intervention for pad replacement.

## Interpretation

This data is the empirical foundation for `pattern-pad-adhesion-failure-precedes-data-dropout` and `fact-pad-attach-rate-2026-q1`. Confidence is high because the data is direct measurement, but the cohort is small.

## Notes

`source_kind: internal-data` flags this as company-internal observation. The MRD generator would label any claim derived from this source as evidence-driven (not vision).
