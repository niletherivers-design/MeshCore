from meshcore_demo.coordinator import (
    build_demo_coordinator,
)
from meshcore_demo.mirror_demo import (
    Mirror,
    MirrorObservation,
)


def test_harmful_mirror_can_model_counterfactual_veto():
    coordinator = build_demo_coordinator()
    mirror = Mirror()

    decision = coordinator.decide(
        "request-a"
    )

    assessment = mirror.assess(
        decision,
        MirrorObservation(
            recent_latency_ms=85.0,
            queue_pressure=0.92,
            cache_hot=False,
        ),
    )

    action_ms = 16.0
    control_ms = 11.0

    would_veto = (
        decision.action_allowed
        and assessment.classification
        == "harmful"
    )

    counterfactual_ms = (
        control_ms
        if would_veto
        else action_ms
    )

    saved_ms = (
        action_ms
        -
        counterfactual_ms
    )

    assert decision.action_allowed is True
    assert assessment.classification == "harmful"
    assert would_veto is True
    assert counterfactual_ms == 11.0
    assert saved_ms == 5.0
