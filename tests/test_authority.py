from meshcore_demo.coordinator import (
    build_demo_coordinator,
)

from meshcore_demo.mirror_demo import (
    Mirror,
    MirrorObservation,
)


def test_mirror_does_not_change_base_decision():
    coordinator = (
        build_demo_coordinator()
    )

    mirror = Mirror()

    before = coordinator.decide(
        "request-a"
    )

    assessment = mirror.assess(
        before,
        MirrorObservation(
            recent_latency_ms=85.0,
            queue_pressure=0.92,
            cache_hot=False,
        ),
    )

    after = coordinator.decide(
        "request-a"
    )

    assert assessment.classification == "harmful"

    assert before == after

    assert before.action_allowed is True


def test_depth_retains_authority():
    coordinator = (
        build_demo_coordinator()
    )

    decision = coordinator.decide(
        "request-c"
    )

    assert decision.action_allowed is False
    assert decision.reason == "depth-veto"


def test_low_confidence_remains_blocked():
    coordinator = (
        build_demo_coordinator()
    )

    decision = coordinator.decide(
        "request-b"
    )

    assert decision.action_allowed is False

    assert (
        decision.reason
        ==
        "below-confidence-threshold"
    )
