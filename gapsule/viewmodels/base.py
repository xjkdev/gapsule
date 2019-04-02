from typing import Callable, Any, Union, List, TypeVar, Dict

T = TypeVar('T')


class ViewModelField():
    def __init__(self, name: str, required: bool = False, nullable: bool = True,
                 readonly: bool = False, defult: Union[None, T, Callable[[], T]] = None,
                 validation: Callable[[T], bool] = None):
        self._name = name
        self._required = required
        self._nullable = nullable
        self._default = defult
        self._readonly = readonly
        self._validation = validation

    def __get__(self, obj: 'ViewModelBase', objType=None):
        if obj is None:
            return self
        obj.get(self._name)

    def __set__(self, obj: 'ViewModelBase', value: T):
        if self._readonly:
            raise AttributeError("can't set readonly attribute")
        if not self._nullable and value is None:
            raise AttributeError("can't set non-nullable attribute to None")
        if self._validation is not None:
            assert self._validation(value), 'attribute validation failed'
        obj[self._name] = value

    def __delete__(self, obj):
        if self._required:
            raise AttributeError("can't delete required attribute")
        del obj[self._name]

    def get_default(self):
        if callable(self._default):
            return self._default()
        else:
            return self._default

    def default(self, default):
        return type(self)(self._name, self._required, self._nullable, self._readonly,
                          default, self._validation)


class ViewModelDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for val in self.__dict__.values():
            if isinstance(val, ViewModelField):
                if val._required and not val._name in kwargs:
                    if not val._nullable and val._default is None:
                        raise ValueError(
                            "attribute is required and not nullalbe, yet not setted.")
                    else:
                        self[val._name] = val.get_default()

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, super().__repr__())


class ViewModelList(List[ViewModelDict]):
    pass
