import os
import json
import tornado.web
import sys
from gapsule.handlers.Base import BaseHandler
from gapsule.utils import ajaxquery
from gapsule.models.repo import (get_commits_num, get_branches_name, get_releases_num,
                                 get_contributors_info, get_specified_path,
                                 get_file_content)


class CodeListHandler(BaseHandler):
    @ajaxquery
    def get(self, username, projectname):
        state_dict = {
            "commits": get_commits_num(),
            "branch": get_branches_name(),
            "releases": get_releases_num(),
            "contributors": get_contributors_info(),
        }
        code_dict = {
            # goto 参数username, projectname,分支为默认master,文件路径为/
            "foider": get_specified_path()
        }
        self.write(json.dumps([state_dict, code_dict]))


class FolderListHandler(BaseHandler):
    @ajaxquery
    def get(self, username, projectname, branch, restpath):
        folder_dict = {
            # goto 参数username, projectname,branch, restpath
            "foider": get_specified_path()
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
