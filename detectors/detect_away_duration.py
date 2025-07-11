from datetime import datetime, timedelta

class AwayTracker:
    def __init__(self):
        self.away_start_time = None
        self.total_away_time = timedelta()
        self.away_periods = []

    def update(self, face_visible, timestamp):
        """Returns (start, end, duration) if person just returned, else None"""
        if not face_visible:
            if self.away_start_time is None:
                self.away_start_time = timestamp
        else:
            if self.away_start_time is not None:
                # just returned
                away_end_time = timestamp
                duration = away_end_time - self.away_start_time
                self.total_away_time += duration
                self.away_periods.append((self.away_start_time, away_end_time, duration))
                start, self.away_start_time = self.away_start_time, None
                return (start, away_end_time, duration)
        return None

    def finalize(self, current_time):
        """Call at end of video if still away"""
        if self.away_start_time is not None:
            duration = current_time - self.away_start_time
            self.total_away_time += duration
            self.away_periods.append((self.away_start_time, current_time, duration))

    def get_total_away_time(self):
        return self.total_away_time

    def get_away_periods(self):
        return self.away_periods
