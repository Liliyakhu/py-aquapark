from __future__ import annotations
from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(
            self,
            owner: ChildrenSlideLimitationValidator
            | AdultSlideLimitationValidator,
            name: str
    ) -> None:
        self.protected_name = "_" + name

    def __get__(
            self,
            instance: ChildrenSlideLimitationValidator
            | AdultSlideLimitationValidator,
            owner: ChildrenSlideLimitationValidator
            | AdultSlideLimitationValidator
    ) -> int:
        return getattr(instance, self.protected_name)

    def __set__(
            self,
            instance: ChildrenSlideLimitationValidator
            | AdultSlideLimitationValidator,
            value: int | str
    ) -> None:
        if self.min_amount <= value <= self.max_amount:
            setattr(instance, self.protected_name, value)
            return
        raise ValueError(self.protected_name)


class Visitor:
    def __init__(self, name: str, age: int, height: int, weight: int) -> None:
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, height: int, weight: int) -> None:
        self.age = age
        self.height = height
        self.weight = weight


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class:
            callable(
                [ChildrenSlideLimitationValidator
                 | AdultSlideLimitationValidator]
            )
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, instance: Visitor) -> bool:
        try:
            self.limitation_class(
                instance.age,
                instance.height,
                instance.weight
            )
        except ValueError:
            return False
        return True
