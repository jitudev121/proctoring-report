from datetime import datetime

class EventTracker:
    def __init__(self, event_name):
        self.event_name = event_name
        self.active = False
        self.start_time = None
        self.stored_info = ""  # <-- Store extra info

    def update(self, condition, current_time, logger, extra_info=""):
        if condition and not self.active:
            # Event just started
            self.active = True
            self.start_time = current_time
            self.stored_info = extra_info  # store info at start
        elif not condition and self.active:
            # Event just ended
            self.active = False
            end_time = current_time
            duration = end_time - self.start_time
            message = f"{self.event_name} started at [{self.format_time(self.start_time)}] and ended at [{self.format_time(end_time)}] (Duration: {self.format_duration(duration)})"
            if self.stored_info:
                message += f" | {self.stored_info}"
            logger.warning(message)
            self.stored_info = ""  # Clear after logging

    def finalize(self, logger, final_time):
        if self.active:
            duration = final_time - self.start_time
            message = f"{self.event_name} started at [{self.format_time(self.start_time)}] and ended at [{self.format_time(final_time)}] (Duration: {self.format_duration(duration)})"
            if self.stored_info:
                message += f" | {self.stored_info}"
            logger.warning(message)
            self.stored_info = ""

    def format_time(self, seconds):
        return datetime.utcfromtimestamp(seconds).strftime('%H:%M:%S')

    def format_duration(self, duration):
        mins, secs = divmod(int(duration), 60)
        return f"{mins}m {secs}s"
