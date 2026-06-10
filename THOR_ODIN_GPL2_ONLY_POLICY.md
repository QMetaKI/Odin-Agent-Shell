# Thor + Odin GPL-2.0-only Policy

## License identity
Odin-Agent-Shell is licensed GPL-2.0-only. Thor-Agent-Kit is expected to use the same license identity when used as the sibling AI-Git handoff system.

## Rationale
Thor+Odin are not ordinary helper libraries. They are intended as AI-Git infrastructure: handoff compiler, candidate protocol, review/gate system, boundary layer, semantic diff surface and safety spine. GPL-2.0-only preserves the expectation that distributed modifications to the implementation remain source-available under the same copyleft terms.

## Repository rule
Unless a file states otherwise, every source file, documentation file, schema, registry, example, template, validator and test in this repository is covered by GPL-2.0-only.

## Protocol boundary note
Interoperability through documented JSON packets, CLI boundaries, local APIs or file artifacts is conceptually a protocol boundary. Independent implementations that do not copy GPL-covered implementation code should be treated separately by maintainers. This policy is a technical project statement, not legal advice.

## Required repository files
- LICENSE
- LICENSE_POLICY.md
- THOR_ODIN_GPL2_ONLY_POLICY.md
- PROTOCOL_BOUNDARY.md
- SPDX_POLICY.md
- THIRD_PARTY_NOTICES.md

## SPDX policy
New source files should include `SPDX-License-Identifier: GPL-2.0-only` where technically appropriate.
