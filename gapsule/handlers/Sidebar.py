from typing import List

from gapsule.models import repo, post
from gapsule.handlers.Base import BaseHandler
from gapsule.utils import ajaxquery, authenticated
from gapsule.utils.viewmodels import ViewModelDict, ViewModelField


class SideBarResult(ViewModelDict):
    state: str = ViewModelField(required=True, nullable=False)
    error: str = ViewModelField(required=False)
    people: List[str] = ViewModelField(required=True, default_factory=list)
    topics: List[str] = ViewModelField(required=True, default_factory=list)
    projects: List[str] = ViewModelField(required=True, default_factory=list)


class SideBarHandler(BaseHandler):

    async def get_topics(self):
        username = self.current_user.user
        topics = await post.get_all_posts_of_poster(username)
        results = []
        for t in topics:
            tmp = {
                "id": t['post_id'],
                "title": t['title'],
            }
            repoid = t['repo_id']
            repoinfo = await repo.get_repo_info(repoid)
            tmp['type'] = 'issues' if t['is_issue'] else 'pull'
            tmp['repo'] = '{}/{}'.format(repoinfo['username'],
                                         repoinfo['reponame'])
            results.append(tmp)
        return results

    async def get_projects(self):
        username = self.current_user.user
        projects = await repo.get_repo_names(username)
        results = [{"owner": username,
                    "repo": "{}/{}".format(username, project)}
                   for project in projects]
        return results

    @ajaxquery
    async def get(self):
        if self.current_user is None:
            self.write(dict(state="error", error="not signed"))
        projects = await self.get_projects()
        topics = await self.get_topics()
        people = []
        self.write(SideBarResult(state='ok', projects=projects,
                                 topics=topics, people=people))
