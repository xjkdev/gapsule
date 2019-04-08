"""
Module viewmodel:
This module is for better defining viewmodels.

ViewModelDict extends normal dict, together with ViewModelField to support some validation. 

example:
class view_model_example(ViewModelDict):
    datalist = ViewModelField('datalist', required=True)
    errormsg = ViewModelField('errormsg', nullable=True)
    count = ViewModelField(dafault=0)

    @datalist.default
    def datalist(self):
        return []

In previous example, we create an view_model_example class that has one required field datalist. 
We also create nullable filed  errormsg, and count filed with default value 0.
And we added an method to generate default value for datalist, because list is mutable object. 
The  name  argument in ViewModelField is optional.

You can use attribute syntax like  model.count  to access value, which provide validation.
Yet you can also use dict syntax to access value like d['name'] = 'value', which ignore validation for flexibility.

ViewModelList is an alias to normal list, for readabiliy.
"""

__all__ = ['ViewModelDict', 'ViewModelField', 'ViewModelList']

from typing import Callable, Any, Union, List, TypeVar, Dict, Generic

T = TypeVar('T')


class ViewModelField(Generic[T]):
    def __init__(self, name: str = None, *, required: bool = False, nullable: bool = True,
                 readonly: bool = False, default: Union[None, T, Callable[[], T]] = None,
                 validation: Callable[[T], bool] = None):
        self._name = name
        self._required = required
        self._nullable = nullable
        self._default = default
        self._readonly = readonly
        self._validation = validation

    def __get__(self, obj: 'ViewModelBase', objType=None) -> T:
        if obj is None:
            return self
        return obj[self._name]

    def __set__(self, obj: 'ViewModelBase', value: T):
        if self._readonly:
            raise AttributeError("can't set readonly attribute")
        if not self._nullable and value is None:
            raise AttributeError("can't set non-nullable attribute to None")
        if self._validation is not None:
            if isinstance(self._validation, classmethod):
                assert self._validation.__get__(obj)(
                    value), 'attribute validation failed'
            else:
                assert self._validation(value), 'attribute validation failed'
        obj[self._name] = value

    def __delete__(self, obj):
        if self._required:
            raise AttributeError("can't delete required attribute")
        del obj[self._name]

    def get_default(self, obj=None):
        if isinstance(self._default, classmethod):
            return self._default.__get__(obj)()
        if callable(self._default):
            return self._default()
        else:
            return self._default

    def default(self, f):
        return type(self)(self._name, required=self._required, nullable=self._nullable, readonly=self._readonly,
                          default=classmethod(f), validation=self._validation)

    def validation(self, f):
        return type(self)(self._name, required=self._required, nullable=self._nullable, readonly=self._readonly,
                          default=self._default, validation=classmethod(f))


class ViewModelDict(dict, Dict[str, Any]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, val in self.__class__.__dict__.items():
            if isinstance(val, ViewModelField):
                if val._name is None:
                    val._name = name
                if val._required and not val._name in self:
                    default = val.get_default(self)
                    if not val._nullable and default is None:
                        raise ValueError(
                            "attribute is required and not nullalbe, yet not setted.")
                    else:
                        self[val._name] = default
                elif not val._nullable and self[val._name] is None:
                    raise ValueError(
                        "attribute is not nullalbe, yet passed None.")

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, super().__repr__())


class ViewModelList(list, List[ViewModelDict]):
    pass
