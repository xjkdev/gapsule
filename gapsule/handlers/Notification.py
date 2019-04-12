from gapsule.handlers.Base import BaseHandler
from  gapsule.models.notification import get_all_notifications
from gapsule.models.user import get_uid
import json
class Notificationhandler(BaseHandler):
    async def get(self):
        userid=await get_uid()
        await get_all_notifications(userid)
        results = await get_all_notifications(userid)
        self.write(json.dumps(results))

