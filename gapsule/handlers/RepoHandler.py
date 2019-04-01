# -*- coding=utf-8 _*_

import os
import json
import tornado
import tornado.web
from gapsule.models.repo import (get_commits_num, get_branches_name, get_releases_num,
                                get_contributors_info, get_specified_path,
                                get_file_content)

class CodeListHandler(tornado.web.RequestHandler):
    def get(self):
        code_dict = {}
        code_state = get_commits_num()
        code_dict["commits"] = code_state
        code_state = get_branches_name()
        code_dict["branch"] = code_state
        code_state = get_releases_num()
        code_dict["releases"] = code_state
        code_state = get_contributors_info()
        code_dict["contributors"] = code_state
        code_state = get_specified_path()
        code_dict["foider"] = code_state
        self.write(code_dict)

class FioderListHandler(tornado.web.RequestHandler):
    def get(self):
        fioder_dict = get_specified_path()
        self.write(json.dumps(fioder_dict))

class FileContentHandler(tornado.web.RequestHandler):
    def get(self):
        file_dict = {}
        path = self.request.path
        file_dict["file"] = get_file_content(path)
        self.write(file_dict)