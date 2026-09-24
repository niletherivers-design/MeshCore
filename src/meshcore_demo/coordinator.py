from __future__ import annotations

from dataclasses import dataclass

from meshcore_demo.hierarchy import (
    Hierarchy,
    PhysicalPlan,
    build_demo_hierarchy,
)


@dataclass(frozen=True, slots=True)
class Prediction:
    target: str
    probability: float


@dataclass(frozen=True, slots=True)
class Decision:
    source: str
    predicted_target: str | None
    probability: float
    physical_plan: PhysicalPlan | None
    action_allowed: bool
    reason: str


class Predictor:
    """
    Simplified Horizontal axis.

    Horizontal predicts relationships.
    It does not own physical storage or action authority.
    """

    def __init__(
        self,
        transitions: dict[str, Prediction],
    ) -> None:
        self._transitions = dict(
            transitions
        )

    def predict(
        self,
        source: str,
    ) -> Prediction | None:
        return self._transitions.get(
            source
        )


class DepthGate:
    """
    Simplified Depth axis.

    Depth represents direct local experience and may veto an
    otherwise-valid optional action.
    """

    def __init__(
        self,
        vetoes: set[
            tuple[str, str]
        ] | None = None,
    ) -> None:
        self._vetoes = set(
            vetoes or ()
        )

    def vetoes(
        self,
        source: str,
        target: str,
    ) -> bool:
        return (
            source,
            target,
        ) in self._vetoes


class MeshCoordinator:
    """
    Coordinates the three axes without merging their authority.

    Horizontal:
        predicts a target.

    Vertical:
        resolves a physical plan.

    Depth:
        may veto an optional action.

    The coordinator itself owns no learned state.
    """

    def __init__(
        self,
        *,
        hierarchy: Hierarchy,
        predictor: Predictor,
        depth: DepthGate,
        action_threshold: float = 0.80,
    ) -> None:
        self.hierarchy = hierarchy
        self.predictor = predictor
        self.depth = depth
        self.action_threshold = float(
            action_threshold
        )

    def decide(
        self,
        source: str,
    ) -> Decision:
        prediction = (
            self.predictor.predict(
                source
            )
        )

        if prediction is None:
            return Decision(
                source=source,
                predicted_target=None,
                probability=0.0,
                physical_plan=None,
                action_allowed=False,
                reason="no-prediction",
            )

        plan = (
            self.hierarchy.resolve(
                prediction.target
            )
        )

        if (
            prediction.probability
            <
            self.action_threshold
        ):
            return Decision(
                source=source,
                predicted_target=
                    prediction.target,
                probability=
                    prediction.probability,
                physical_plan=plan,
                action_allowed=False,
                reason=
                    "below-confidence-threshold",
            )

        if plan is None:
            return Decision(
                source=source,
                predicted_target=
                    prediction.target,
                probability=
                    prediction.probability,
                physical_plan=None,
                action_allowed=False,
                reason="no-physical-plan",
            )

        if self.depth.vetoes(
            source,
            prediction.target,
        ):
            return Decision(
                source=source,
                predicted_target=
                    prediction.target,
                probability=
                    prediction.probability,
                physical_plan=plan,
                action_allowed=False,
                reason="depth-veto",
            )

        return Decision(
            source=source,
            predicted_target=
                prediction.target,
            probability=
                prediction.probability,
            physical_plan=plan,
            action_allowed=True,
            reason="allow",
        )


def build_demo_coordinator(
) -> MeshCoordinator:
    hierarchy = (
        build_demo_hierarchy()
    )

    predictor = Predictor(
        {
            "request-a": Prediction(
                target="object-a",
                probability=0.93,
            ),
            "request-b": Prediction(
                target="object-b",
                probability=0.72,
            ),
            "request-c": Prediction(
                target="object-c",
                probability=0.91,
            ),
        }
    )

    depth = DepthGate(
        {
            (
                "request-c",
                "object-c",
            ),
        }
    )

    return MeshCoordinator(
        hierarchy=hierarchy,
        predictor=predictor,
        depth=depth,
        action_threshold=0.80,
    )


if __name__ == "__main__":
    coordinator = (
        build_demo_coordinator()
    )

    for source in (
        "request-a",
        "request-b",
        "request-c",
        "unknown-request",
    ):
        decision = (
            coordinator.decide(
                source
            )
        )

        print()
        print(
            f"source: {source}"
        )
        print(
            "target:",
            decision.predicted_target,
        )
        print(
            "probability:",
            decision.probability,
        )
        print(
            "plan:",
            decision.physical_plan,
        )
        print(
            "allowed:",
            decision.action_allowed,
        )
        print(
            "reason:",
            decision.reason,
        )
