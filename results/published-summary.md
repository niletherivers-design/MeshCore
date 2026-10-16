# Published Results

## MeshCore v1.2.0

MeshCore v1.2.0 completed its standalone qualification as a **FULLY FROZEN
PASS**.

The public-facing release summary intentionally records only selected,
sanitary release facts and does not reproduce the complete internal research
environment.

### Final Freeze

- Final release freeze: PASS
- Final staged integrity verification: PASS
- Final integrity entries: 37
- Final release attestation consumed exactly once
- Production files changed during final freeze: NO
- Docker/tests/pytest rerun during final freeze: NO
- Production authority: OFF

### Runtime Corrective Validation

The qualification chain identified a production Docker package-layout import
defect and carried a forward-only correction through validation before the
final release freeze.

Corrected runtime evidence included:

- 35 OpenAPI operations
- 6 routes
- 5 application-namespace modules
- 0 duplicate routes

### Frozen Evidence Hashes

`results/v120/FINAL-ATTESTATION.txt`

    5a1842a41c9ab9f68ad61f9ba2828ea7c63c03b411ae8cc05a40f0d283491beb

`results/v120/FINAL-INTEGRITY.sha256`

    412f9a8f0866c35eadedf16dbe49fb042f2d5fe0e4320abbb56d1cbcacbeade1

These hashes identify the final sealed internal release evidence. Historical
one-shot v1.2.0 qualification gates must not be rerun or regenerated.

## Scope

The v1.2.0 frozen status applies to MeshCore as a standalone project. Later
REVA/Odysseus integration, production deployment authorization, and future
MeshCore development are separate workstreams.
