from __future__ import annotations

from dataclasses import dataclass
from statistics import mean

from meshcore_demo.coordinator import (
    build_demo_coordinator,
)
from meshcore_demo.mirror_demo import (
    Mirror,
    MirrorObservation,
)


@dataclass(frozen=True, slots=True)
class MatchedOutcome:
    name: str
    observation: MirrorObservation
    action_ms: float
    control_ms: float


def main() -> None:
    coordinator = build_demo_coordinator()
    mirror = Mirror()

    source = "request-a"

    samples = (
        MatchedOutcome(
            name="low-load",
            observation=MirrorObservation(
                recent_latency_ms=4.0,
                queue_pressure=0.10,
                cache_hot=True,
            ),
            action_ms=8.0,
            control_ms=11.0,
        ),
        MatchedOutcome(
            name="mixed-load",
            observation=MirrorObservation(
                recent_latency_ms=25.0,
                queue_pressure=0.55,
                cache_hot=False,
            ),
            action_ms=10.0,
            control_ms=10.5,
        ),
        MatchedOutcome(
            name="high-load-a",
            observation=MirrorObservation(
                recent_latency_ms=85.0,
                queue_pressure=0.92,
                cache_hot=False,
            ),
            action_ms=16.0,
            control_ms=11.0,
        ),
        MatchedOutcome(
            name="high-load-b",
            observation=MirrorObservation(
                recent_latency_ms=72.0,
                queue_pressure=0.88,
                cache_hot=False,
            ),
            action_ms=14.0,
            control_ms=10.0,
        ),
    )

    deltas = []

    print(
        "MeshCore Synthetic Counterfactual Demo"
    )
    print(
        "======================================"
    )

    for sample in samples:
        decision = coordinator.decide(
            source
        )

        assessment = mirror.assess(
            decision,
            sample.observation,
        )

        would_veto = (
            decision.action_allowed
            and
            assessment.classification
            ==
            "harmful"
        )

        counterfactual_ms = (
            sample.control_ms
            if would_veto
            else sample.action_ms
        )

        delta = (
            sample.action_ms
            -
            counterfactual_ms
        )

        deltas.append(
            delta
        )

        print()
        print(
            "scenario:",
            sample.name,
        )
        print(
            "Mirror:",
            assessment.classification,
        )
        print(
            "action_ms:",
            sample.action_ms,
        )
        print(
            "control_ms:",
            sample.control_ms,
        )
        print(
            "would_veto:",
            would_veto,
        )
        print(
            "counterfactual_ms:",
            counterfactual_ms,
        )
        print(
            "saved_ms:",
            round(
                delta,
                3,
            ),
        )

    print()
    print(
        "SUMMARY"
    )
    print(
        "======="
    )

    print(
        "mean saved_ms:",
        round(
            mean(
                deltas
            ),
            3,
        ),
    )

    print()
    print(
        "NOTE:"
    )
    print(
        "These are synthetic demonstration values."
    )
    print(
        "They are not MeshCore research benchmark results."
    )


if __name__ == "__main__":
    main()
