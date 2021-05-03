"""Module for base classes in the core module."""
# !/usr/bin/python -tt
# -*- coding: utf-8 -*-
# =============================================================================
# File      : classes.py -- Base classes for pathpy
# Author    : Jürgen Hackl <hackl@ifi.uzh.ch>
# Time-stamp: <Sat 2021-05-01 17:55 juergen>
#
# Copyright (c) 2016-2021 Pathpy Developers
# =============================================================================
from typing import Any, Optional
from copy import deepcopy
from collections.abc import MutableMapping
from singledispatchmethod import singledispatchmethod  # NOTE: not needed at 3.9

from pathpy import logger

# create logger for the Path class
LOG = logger(__name__)


class PathPyObject:
    """Base class for all pathpy core objects."""

    def __init__(self, uid: Optional[str] = None, **kwargs: Any) -> None:
        """Initialize the base class."""

        # declare variable
        self._uid: str
        self._is_python_uid: bool
        self.attributes: Any

        # assign node identifier
        if uid is not None:
            self._uid = str(uid)
            self._is_python_uid = False
        else:
            self._uid = hex(id(self))
            self._is_python_uid = True

        # update attributes
        self.attributes = kwargs

    def __setitem__(self, key: Any, value: Any) -> None:
        """Add a specific attribute to the object.

        An attribute has a key and the corresponding value expressed as a pair,
        key: value.

        Parameters
        ----------
        key: Any
            Unique identifier for a corrisponding value.

        value: Any
            A value i.e. attribute which is associated with the object.

        Examples
        --------

        Generate new node.

        >>> from pathpy import Node
        >>> u = Node('u')

        Add atribute to the node.

        >>> u['color'] = 'blue'

        """

        self.attributes[key] = value

    def __getitem__(self, key: Any) -> Any:
        """Returns a specific attribute of the object.

        Parameters
        ----------
        key: any
            Key value for the attribute of the object.

        Returns
        -------
        any
            Returns the attribute of the node associated with the given key
            value.

        Raises
        ------
        KeyError
            If no attribute with the assiciated key is defined.

        Examples
        --------

        Generate new node with blue color

        >>> from pathpy import Node
        >>> u = Node('u', color='blue')

        Get the node attribute.

        >>> u['color']
        'blue'

        """
        return self.attributes.get(key, None)

    def __repr__(self) -> str:
        """Return the description of the object.

        Returns
        -------
        str

            Returns the description of the object with the class and assigned
            node uid.

        Examples
        --------
        Genarate new node.

        >>> from pathpy import Node
        >>> u = Node('u')
        >>> print(u)
        Node u

        """
        # declare variable
        string: str

        # check if python id is used as uid or not
        if self._is_python_uid:
            # if python id is used dont show in the object description
            string = super().__repr__()
        else:
            # if user uid is used show in the object description
            string = '{} {}'.format(self.__class__.__name__, self.uid)

        return string

    @property
    def uid(self) -> str:
        """Return the unique identifier (uid) of the object.

        Returns
        -------
        str

            Return the node identifier (uid) as a string.

        Examples
        --------
        Generate a single node and print the uid.

        >>> from pathpy import Node
        >>> u = Node('u')
        >>> u.uid
        u

        """
        return self._uid

    def update(self, **kwargs: Any) -> None:
        """Update the attributes of the object.

        Parameters
        ----------
        kwargs : Any
            Attributes to add or update for the object as key=value pairs.

        Examples
        --------

        Generate simple node with attribute.

        >>> from pathpy import Node
        >>> u = Node('u',color='red')
        >>> u.attributes
        {'color': 'red'}

        Update attributes.

        >>> u.update(color='green',shape='rectangle')
        >>> u.attributes
        {'color': 'green', 'shape': 'rectangle'}

        """

        self.attributes.update(**kwargs)

    def copy(self):
        """Return a copy of the node.

        Returns
        -------
        :py:class:`Node`
            A copy of the node.

        Examples
        --------
        >>> from pathpy import Node
        >>> u = Node('u')
        >>> v = u.copy()
        >>> v.uid
        u
        """
        return deepcopy(self)

    def weight(self, weight: str = 'weight', default: float = 1.0) -> float:
        """Returns the weight of the object.

        Per default the attribute with the key 'weight' is used as
        weight. Should there be no such attribute, a new one will be crated
        with weight = 1.0.

        If an other attribute should be used as weight, the option weight has
        to be changed.

        If a weight is assigned but for calculation a weight of 1.0 is needed,
        the weight can be disabled with False or None.

        Parameters
        ----------
        weight : str, optional (default = 'weight')
            The weight parameter defines which attribute is used as weight. Per
            default the attribute 'weight' is used. If `None` or `False` is
            chosen, the weight will be 1.0. Also any other attribute of the
            edge can be used as a weight

        Returns
        -------
        float
            Returns the attribute value associated with the keyword.

        Examples
        --------

        Create new edge and get the weight.

        >>> form pathpy import Edge
        >>> vw = Edge('v','w')
        >>> vw.weight()
        1.0

        Change the weight.

        >>> vw['weight'] = 4
        >>> vw.weight()
        4.0

        >>> vw.weight(False)
        1.0

        Add an attribute and use this as weight.

        >>> vw['length'] = 5
        >>> vw.weight('length')
        5.0

        Create new path and get the weight.

        >>> form pathpy import Path
        >>> p = Path('a','b','c')
        >>> p.weight()
        1.0

        Change the weight.

        >>> p['weight'] = 4
        >>> p.weight()
        4.0

        >>> p.weight(False)
        1.0

        Add an attribute and use this as weight.

        >>> p['length'] = 5
        >>> p.weight('length')
        5.0

        """
        value: float
        weight = False if weight is None else weight

        if not weight:
            value = default
        elif isinstance(weight, str) and weight != 'weight':
            value = float(self.attributes.get(weight, 0.0))
        else:
            value = float(self.attributes.get('weight', default))
        return value


