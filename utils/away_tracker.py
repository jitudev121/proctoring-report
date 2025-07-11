from detectors.event_tracker import EventTracker

class AwayTracker:
    def __init__(self):
        self.event_tracker = EventTracker()

    def update(self, is_face_visible, timestamp):
        return self.event_tracker.update("away", not is_face_visible, timestamp)

    def finalize(self, final_time, logger):
        self.event_tracker.finalize(final_time, logger)

    def get_total_away_time(self):
        return sum(
            [e['duration'].total_seconds() for e in self.event_tracker.get_logged_events() if e['type'] == 'away']
        )

    def get_away_periods(self):
        return [(e['start'], e['end'], e['duration']) for e in self.event_tracker.get_logged_events() if e['type'] == 'away']
