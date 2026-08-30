"""Small teaching-oriented metrics helpers."""

from dataclasses import dataclass


@dataclass(frozen=True)
class BinaryCounts:
    tp: int
    fp: int
    tn: int
    fn: int

    @property
    def detection_rate(self) -> float:
        denom = self.tp + self.fn
        return self.tp / denom if denom else float("nan")

    @property
    def false_alarm_rate(self) -> float:
        denom = self.fp + self.tn
        return self.fp / denom if denom else float("nan")
