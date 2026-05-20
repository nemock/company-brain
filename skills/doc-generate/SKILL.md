---
name: doc-generate
description: Generate planning documents from the vault. Profile-aware section inclusion. v1 ships a full MRD generator with evidence-vs-vision split, anti-decisions section, and IFU comparison (medical-device profile). PID, business plan, competitive brief, and risk brainstorm ship as scaffolds in v0.4.0.
---

# doc-generate

> Placeholder skill. MRD pipeline lands in v0.3.0; scaffolds for other generators land in v0.4.0.

Documents in v1:

| Document | v1 status |
|---|---|
| Marketing Requirements Document (MRD) | Fully implemented |
| Project Initiation Document (PID) | Scaffold |
| Business Plan | Scaffold |
| Competitive Brief | Scaffold |
| Risk Brainstorm (medical-device only) | Scaffold |

All output is profile-aware: medical-device-only sections (IFU, regulatory landscape) are omitted entirely when the active profile doesn't enable them. Every generated document carries the controlled-document-boundary footer when the medical-device profile is active.

See [PRD.md §11](../../PRD.md) for the MRD output structure and [docs/controlled-document-boundary.md](../../docs/controlled-document-boundary.md) for the boundary policy.
