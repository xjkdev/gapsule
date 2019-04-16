import asyncio

from tornado.escape import json_decode

from gapsule.handlers.Base import BaseHandler
from gapsule.utils import ajaxquery, authenticated
from gapsule.utils.cookie_session import format_log_time
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
    action: str = ViewModelField(required=True, nullable=False)
    content: str = ViewModelField(required=False)


class NewIssueInput(ViewModelDict):
    owner: str = ViewModelField(required=True, nullable=False)
    repo: str = ViewModelField(required=True, nullable=False)
    title: str = ViewModelField(required=True, nullable=False)
    comment: str = ViewModelField(required=True, nullable=False)


class ForumHandler(BaseHandler):
    @ajaxquery
    async def get(self, owner, reponame, posttype, postid):
        repoid = await repo.get_repo_id(owner, reponame)
        postid = int(postid)
        poster, title, comments, status = await asyncio.gather(
            post.get_postername(repoid, postid),
            post.get_title(repoid, postid),
            post.get_all_comments(repoid, postid),
            post.get_status(repoid, postid)
        )
        for comment in comments:
            if 'address_time' in comment:
                comment['address_time'] = format_log_time(
                    comment['address_time'])
            if 'conmmenter' in comment:  # FIXME
                comment['commenter'] = comment['conmmenter']
        if posttype == 'issues':
            self.write(ForumGetResult(state='ok', title=title, poster=poster, status=status,
                                      comments=comments))
        else:
            self.write(ForumGetResult(state='ok', title=title, poster=poster, status=status,
                                      comments=comments))

    @ajaxquery
    async def post(self, owner, reponame, postid):
        data = ForumPostInput(json_decode(self.request.body))
        postid = int(postid)
        repoid = await repo.get_repo_id(owner, reponame)
        if data.action == 'newComment':
            await post.create_new_comment(
                repoid, postid, 'rich', data.content, self.current_user.user)
            self.write(dict(state='ok'))
        elif data.action == 'closeIssue':
            if len(data.content) > 0:
                content = '<action>close</action>' + data.content
                await post.create_new_comment(
                    repoid, postid, 'rich', content, self.current_user.user)
            await post.alter_status(repoid, postid, 'Closed')
            self.write(dict(state='ok'))
        elif data.action == 'reopenIssue':
            if len(data.content) > 0:
                content = '<action>close</action>' + data.content
                await post.create_new_comment(
                    repoid, postid, 'rich', content, self.current_user.user)
            await post.alter_status(repoid, postid, 'Open')
            self.write(dict(state='ok'))
        else:
            self.write(dict(state='error', error='invalid action.'))


class PostListHandler(BaseHandler):
    @ajaxquery
    async def get(self, owner, reponame, posttype):
        repoid = await repo.get_repo_id(owner, reponame)
        # if posttype == 'issues':
        # TODO: 区分issues和pulls
        allposts = await post.get_all_attached_posts(repoid)
        for ipost in allposts:
            if 'post_time' in ipost:
                ipost['post_time'] = format_log_time(ipost['post_time'])
        # print(allposts)
        self.write(dict(state='ok', issues=allposts))


class NewIssueHandler(BaseHandler):
    def get(self, owner, reponame):
        self.render('index.html')

    @authenticated
    async def post(self, owner, reponame):
        data = NewIssueInput(json_decode(self.request.body))
        repoid = await repo.get_repo_id(data.owner, data.repo)
        poster = self.current_user.user
        postid = await post.create_new_attached_post(repoid, poster, data.title, 'Open',
                                                     True)
        await post.create_new_comment(repoid, postid, 'text', data.comment, poster)
        print(data, repoid, poster, postid)
        self.write(dict(state='ok', issueid=postid))
