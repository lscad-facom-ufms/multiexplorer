from typing import Optional, Dict
from Tkinter import Frame


class Presenter(object):
    def __init__(self):
        self.results = None  # type: Optional[Dict]

        self.frame = None  # type: Optional[Frame]

    def partial_presentation(self, frame, results):
        # type: (Frame, Dict) -> None
        raise NotImplementedError

    def final_presentation(self, frame, results):
        # type: (Frame, Dict) -> None
        raise NotImplementedError
