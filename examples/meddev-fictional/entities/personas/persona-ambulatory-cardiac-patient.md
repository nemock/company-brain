---
id: persona-ambulatory-cardiac-patient
title: "Persona: Ambulatory Cardiac Patient"
type: persona
namespace: market
summary: "Adult patient discharged from cardiology service with continuous-monitoring orders for 7-30 days; mobile, lives at home, manages own pad changes."
auto_inject: false
applicable_when: null
confidence: 0.8
verified_at: 2026-05-21
verified_by: nemock
staleness_signal: "Revise after the next round of customer interviews if the persona shape changes materially."
tags: [persona]
edges:
  - target: pillar-icp-ambulatory-cardiac-patients
    type: supports
    weight: 0.9
    note: "Persona is the human shape of the ICP."
  - target: source-customer-interview-2026-04-12-nurse-anderson
    type: derived_from
    weight: 0.6
    note: "Interview informed the persona; not the sole source."
related: []
source_url: null
controlled_document: false
---

# Persona: Ambulatory Cardiac Patient

## Summary

An adult patient (typically 55+) who has just been discharged from a cardiology service or referred for ambulatory monitoring. Has a smartphone or can borrow one. Comfortable with self-care once the routine is established. Wants to be done with monitoring as quickly as clinically appropriate.

## Content

What the persona cares about:

- Getting the monitoring window over with so the cardiologist can make a call.
- Not getting woken up at night by a poorly-placed sensor.
- Knowing the device is "doing its job" without having to interpret data.
- A pad change that doesn't require a clinic visit.

What the persona does NOT care about:

- The wearable being slim or beautiful (though it shouldn't be obviously medical-looking in public).
- Owning the device — they want a service, not a gadget.
- Fitness data, sleep tracking, or any non-cardiac signal.

## Edges

`supports` the ICP pillar — the persona is the human-readable version of the abstract ICP.

## Notes

A second important persona — the care-team nurse — is implicit in the customer-interview source. We have not yet promoted "nurse" to its own persona node because the trial cohort interactions have been mediated by the primary persona above.
