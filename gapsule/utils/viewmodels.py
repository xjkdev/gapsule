"""
Module viewmodel:
This module is for better defining viewmodels.

ViewModelDict extends normal dict, together with ViewModelField to support some validation. 

example:
class view_model_example(ViewModelDict):
    datalist = ViewModelField(required=True, default_factory=list)
    errormsg = ViewModelField(nullable=True)
    count = ViewModelField(dafault=0)

In previous example, we create an view_model_example class that has one required field datalist. 
We also create nullable filed errormsg, and count filed with default value 0.
And we added an default_factory to generate default value for datalist, because list is mutable object. 

You can use attribute syntax like  model.count  to access value, which provide validation.
Yet you can also use dict syntax to access value like d['name'] = 'value', which ignore validation for flexibility.

ViewModelList is an alias to normal list, for readabiliy.
"""

__all__ = ['ViewModelDict', 'ViewModelField', 'ViewModelList']

from typing import Callable, Any, Union, List, TypeVar, Dict, Generic, Type

T = TypeVar('T')


class ViewModelField(Generic[T]):
    __slots__ = ['_default', '_default_factory', '_name', '_nullable', '_required',
                 '_readonly', '_type', '_validator']

    def __init__(self, type: Type = None,  *, required: bool = False, nullable: bool = True,
                 readonly: bool = False, default: T = None, default_factory: Callable[[], T] = None,
                 validator: Callable[[T], bool] = None):
        self._required = required
        self._nullable = nullable
        self._default = default
        self._default_factory = default_factory
        self._readonly = readonly
        self._validator = validator
        self._type = type

    def __get__(self, obj: 'ViewModelBase', objType=None) -> T:
        if obj is None:
            return self
        return obj[self._name]

    def __set__(self, obj: 'ViewModelBase', value: T):
        if self._readonly:
            raise AttributeError("can't set readonly attribute")
        if not self._nullable and (value is None or
                                   hasattr(value, '__len__') and
                                   len(value) == 0):
            raise AttributeError("can't set non-nullable attribute to None")
        if self._validator is not None:
            assert self._validator(value), 'attribute validation failed'
        obj[self._name] = value

    def __delete__(self, obj):
        if self._required:
            raise AttributeError("can't delete required attribute")
        del obj[self._name]

    def __set_name__(self, owner, name):
        self._name = name
        func = getattr(type(self._default), '__set_name__', None)
        if func:
            # There is a __set_name__ method on the descriptor, call
            # it.
            func(self._default, owner, name)

    def get_default(self, obj=None):
        if self._default_factory is not None:
            return self._default_factory()
        else:
            return self._default


class ViewModelDict(dict, Dict[str, Any]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for val in self.__class__.__dict__.values():
            if isinstance(val, ViewModelField):
                if val._required and not val._name in self:
                    default = val.get_default(self)
                    if not val._nullable and default is None:
                        raise ValueError(
                            "attribute {} is required and not nullalbe, yet not setted.".format(
                                val._name
                            ))
                    else:
                        self[val._name] = default
                elif not val._nullable and self[val._name] is None:
                    raise ValueError(
                        "attribute {} is not nullalbe, yet passed None.".format(val._name))

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, super().__repr__())


class ViewModelList(list, List[ViewModelDict]):
    pass
