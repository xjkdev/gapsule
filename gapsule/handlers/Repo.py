import os
import json
import tornado.web
import sys
from typing import List, Tuple, Optional
from gapsule.handlers.Base import BaseHandler
from gapsule.utils import ajaxquery
from gapsule.utils.viewmodels import ViewModelDict, ViewModelField
from gapsule.models.repo import (get_commits_num, get_branches_num, get_releases_num,
                                 get_contributors_info, get_specified_path,
                                 get_file_content)


class CodeListResult(ViewModelDict):
    status: str = ViewModelField(required=True)
    commits: int = ViewModelField(required=True)
    branch: int = ViewModelField(required=True)
    releases: int = ViewModelField(required=True)
    contributors: int = ViewModelField(required=True)
    files: List[Tuple[str, str]] = ViewModelField(required=True)


class FolderListResult(ViewModelDict):
    files: List[Tuple[str, str]] = ViewModelField(required=True)


class FileContentResult(ViewModelDict):
    content: Optional[str] = ViewModelField(required=True)


class CodeListHandler(BaseHandler):
    @ajaxquery
    def get(self, username, projectname):
        state_dict = CodeListResult({
            "status": "ok",
            "commits": get_commits_num(username, projectname, 'master'),
            "branch": get_branches_num(username, projectname),
            "releases": get_releases_num(),
            "contributors": get_contributors_info(),
            "files":  get_specified_path(username, projectname, 'master')
        })
        self.write(state_dict)


class FolderListHandler(BaseHandler):
    @ajaxquery
    def get(self, username, projectname, branch, restpath):
        folder_dict = FolderListResult(files=get_specified_path(username,
                                                                projectname, branch, restpath))
        self.write(folder_dict)


class FileContentHandler(BaseHandler):
    @ajaxquery
    def get(self, username, projectname, branch, restpath):
        file_dict = FileContentResult(content=get_file_content(restpath))
        self.write(file_dict)
