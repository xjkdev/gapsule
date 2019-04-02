from gapsule.viewmodels import ViewModelDict, ViewModelField


class SignInResult(ViewModelDict):
    state = ViewModelField('state', required=False)
    error = ViewModelField('error', required=False)
