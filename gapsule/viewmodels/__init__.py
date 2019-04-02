"""
Module viewmodel:

This module is for defining viewmodels.

example:
class view_model_example(ViewModelDict):
    datalist = ViewModelField('datalist', required=True)
    errormsg = ViewModelField('errormsg', nullable=True)
    count = ViewModelField('count', dafault=0)

    @datalist.default
    def datalist():
        return []

ViewModelDict extends normal dict, together with ViewModelField to support some validation. 
In previous example, we create an view_model_example class that has one required field datalist. 
We also create nullable filed  errormsg, and count filed with default value 0.
And we added an method to generate default value for datalist, because list is mutable object. 

You can use attribute syntax like  model.count  to access value, which provide validation.
Yet you can also use dict syntax to access value like d['name'] = 'value', which ignore validation for flexibility.

ViewModelList is an alias to normal list, for readabiliy.
"""
from gapsule.viewmodels.base import ViewModelDict, ViewModelField, ViewModelList

__all__ = ['ViewModelDict', 'ViewModelField', 'ViewModelList']
