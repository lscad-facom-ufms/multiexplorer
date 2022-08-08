from typing import Callable, Any


class Event:
    def __init__(self):
        pass

    FLOW_EXECUTION_STARTED = "flow_execution_started"

    FLOW_EXECUTION_ENDED = "flow_execution_ended"

    FLOW_EXECUTION_FAILED = "flow_execution_failed"

    STEP_EXECUTION_STARTED = "step_execution_started"

    STEP_EXECUTION_ENDED = "step_execution_ended"

    STEP_EXECUTION_FAILED = "step_execution_failed"


class EventFirer(object):
    """
    Extending this class allows some sort simple communication between objects in the form of event firing and handling.

    It's intended to be used as a means to allow GUI related objects react to the behavior of the objects responsible
    for execution (ExecutionFlow, Step, etc.)

    Valid event names should be defined as static properties in the "Event" class or in the extending class.

    The proper value of "events" should be defined, in the initialization method of the extending class
    as a dictionary where the keys are valid event names and the values are lists/arrays of handler function names.

    It's important to align the handling functions signatures with the arguments used when firing the events.
    """

    def __init__(self):
        self.events = {}

    def add_handler(self, event_name, callback_fn):
        # type: (str, Callable) -> None
        """
        Add an event handler
        """
        if event_name not in self.events:
            self.events[event_name] = []

        if callback_fn not in self.events[event_name]:
            self.events[event_name].append(callback_fn)

    def remove_handler(self, event_name, callback_fn):
        # type: (str, Callable) -> None
        """
        Remove an event handler
        """
        self.events[event_name].remove(callback_fn)

    def fire(self, event_name, *args):
        # type: (str, Any) -> None
        """
        Fires an event, i.e., evokes it's handlers.
        """
        for callback_fn in self.events[event_name]:
            callback_fn(*args)