class PathPyCollection(MutableMapping):
    """Base collection for PathPyObjects"""

    def __init__(self, *args, **kwargs) -> None:

        # dict to store the PathPyObjects {uid:PathPyObject}
        self._store: dict = dict()

        # use the free update to set keys
        self.update(dict(*args, **kwargs))

    @singledispatchmethod
    def __getitem__(self, key):
        return None

    @__getitem__.register(str)  # type: ignore
    def _(self, key):
        return self._store[key]

    @__getitem__.register(PathPyObject)  # type: ignore
    def _(self, key):
        return self._store[key.uid]

    def __setitem__(self, key, value):
        self._store[key] = value

    def __delitem__(self, key):
        del self._store[key]

    def __iter__(self):
        return iter(self._store)

    def __len__(self):
        return len(self._store)

    def __repr__(self):
        return self._store.__repr__()

    @singledispatchmethod
    def __contains__(self, item) -> bool:
        """Returns if item is in edges."""
        return False

    @__contains__.register(PathPyObject)  # type: ignore
    def _(self, item: PathPyObject) -> bool:
        return item in self._store.values()

    @__contains__.register(str)  # type: ignore
    def _(self, item: str) -> bool:
        return item in self._store.keys()

    @property
    def uids(self) -> set:
        """Return the associated uids. """
        return set(self.keys())

    @singledispatchmethod
    def add(self, *args: Any, **kwargs: Any) -> None:
        """Add objects"""
        # pylint: disable=no-self-use
        # pylint: disable=unused-argument
        raise NotImplementedError

    @add.register(PathPyObject)  # type: ignore
    def _(self, *args: PathPyObject, **kwargs: Any) -> None:
        """Add object to collection"""

        for obj in args:
            # check if object exists already
            if obj not in self.values() and obj.uid not in self.keys():

                # update attributes
                if kwargs:
                    obj.update(**kwargs)

                # add edge to the collection
                self._add(obj)
            else:
                self._if_exist(obj, **kwargs)

    def _add(self, obj: PathPyObject) -> None:
        """Add an edge to the set of edges."""
        self[obj.uid] = obj

    def _if_exist(self, obj: Any, **kwargs: Any) -> None:
        """Helper function if the edge does already exsist."""
        # pylint: disable=no-self-use
        # pylint: disable=unused-argument
        LOG.error('The object "%s" already exists in the Collection', obj.uid)
        raise KeyError

    @singledispatchmethod
    def remove(self, *args: Any, **kwargs: Any) -> None:
        """Remove objects"""
        # pylint: disable=no-self-use
        # pylint: disable=unused-argument
        raise NotImplementedError

    @remove.register(PathPyObject)  # type: ignore
    def _(self, *args: PathPyObject, **kwargs: Any) -> None:
        """Remove object from the collection"""
        # pylint: disable=unused-argument
        for obj in args:
            # check if object exists already
            if obj in self.values() and obj.uid in self.keys():
                self._remove(obj)

    def _remove(self, obj: PathPyObject) -> None:
        """Add an edge to the set of edges."""
        self.pop(obj.uid, None)


# =============================================================================
# eof
#
# Local Variables:
# mode: python
# mode: linum
# mode: auto-fill
# fill-column: 79
# End: