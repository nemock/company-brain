# Master Node Index

This file is the agent's primary entry point. The `maintain` skill keeps it in sync as nodes are added; for now it is a starter scaffold.

**Active profile**: `medical-device`.

## Retrieval protocol

1. **Phase 1**: read summaries here and any pillar with `auto_inject: true` whose `applicable_when` matches the question.
2. **Phase 2**: load full bodies for surviving candidates and walk their `edges` frontmatter one hop. Most answers live within one or two hops.

## Node tables

Total nodes: 0.

_(No nodes yet. Use the `intake` or `atomize` skill to add some, then run `cb validate --fix` to populate this index.)_
