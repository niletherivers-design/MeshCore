# MeshCore

**Experimental Adaptive Storage Architecture**

MeshCore is an experimental systems research project exploring hierarchical
data organization, predictive relationships, bounded runtime adaptation,
and asynchronous contextual evaluation.

The architecture separates physical storage planning, predictive
relationships, direct local experience, and experimental contextual
evaluation so that adaptive components can be measured without silently
changing the underlying storage authority.

## Architecture

MeshCore currently explores three primary axes:

- **Vertical** — hierarchical physical storage and retrieval planning.
- **Horizontal** — predictive relationships and transition modeling.
- **Depth** — direct local experience and bounded action gating.

An experimental **Mirror** layer operates asynchronously as a contextual
second-opinion system. It classifies observed situations as beneficial,
harmful, or uncertain.

The Mirror is currently shadow-only research infrastructure and does not
control production actions.

## Research Methodology

The project emphasizes:

- reproducible experiments
- explicit authority boundaries
- frozen experimental artifacts
- causal ACTION/CONTROL comparisons
- preservation of negative and inconclusive results
- parity testing
- bounded asynchronous processing
- fail-soft background components

## Repository Structure

    MeshCore/
    ├── benchmarks/
    ├── docs/
    │   ├── architecture.md
    │   └── methodology.md
    ├── results/
    │   └── published-summary.md
    ├── src/
    │   └── meshcore_demo/
    ├── .gitignore
    ├── README.md
    └── requirements.txt

## Project Status

MeshCore is an active research prototype.

This public repository contains sanitized demonstrations, architecture
documentation, and selected experimental results rather than the complete
internal research environment.

## Author

**Nile**

Independent systems researcher and developer.

## Running the Public Demo

Create a virtual environment:

    python3 -m venv .venv
    source .venv/bin/activate

Install development dependencies:

    python -m pip install -r requirements-dev.txt

Run the coordinator demo:

    PYTHONPATH=src python -m meshcore_demo.coordinator

Run the Mirror demo:

    PYTHONPATH=src python -m meshcore_demo.mirror_demo

Run the tests:

    PYTHONPATH=src pytest -q

The authority tests verify that the advisory Mirror layer does not modify
the base MeshCore coordinator decision.
