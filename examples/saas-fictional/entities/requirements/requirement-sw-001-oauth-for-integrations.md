---
id: requirement-sw-001-oauth-for-integrations
title: "Software Requirement: OAuth for All Third-Party Integrations"
type: requirement
namespace: requirements
summary: "The software shall use OAuth 2.0 for all third-party integrations (GitHub, Linear, Jira). Personal access tokens are not supported in v1."
auto_inject: false
applicable_when: null
confidence: 0.95
verified_at: 2026-02-15
verified_by: nemock
staleness_signal: "Stable; OAuth 2.0 is the industry baseline. Revisit only if a target integration drops OAuth support."
tags: [requirement, software, auth]
requirement_class: software
edges:
  - target: requirement-user-001-self-serve-integration-setup
    type: supports
    weight: 0.85
    note: "OAuth is what makes self-serve setup possible without manual token management."
related: []
source_url: null
controlled_document: false
---

# Software Requirement: OAuth for All Third-Party Integrations

## Summary

OAuth 2.0 only.

## Statement

The software shall:

- Authenticate against GitHub, Linear, and Jira using OAuth 2.0 (PKCE flow where supported).
- Store refresh tokens encrypted at rest using the platform key-management service.
- Refresh access tokens automatically before expiry; surface explicit re-auth prompts only on refresh failure.
- NOT support personal access tokens, basic auth, or API keys as integration credentials in v1.

## Why software-class

This is a software-level statement (about code we write), not a system-level statement (about infrastructure or data flow). The SRS scaffold pulls it.

## Edges

`supports` the user-class self-serve requirement (OAuth is the mechanism that makes self-serve possible).
