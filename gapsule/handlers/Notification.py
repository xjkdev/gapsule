from gapsule.handlers.Base import BaseHandler
import json

from gapsule.utils import ajaxquery, authenticated
from gapsule.models.notification import get_all_notifications
from gapsule.models.user import get_uid


class NotificationHandler(BaseHandler):
    @authenticated
    @ajaxquery
    async def get(self):
        username = self.current_user.user
        userid = await get_uid(username)
        results = await get_all_notifications(userid)
        self.write(json.dumps(results))
