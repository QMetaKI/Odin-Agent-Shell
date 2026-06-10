# Acceptance Tests v7.1

## Universal Work

- valid rewrite work accepted
- invalid missing binding rejected
- forbidden verb rejected
- blocked output contract rejected
- candidate-only contract accepted

## Semantic Bus

- local-only channels loaded
- event envelope validated
- batch replay reconstructs work path
- blocked_sensitive payload rejected

## Model Routes

- default route is 3B+7B/8B hybrid for standard local quality
- low memory strict avoids 7B default
- quality model is escalation only
- remote requires explicit permission

## Candidate Output

- every response contains candidate artifact
- app-owned actions do not execute in Odin
- candidate DNA links trace/work/bus/slots

## Claim Boundary

- unsupported claims blocked or downgraded
- model output cannot become truth without app acceptance or receipt
