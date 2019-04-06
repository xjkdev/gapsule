from gapsule.handlers.Base import BaseHandler
from gapsule.utils import ajaxquery
from gapsule.utils.viewmodels import ViewModelDict, ViewModelField


class ReplyStruct(ViewModelDict):
    user = ViewModelField(required=True, nullable=False)
    text = ViewModelField(required=True)
    special = ViewModelField()


class ForumGetResult(ViewModelDict):
    title = ViewModelField(required=True, nullable=False)
    initiator = ViewModelField(required=True, nullable=False)
    replys = ViewModelField(required=True)


class ForumPostInput(ViewModelDict):
    action = ViewModelField(required=True, nullable=False)
    text = ViewModelField()
    refs = ViewModelField()


class ForumHandler(BaseHandler):
    @ajaxquery
    def get(self, host, id):
        pass
