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
        results = await get_all_notifications(username)
        self.write(dict(state='ok', notifications=results))
