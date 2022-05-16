from time import time


class ViewsCounter:
    def __init__(self):
        self._day_views = 0
        self._day_views_step = 60 * 60 * 24 # 1 day
        self._day_next_time = int(time()) + self._day_views_step


    def get_day_views(self) -> int:
        if time() < self._day_next_time:
            return self._day_views
        self._day_views = 0
        self._day_next_time += self._day_views_step
        return 0 

    def increment_day_views(self) -> None:
        if time() < self._day_next_time:
            self._day_views += 1
        else:
            self._day_views = 1
            self._day_next_time += self._day_views_step