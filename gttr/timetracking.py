from typing import Optional, Dict, Iterator, Tuple
from datetime import datetime
from dateutil.parser import parse


class TimeReport:
    def __init__(self) -> None:
        self.user_totals: Dict[str, int] = {}
        self.day_totals: Dict = {}

    def _parse_body(self, body: str) -> Optional[int]:
        """
        Return spent time in seconds
        """
        if body.startswith("added") and "of time spent" in body:
            timestr, _ = body.split("of time spent")
            timelist = timestr.split()[1:]
            spent_seconds = 0
            for ts in timelist:
                if ts.endswith('y'):
                    spent_seconds += int(ts[:-1]) * 31536000
                elif ts.endswith('w'):
                    spent_seconds += int(ts[:-1]) * 604800
                elif ts.endswith('d'):
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
        if username not in self.user_totals:
            self.user_totals[username] = 0
        self.user_totals[username] += spent_time

        created_at_date = created_at.date()
        if created_at_date not in self.day_totals:
            self.day_totals[created_at_date] = {}
        if username not in self.day_totals[created_at_date]:
            self.day_totals[created_at_date][username] = 0
        self.day_totals[created_at_date][username] += spent_time

    def _parse_created_at(self, created_at_str: str) -> datetime:
        return parse(created_at_str)

    def parse_note(self, username, body, created_at_str):
        spent_time = self._parse_body(body)
        created_at = self._parse_created_at(created_at_str)

        if spent_time:
            self._add_spent_time(username, created_at, spent_time)
    
    def total_report(self) -> Iterator[Tuple[str, int]]:
        for u, s in self.user_totals.items():
            yield (u, s)
