from typing import List, Tuple, Optional
import asyncio
from tornado.escape import json_decode
import tornado.web
from gapsule.handlers.Base import BaseHandler
from gapsule.utils import ajaxquery
from gapsule.utils.viewmodels import ViewModelDict, ViewModelField
from gapsule.models.repo import (get_commits_num, get_branches_num, get_releases_num,
                                 get_contributors_info, get_specified_path,
                                 get_file_content, create_new_repo, get_default_branch)


class CodeListResult(ViewModelDict):
    state: str = ViewModelField(required=True)
    commitNumber: int = ViewModelField(required=True)
    branchNumber: int = ViewModelField(required=True)
    releaseNumber: int = ViewModelField(required=True)
    contributorNumber: int = ViewModelField(required=True)
    allFiles: List[Tuple[str, str]] = ViewModelField(required=True)
    readme: str = ViewModelField(required=False)
    currentBranch: str = ViewModelField(required=True)


class FolderListResult(ViewModelDict):
    files: List[Tuple[str, str]] = ViewModelField(required=True)


class FileContentResult(ViewModelDict):
    content: Optional[str] = ViewModelField(required=True)


class CreateNewRepoInput(ViewModelDict):
    creator: str = ViewModelField(required=True, nullable=False)
    reponame: str = ViewModelField(required=True, nullable=False)
    description: str = ViewModelField(required=True, nullable=False)
    repoVisibility: bool = ViewModelField(required=True, nullable=False)


class CodeListHandler(BaseHandler):
    @ajaxquery
    async def get(self, username, projectname):
        commit, branch, release, contributor, files, default_branch = await asyncio.gather(
            get_commits_num(username, projectname, 'master'),
            get_branches_num(username, projectname),
            get_releases_num(),
            get_contributors_info(),
            get_specified_path(username, projectname, 'master'),
            get_default_branch(username, projectname),
        )
        state_dict = CodeListResult(
            state="ok",
            commitNumber=commit,
            branchNumber=branch,
            releaseNumber=release,
            contributorNumber=contributor,
            allFiles=files,
            readme='',
            currentBranch=default_branch
        )
        self.write(state_dict)


class FolderListHandler(BaseHandler):
    @ajaxquery
    async def get(self, username, projectname, branch, restpath):
        files = await get_specified_path(username,
                                         projectname, branch, restpath)
        folder_dict = FolderListResult(files=files)
        self.write(folder_dict)


class FileContentHandler(BaseHandler):
    @ajaxquery
    async def get(self, username, projectname, branch, restpath):
        content = await get_file_content(restpath)
        file_dict = FileContentResult(content=content)
        self.write(file_dict)


class NewRepoHandler(BaseHandler):
    @ajaxquery
    def get(self):
        self.write(dict(state='ok', options=[self.current_user.user]))

    async def post(self):
        data = CreateNewRepoInput(json_decode(self.request.body))
        print(data)
        await create_new_repo(data.creator, data.reponame, data.description,
                              data.repoVisibility)
        self.write(dict(state='ok'))
