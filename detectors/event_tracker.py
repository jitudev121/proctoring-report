from datetime import datetime

class EventTracker:
    def __init__(self, event_name):
        self.event_name = event_name
        self.active = False
        self.start_time = None

    def update(self, condition, current_time, logger):
        if condition and not self.active:
            # Event started
            self.active = True
            self.start_time = current_time
        elif not condition and self.active:
            # Event ended
            self.active = False
            end_time = current_time
            duration = end_time - self.start_time
            logger.warning(f"{self.event_name} started at [{self.format_time(self.start_time)}] and ended at [{self.format_time(end_time)}] (Duration: {self.format_duration(duration)})")

    def finalize(self, logger, final_time):
        """Close the event at the end if still active"""
        if self.active:
            duration = final_time - self.start_time
            logger.warning(f"{self.event_name} started at [{self.format_time(self.start_time)}] and ended at [{self.format_time(final_time)}] (Duration: {self.format_duration(duration)})")

    def format_time(self, seconds):
        return datetime.utcfromtimestamp(seconds).strftime('%H:%M:%S')

    def format_duration(self, duration):
        mins, secs = divmod(int(duration), 60)
        return f"{mins}m {secs}s"
