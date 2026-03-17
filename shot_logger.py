"""
Shot logger for cStrafe UI.

Logs every shot classification to a CSV file and tracks per-direction
statistics in memory. Press F7 to display a summary in the overlay.

Log files are saved in a ``logs/`` folder next to the application with
a timestamped filename so previous sessions are never overwritten.
"""

import csv
import os
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

from classifier import ShotClassification


@dataclass
class DirectionStats:
    """Running statistics for a single strafe direction."""
    total: int = 0
    counterstrafes: int = 0
    overlaps: int = 0
    bads: int = 0
    cs_times: List[float] = field(default_factory=list)
    shot_delays: List[float] = field(default_factory=list)
    overlap_times: List[float] = field(default_factory=list)

    def record(self, classification: ShotClassification) -> None:
        self.total += 1
        if classification.label == "Counter\u2011strafe":
            self.counterstrafes += 1
            if classification.cs_time is not None:
                self.cs_times.append(classification.cs_time)
            if classification.shot_delay is not None:
                self.shot_delays.append(classification.shot_delay)
        elif classification.label == "Overlap":
            self.overlaps += 1
            if classification.overlap_time is not None:
                self.overlap_times.append(classification.overlap_time)
        else:
            self.bads += 1

    @property
    def cs_rate(self) -> float:
        return (self.counterstrafes / self.total * 100) if self.total else 0.0

    @property
    def avg_cs_time(self) -> Optional[float]:
        return sum(self.cs_times) / len(self.cs_times) if self.cs_times else None

    @property
    def avg_shot_delay(self) -> Optional[float]:
        return sum(self.shot_delays) / len(self.shot_delays) if self.shot_delays else None

    @property
    def avg_overlap(self) -> Optional[float]:
        return sum(self.overlap_times) / len(self.overlap_times) if self.overlap_times else None


class ShotLogger:
    """Logs shots to CSV and maintains per-direction statistics."""

    def __init__(self) -> None:
        self._stats: Dict[str, DirectionStats] = defaultdict(DirectionStats)
        self._global = DirectionStats()
        self._log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
        os.makedirs(self._log_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self._log_path = os.path.join(self._log_dir, f"session_{timestamp}.csv")
        self._csv_file = open(self._log_path, "w", newline="", encoding="utf-8")
        self._writer = csv.writer(self._csv_file)
        self._writer.writerow([
            "timestamp", "direction", "classification",
            "cs_time_ms", "shot_delay_ms", "overlap_ms",
        ])
        self._csv_file.flush()

    def log(self, classification: ShotClassification) -> None:
        direction = classification.direction or "unknown"
        self._stats[direction].record(classification)
        self._global.record(classification)
        self._writer.writerow([
            datetime.now().strftime("%H:%M:%S.%f")[:-3],
            direction,
            classification.label,
            f"{classification.cs_time:.0f}" if classification.cs_time is not None else "",
            f"{classification.shot_delay:.0f}" if classification.shot_delay is not None else "",
            f"{classification.overlap_time:.0f}" if classification.overlap_time is not None else "",
        ])
        self._csv_file.flush()

    def get_summary(self) -> str:
        """Return a formatted summary string for the overlay."""
        if self._global.total == 0:
            return "No shots logged yet"

        lines = [f"Session: {self._global.total} shots"]
        lines.append(f"CS: {self._global.cs_rate:.0f}%  "
                      f"OL: {self._global.overlaps}  "
                      f"Bad: {self._global.bads}")
        lines.append("")

        # Sort directions: A→D and D→A first (horizontal), then vertical
        priority = {"A→D": 0, "D→A": 1, "W→S": 2, "S→W": 3}
        sorted_dirs = sorted(
            self._stats.keys(),
            key=lambda d: priority.get(d, 99),
        )

        for direction in sorted_dirs:
            stats = self._stats[direction]
            if stats.total == 0:
                continue
            line = f"{direction}: {stats.cs_rate:.0f}% CS ({stats.total})"
            details = []
            if stats.avg_cs_time is not None:
                details.append(f"avg {stats.avg_cs_time:.0f}ms")
            if stats.avg_overlap is not None:
                details.append(f"OL avg {stats.avg_overlap:.0f}ms")
            if details:
                line += f" [{', '.join(details)}]"
            lines.append(line)

        return "\n".join(lines)

    def close(self) -> None:
        if self._csv_file and not self._csv_file.closed:
            self._csv_file.close()
