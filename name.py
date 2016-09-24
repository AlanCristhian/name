"""A library with a base class that stores the assigned name of an object.

  >>> import name
  >>> a = name.AutoName()
  >>> a.__assigned_name__
  'a'
"""

import inspect


__all__ = ["AutoName"]


# Yields all locals variables in the higher (calling) frames
def _get_outer_locals(frame):
    while frame:
        yield frame.f_locals
        frame = frame.f_back


class AutoName:
    """ Creates an object with the '__assigned_name__'
    attribute that stores the name of such object.

    >>> import name
    >>> a = name.AutoName()
    >>> a.__assigned_name__
    'a'

    """
    def __init__(self, count=0):
        assert isinstance(count, int), \
               "Expected 'int' object, got '%s'" % count.__class__.__name__
        assert count >= 0, "Expected positive 'int' number, got '%r'" % count
        self.__count = count
        self.__name = None

    # I define the '__iter__' method to give compatibility
    # with the unpack sequence assignment syntax.
    def __iter__(self):
        # NOTE: I call 'type(self)' to warranty that this
        # method works even in a subclass of this.
        return (type(self)() for _ in range(self.__count))

    # Find the assigned name of the current object.
    def _find_name(self, frame):
        scope = _get_outer_locals(frame)
        # NOTE: The same object could have many names in differents scopes.
        # So, I stores all names in the 'scopes' var. The valid name is one
        # that is in the last scope.
        scopes = []
        for variables in scope:
            # NOTE: An object could have various names in the same scope. So,
            # I stores all in the 'names' var. This situation happen when user
            # assign the object to multiples variables with the "multiple
            # assignment syntax".
            names = []
            for name, value in variables.items():
                if value is self:
                    names.append(name)
            if names:
                scopes.append(names)
        if scopes:
            # Remember: the valid name is one that is in the last scope.
            names = scopes[-1]
            if len(names) > 1:  # Check for multiple assignment.
                raise NameError(
                    "Can not assign a unique name to multiple variables.")
            else:
                return names[0]
        raise NameError("Can not find the name of this object.")

    @property
    def __assigned_name__(self):
        """Find the name of the instance of the current class."""
        if self.__name is None:
            frame = inspect.currentframe().f_back
            self.__name = self._find_name(frame)
        return self.__name