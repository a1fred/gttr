from typing import Optional, Dict, Iterator, Tuple
from datetime import datetime
from dateutil.parser import parse


class TimeReport:
    def __init__(self) -> None:
        self.data: Dict[str, int] = {}

    def _parse_body(self, body: str) -> Optional[int]:
        """
        Return spent time in seconds
        """
        if body.startswith("added") and body.endswith("of time spent"):
            timelist = body.split()[1:-3]
            spent_seconds = 0
            for ts in timelist:
                if ts.endswith('d'):
                    spent_seconds += int(ts[:-1]) * 86400
                elif ts.endswith('h'):
                    spent_seconds += int(ts[:-1]) * 3600
                elif ts.endswith('m'):
                    spent_seconds += int(ts[:-1]) * 60
                elif ts.endswith('s'):
                    spent_seconds += int(ts[:-1])
                else:
                    raise ValueError(ts)

            return spent_seconds
        else:
            return None
    
    def _add_spent_time(self, username, created_at, spent_time):
        if username not in self.data:
            self.data[username] = 0

        self.data[username] += spent_time

    def _parse_created_at(self, created_at_str: str) -> datetime:
        return parse(created_at_str)

    def parse_note(self, username, body, created_at_str):
        spent_time = self._parse_body(body)
        created_at = self._parse_created_at(created_at_str)

        if spent_time:
            self._add_spent_time(username, created_at, spent_time)
    
    def total_report(self) -> Iterator[Tuple[str, int]]:
        for u, s in self.data.items():
            yield (u, s)
