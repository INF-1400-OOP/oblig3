class EventDispatcher:
    """ Event dispatcher class - greatly inspired by the lecture notes, but with some artistic twists. 
    
    Usage:
    
    # Inside a loop having some type of pygame-events we can register custom handlers with their methods to do things when a already registered event arise.
    # Should be used in combination with EventHandler objects.

    Example:
    my_dispatcher = EventDispatcher()
    my_event_handler = EventHandler(pygame.SOMEEVENT)
    my_event_handler.handler = my_custom_handler_function
    my_dispatcher.register_handler(my_event_handler)

    for event in pygame.event.get():
        my_dispatcher.dispatch(event)
    """
    def __init__(self) -> None:
        self.__handlers = {}

    def register_handler(self, event_handler) -> None:
        """ Register new handlers.
        Args:
            event_handler: EventHandler
                Method only accepts argument of type <class, EventHandler>.
        """

        # check for correct argument type
        if not isinstance(event_handler, EventHandler):
            raise TypeError(f"Inappropriate arguement {event_handler}, must be of type: {EventHandler}.")
        
        # Ensure no duplicates of handlers
        elif event_handler.type in self.__handlers:
            raise DuplicateHandlerError(event_handler)

        # add handler to handlers
        self.__handlers[event_handler.type] = event_handler.handler

    def dispatch(self, event) -> None:
        """ Dispatches event handler. """
        if event.type in self.__handlers:
            self.__handlers[event.type](event)

class EventHandler:
    """ Event handler - Create a custom event. Also inspired from lecture notes. 
    Usage:
    See docstring of EventDispatcher for in-depth usage and example.

    Example:
    my_event_handler = EventHandler(pygame.SOMEEVENT)
    my_event_handler.handler = my_custom_handler_function
    """
    def __init__(self, event_type):
        self._type = event_type
        self._handler = None

    # getters and setters
    @property
    def type(self):
        return self._type
    
    @property
    def handler(self):
        return self._handler

    @type.setter
    def type(self, event_type):
        self._type = event_type

    @handler.setter
    def handler(self, handler):
        self._handler = handler

    def add_to_dispatcher(self, dispatcher):
        """ Does the same as EventDispatcher.register_handler(). """
        dispatcher.register_handler(self)

    def __str__(self):
        return f"Event handler for type {self.type} with handler {self.handler}"

class DuplicateHandlerError(Exception):
    """ Raised if a duplicate of a event handler is detected """
    def __init__(self, event_handler, message="Duplicate of an event handler detected."):
        self._event_handler = event_handler
        self._message = message
        super().__init__(self._message)

    @property
    def message(self):
        return self._message

    @property
    def event_handler(self):
        return self._event_handler

    @message.setter
    def message(self, message):
        self._message = message

    def __str__(self) -> str:
        return f"{self.event_handler} -> {self.message}"

if __name__ == "__main__":
    
    def my_handler(event):
        print(f"{event = }")
        return 

    dispatcher = EventDispatcher()
    e1 = EventHandler("button")
    print(e1.type)
    print(e1.handler)
    print(e1)
    e1.handler = my_handler
    print(e1.type)
    print(e1.handler)
    print(e1)
    e1.add_to_dispatcher(dispatcher)
    c = "abc"
    # dispatcher.register_handler(c)
    dispatcher.register_handler(e1)
