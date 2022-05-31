class Event:
    EXECUTION_STARTED = "execution_started"

    EXECUTION_ENDED = "execution_ended"


class EventFirer:
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
        """
        Add an event handler
        """
        self.events[event_name].append(callback_fn)

    def remove_handler(self, event_name, callback_fn):
        """
        Remove an event handler
        """
        self.events[event_name].remove(callback_fn)

    def fire(self, event_name, *args):
        """
        Fires an event, i.e., evokes it's handlers.
        """
        for callback_fn in self.events[event_name]:
            callback_fn(*args)
