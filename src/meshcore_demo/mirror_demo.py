from __future__ import annotations

from dataclasses import dataclass

from meshcore_demo.coordinator import (
    Decision,
    build_demo_coordinator,
)


@dataclass(frozen=True, slots=True)
class MirrorObservation:
    """
    Simplified runtime context visible to the public Mirror demo.

    These values are synthetic demonstration inputs, not measurements
    from the private MeshCore research environment.
    """

    recent_latency_ms: float
    queue_pressure: float
    cache_hot: bool


@dataclass(frozen=True, slots=True)
class MirrorAssessment:
    classification: str
    score: float
    reason: str


class Mirror:
    """
    Advisory-only contextual observer.

    The Mirror receives a completed coordinator decision plus runtime
    context and produces a second opinion.

    It does NOT alter:
      - the prediction
      - the physical plan
      - the Depth decision
      - action_allowed
    """

    def assess(
        self,
        decision: Decision,
        observation: MirrorObservation,
    ) -> MirrorAssessment:
        if not decision.action_allowed:
            return MirrorAssessment(
                classification="uncertain",
                score=0.0,
                reason="base-action-not-allowed",
            )

        risk = 0.0

        if observation.recent_latency_ms >= 40.0:
            risk += 0.45

        if observation.queue_pressure >= 0.75:
            risk += 0.40

        if not observation.cache_hot:
            risk += 0.20

        if risk >= 0.70:
            return MirrorAssessment(
                classification="harmful",
                score=min(risk, 1.0),
                reason="high-runtime-pressure",
            )

        if risk < 0.20:
            return MirrorAssessment(
                classification="beneficial",
                score=1.0 - risk,
                reason="favorable-runtime-state",
            )

        return MirrorAssessment(
            classification="uncertain",
            score=1.0 - abs(
                0.50 - risk
            ),
            reason="mixed-runtime-state",
        )


def demonstrate() -> None:
    coordinator = (
        build_demo_coordinator()
    )

    mirror = Mirror()

    scenarios = (
        (
            "low-load",
            MirrorObservation(
                recent_latency_ms=4.0,
                queue_pressure=0.10,
                cache_hot=True,
            ),
        ),
        (
            "mixed-load",
            MirrorObservation(
                recent_latency_ms=25.0,
                queue_pressure=0.55,
                cache_hot=False,
            ),
        ),
        (
            "high-load",
            MirrorObservation(
                recent_latency_ms=85.0,
                queue_pressure=0.92,
                cache_hot=False,
            ),
        ),
    )

    source = "request-a"

    for name, observation in scenarios:
        decision_before = (
            coordinator.decide(
                source
            )
        )

        assessment = mirror.assess(
            decision_before,
            observation,
        )

        decision_after = (
            coordinator.decide(
                source
            )
        )

        unchanged = (
            decision_before
            ==
            decision_after
        )

        print()
        print(
            f"scenario: {name}"
        )
        print(
            "base allowed:",
            decision_before.action_allowed,
        )
        print(
            "base reason:",
            decision_before.reason,
        )
        print(
            "Mirror:",
            assessment.classification,
        )
        print(
            "Mirror score:",
            round(
                assessment.score,
                3,
            ),
        )
        print(
            "Mirror reason:",
            assessment.reason,
        )
        print(
            "base decision unchanged:",
            unchanged,
        )


if __name__ == "__main__":
    demonstrate()
