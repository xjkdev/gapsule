import json
import tornado.web

from gapsule.handlers.Base import BaseHandler
from gapsule.utils import ajaxquery
from gapsule.models.repo import (get_commits_num, get_branches_num, get_releases_num,
                                 get_contributors_info, get_specified_path,
                                 get_file_content)


class CodeListHandler(BaseHandler):
    @ajaxquery
    def get(self, username, projectname):
        state_dict = {
            "status": "ok",
            "commits": get_commits_num(username, projectname, 'master'),
            "branch": get_branches_num(username, projectname),
            "releases": get_releases_num(),
            "contributors": get_contributors_info(),
            "folder":  get_specified_path(username, projectname, 'master')
        }
        self.write(state_dict)


class FolderListHandler(BaseHandler):
    @ajaxquery
    def get(self, username, projectname, branch, restpath):
        folder_dict = {
            # goto 参数username, projectname,branch, restpath
            "foider": get_specified_path(username, projectname, branch, restpath)
        }
        self.write(folder_dict)


class FileContentHandler(BaseHandler):
    @ajaxquery
    def get(self, username, projectname, branch, restpath):
        file_dict = {
            # goto 参数username, projectname,branch, restpath
            "file": get_file_content(restpath)
        }
        self.write(file_dict)
