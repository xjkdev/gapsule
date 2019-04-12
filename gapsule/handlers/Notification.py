from gapsule.handlers.Base import BaseHandler
from  gapsule.models.notification import get_all_notifications
from gapsule.models.user import get_uid
import json
class Notificationhandler(BaseHandler):
    async def get(self):
        username = self.current_user.user
        userid=await get_uid(username)
        await get_all_notifications(userid)
        results = await get_all_notifications(userid)
        self.write(json.dumps(results))

