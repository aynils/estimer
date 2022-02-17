from functools import wraps
from time import time


def function_timer(f, threshold=0.1):
    @wraps(f)
    def wrap(*args, **kw):
        time_start = time()
        result = f(*args, **kw)
        time_end = time()
        duration = time_end - time_start
        if duration >= threshold:
            print(f"⚠️func:{f.__name__} took: {duration} sec")
        else:
            print(f"✅func:{f.__name__} took: {duration} sec")
        return result

    return wrap


class Timer:
    def __init__(self):
        self.init_time = time()
        self.result = {}

    def start(self, key: str):
        try:
            self.result[key]["start"] = time()
        except KeyError:
            self.result[key] = {}
            self.result[key]["start"] = time()

    def stop(self, key: str):
        try:
            self.result[key]["stop"] = time()
            self.result[key]["duration"] = self.result[key]["stop"] - self.result[key]["start"]
        except KeyError:
            print(f"Key {key} must be started before stopped.")

    def pause(self, key: str):
        try:
            self.result[key]["pause"] = time()
            previous_duration = self.result[key].get("duration", 0)
            self.result[key]["duration"] = previous_duration + self.result[key]["pause"] - self.result[key]["start"]
        except KeyError:
            print(f"Key {key} must be started before paused.")

    def get_result(self):
        return self.result

    def print(self):
        for key in self.result:
            duration = self.result[key].get("duration", "❌ not stopped")
            print(f"{key} took: {duration} sec")
