# MeshCore v1.2.0 Release Notes

## Status

**FULLY FROZEN PASS**

MeshCore v1.2.0 completed its standalone qualification and final release
freeze. The v1.2.0 evidence chain is sealed; historical one-shot qualification
gates must not be rerun or regenerated.

## Qualification Summary

- Final release freeze completed successfully.
- Final staged integrity verification: PASS.
- Final integrity entry count: 37.
- Final attestation/install/verification exits: 0.
- Runtime/package-layout corrective validation completed successfully.
- Production files were not changed by the final freeze.
- Docker/tests/pytest were not rerun during the final freeze.
- Production authority remained OFF throughout qualification.

## Frozen Evidence

- `results/v120/FINAL-ATTESTATION.txt`
  - SHA-256: `5a1842a41c9ab9f68ad61f9ba2828ea7c63c03b411ae8cc05a40f0d283491beb`
- `results/v120/FINAL-INTEGRITY.sha256`
  - SHA-256: `412f9a8f0866c35eadedf16dbe49fb042f2d5fe0e4320abbb56d1cbcacbeade1`

The final release attestation was consumed exactly once.

## Runtime Corrective Result

The v1.2 qualification chain recorded and corrected a production Docker
package-layout import defect before the final freeze. The corrected validation
passed under the frozen release process.

Recorded runtime validation included:

- 35 OpenAPI operations after correction
- 6 routes
- 5 application-namespace modules
- 0 duplicate routes

## Release Semantics

`v1.2.0` is the completed standalone MeshCore baseline.

The following are deliberately separate from this release status:

- integration into later REVA/Odysseus versions
- production deployment authorization
- future MeshCore feature development

Future work should use a later MeshCore version and must not rewrite or rerun
the frozen v1.2.0 release evidence.

## Authority

`PRODUCTION_AUTHORITY=OFF`

The release freeze establishes evidence and reproducibility state; it does not
by itself grant production execution authority.
