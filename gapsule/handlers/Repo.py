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
    status: str = ViewModelField(required=True, nullable=False)
    content: Optional[str] = ViewModelField(required=False)
    error: str = ViewModelField(required=False)


class CreateNewRepoInput(ViewModelDict):
    creator: str = ViewModelField(required=True, nullable=False)
    reponame: str = ViewModelField(required=True, nullable=False)
    description: str = ViewModelField(required=True, nullable=False)
    repoVisibility: bool = ViewModelField(required=True, nullable=False)


class CodeListHandler(BaseHandler):
    @ajaxquery
    async def get(self, owner, reponame):
        commit, branch, release, contributor, files, default_branch = await asyncio.gather(
            get_commits_num(owner, reponame, 'master'),
            get_branches_num(owner, reponame),
            get_releases_num(),
            get_contributors_info(),
            get_specified_path(owner, reponame, 'master'),
            get_default_branch(owner, reponame),
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
    async def get(self, owner, reponame, branch, restpath):
        files = await get_specified_path(owner,
                                         reponame, branch, restpath)
        folder_dict = FolderListResult(files=files)
        self.write(folder_dict)


class FileContentHandler(BaseHandler):
    @ajaxquery
    async def get(self, owner, reponame, branch, restpath):
        try:
            data = await get_file_content(owner, reponame, branch, restpath)
            self.write(dict(state="ok", content=data))
        except OSError as e:
            print(e)
            self.write(dict(state="error", content=None,
                            error='os error occurs.'))


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
