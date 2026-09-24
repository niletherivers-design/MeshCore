from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PhysicalPlan:
    """
    Simplified physical retrieval plan.

    The real MeshCore research system uses a more detailed hierarchical
    storage representation. This public demo intentionally exposes only
    the architectural idea.
    """

    target: str
    path: tuple[str, ...]


class Hierarchy:
    """
    Small demonstration of the MeshCore Vertical axis.

    Vertical owns physical organization and retrieval planning.
    It does not make predictions and does not decide whether an
    optional action should execute.
    """

    def __init__(
        self,
        locations: dict[str, tuple[str, ...]],
    ) -> None:
        self._locations = dict(locations)

    def resolve(
        self,
        target: str,
    ) -> PhysicalPlan | None:
        path = self._locations.get(target)

        if path is None:
            return None

        return PhysicalPlan(
            target=target,
            path=path,
        )


def build_demo_hierarchy() -> Hierarchy:
    return Hierarchy(
        {
            "object-a": (
                "pack-01",
                "macro-00",
                "micro-03",
            ),
            "object-b": (
                "pack-01",
                "macro-02",
                "micro-11",
            ),
            "object-c": (
                "pack-04",
                "macro-01",
                "micro-07",
            ),
        }
    )


if __name__ == "__main__":
    hierarchy = build_demo_hierarchy()

    for target in (
        "object-a",
        "object-b",
        "missing-object",
    ):
        print(
            target,
            "->",
            hierarchy.resolve(target),
        )
