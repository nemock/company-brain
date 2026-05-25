# Profiles

A **profile** is a configuration that determines which node types, intake sub-modes, and document sections are active in a vault. The profile mechanism is the company-brain pattern for "same schema engine, different industries."

A vault declares its profile in `_system/PROFILE.md`. The active profile drives:

- Which folders the [`vault-architect`](../skills/vault-architect/SKILL.md) skill creates (`cb scaffold --profile <name>`).
- Which node types the validator accepts.
- Which intake sub-modes the [`intake`](../skills/intake/SKILL.md) skill exposes.
- Which sections appear in generated documents (medical-device-only sections are omitted entirely, not rendered empty).
- Which scaffolded generators run vs. raise (e.g. `cb render risk-register` requires the medical-device profile).
- Whether the controlled-document footer is appended to generated docs.

## v0.5.0 profiles

| Profile | Status | What it adds beyond the universal types |
|---|---|---|
| `default` | shipped | Nothing — only the universal epistemic + entity types. Right for software, SaaS, services, consumer products, and most non-regulated industries. |
| `medical-device` | shipped | `indication-for-use`, `regulatory-clearance`, `risk-insight`, `hazard`, `hazardous-situation`, `harm`, `risk-control-idea`, `regulation`, `standard`. Plus the controlled-document-boundary footer on every generated doc. |
| `saas` | reserved | Slot held for v1.x. Distinct from `default` in that it will eventually add SaaS-specific node types (e.g. `pricing-experiment`, `growth-loop`). For now, use `default`. |
| `hardware` | reserved | Slot held for v1.x. Will eventually add `component`, `kit`, `bom-item` for BOM modeling (per PRD §18). |
| `services` | reserved | Slot held for v1.x. Will eventually add `engagement`, `service-tier`, `delivery-template`. |

The universal types (epistemic + entity) are always available. The active profile only adds to that base; it never removes a universal type.

## Worked example: medical-device vs default

The two shipped profiles are exercised by the two example vaults. Compare:

- [`examples/meddev-fictional/`](../examples/meddev-fictional/) — `medical-device` profile, a fictional ambulatory cardiac monitor company.
- [`examples/saas-fictional/`](../examples/saas-fictional/) — `default` profile, a fictional engineering productivity analytics company.

### Active node types

```bash
cb describe-profile --name medical-device | jq '.active_node_types[].name'
cb describe-profile --name default        | jq '.active_node_types[].name'
```

The medical-device profile has 30 active node types; the default profile has 21. The 9 extra types are the medical-device-only ones listed above.

### MRD section structure

| Section | medical-device | default |
|---|:-:|:-:|
| 1 Executive summary | ✅ | ✅ |
| 2 Vision and positioning | ✅ | ✅ |
| 3 Indications for use | ✅ | — |
| 4 → 3 Market and personas | ✅ | ✅ |
| 5 → 4 Market requirements | ✅ | ✅ |
| 6 → 5 Competitive landscape | ✅ | ✅ |
| 7 Regulatory landscape | ✅ | — |
| 8 → 6 Evidence vs. vision split | ✅ | ✅ |
| 9 → 7 Open questions | ✅ | ✅ |
| 10 → 8 What we are explicitly not doing | ✅ | ✅ |
| 11 → 9 Sources | ✅ | ✅ |

The shifted section numbers are deliberate. The default-profile MRD reads as a coherent 9-section document; it does not have a gap where §3 and §7 would be.

### Doc-generate scaffolds

19 scaffolds ship in v0.4.0. Three are medical-device-only:

| Scaffold | Profile required |
|---|---|
| `risk-register` | medical-device |
| `ifu-comparison` | medical-device |
| `risk-brainstorm` | medical-device |

The other 16 scaffolds work on any profile. Each scaffold's data-assembly function pulls only the nodes it can use; on a sparser vault it degrades to bracketed placeholders with a hint to run the right `intake` sub-mode.

### Controlled-document footer

```
> This is a planning artifact. It is not a controlled document and is not part of
> any design history file, risk management file, or traceability matrix per
> ISO 14971, IEC 62304, or 21 CFR 820.
```

This footer is appended to every generated document **only** when the active profile is `medical-device`. The default profile does not append it; medical-device users get it for free without having to remember.

## How to choose

- **Software / SaaS / services / consumer products / most B2B verticals** → `default`. Use it now; the future `saas` / `services` profile slots will be opt-in upgrades when they ship.
- **Medical devices, in-vitro diagnostics, or anything that touches ISO 14971** → `medical-device`. Even pre-clearance startups benefit from the IFU / clearance / risk vocabulary being first-class.

You cannot flip the profile of an existing vault in place. Re-scaffolding into the same directory with a different profile leaves orphan folders from the previous profile. Pick at vault creation and stay with that choice.

## Forking a profile

If you need a custom profile for an industry company-brain doesn't ship — say, automotive functional safety with ISO 26262 vocabulary — fork the company-brain repo, add your profile to [`src/company_brain/schema/profiles.py`](../src/company_brain/schema/profiles.py) and the relevant node types to [`src/company_brain/schema/node_types.py`](../src/company_brain/schema/node_types.py), and submit a PR. The schema is data; new profiles are typically a small change.

## Inspecting a vault's profile

```bash
cb describe-profile --path <vault>     # reads from _system/PROFILE.md
cb describe-profile --name medical-device   # describe by name
cb describe-node indication-for-use --path <vault>
```

The describe commands are read-only and return JSON, useful for both human inspection and skill scripting.
