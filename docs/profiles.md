# Profiles

> Placeholder. The profile mechanism lands with v0.1.0 — see [PRD.md §8](../PRD.md).

A **profile** is a configuration that determines which node types, intake sub-modes, and document sections are active in a vault. v1 ships the `medical-device` profile; `saas`, `hardware`, and `services` slots are reserved.

When v0.1.0 ships, this document will cover:

- How `_system/PROFILE.md` declares the active profile.
- The `medical-device` profile in detail.
- The `default` industry-agnostic profile.
- How profile-conditional document sections are omitted entirely (not rendered empty) when the active profile doesn't enable them.
- How to fork an existing profile for a custom industry.
