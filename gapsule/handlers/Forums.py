import asyncio
from urllib.parse import parse_qs

from gapsule.handlers.Base import BaseHandler
from gapsule.utils import ajaxquery
from gapsule.models import repo, post
from gapsule.utils.viewmodels import ViewModelDict, ViewModelField


class ReplyStruct(ViewModelDict):
    user = ViewModelField(required=True, nullable=False)
    text = ViewModelField(required=True)
    special = ViewModelField()


class ForumGetResult(ViewModelDict):
    title = ViewModelField(required=True, nullable=False)
    poster = ViewModelField(required=True, nullable=False)
    comments = ViewModelField(required=True)


class ForumPostInput(ViewModelDict):
    type = ViewModelField()
    text = ViewModelField()


class ForumHandler(BaseHandler):
    @ajaxquery
    async def get(self, owner, reponame, postid):
        repoid = await repo.get_repo_id(owner, reponame)
        poster, title, comments = await asyncio.gather([
            post.get_postername(repoid, postid),
            post.get_title(repoid, postid),
            post.get_all_comments(repoid, postid)
        ])
        self.write(ForumGetResult(title=title, poster=poster,
                                  comments=comments))

    @ajaxquery
    async def post(self, owner, reponame, postid):
        repoid = await repo.get_repo_id(owner, reponame)
        data = ForumPostInput(**parse_qs(self.request.body))
        await post.create_new_comment(
            repoid, postid, 'rich', data['content'], self.current_user.user)
        self.write(dict(state='ok'))
