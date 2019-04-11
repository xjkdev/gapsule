import json
import tornado.web

from gapsule.utils.decorators import ajaxquery
from gapsule.handlers.Base import BaseHandler


class CreatePullRequest(BaseHandler):
    @ajaxquery
    def get(self, username, projectname, restpath):
        compare_information = self.judgeBranch(username, restpath)
        for key_state in compare_information.keys():
            key_judge = False
            key_judge = (key_state == "base_repository") or(key_state == "base_branch") or(
                key_state == "base_repository") or(key_state == "head_repository")
            if not key_judge:
                self.set_status(400, "Unknown")
        # 参数compare_information,得到对比的数据,需要数据库提供接口
        request_end = 1
        if request_end == None:
            self.set_status(404, "Unknown")
        self.write(json.dumps(request_end))

    def judgeBranch(self, username, statepath):
        compare_dict = {}
        separate_sign = 0
        str_path = ''
        for state in statepath:
            str_path += state
            if state == ':' and separate_sign == 0:
                compare_dict["base_repository"] = str_path
                str_path = ''
                separate_sign = 1
            if state == '.' and separate_sign == 1:
                compare_dict["base_branch"] = str_path
                str_path = ''
                separate_sign = 2
            if state == '.' and separate_sign == 0:
                compare_dict["base_repository"] = username
                compare_dict["base_branch"] = str_path
                str_path = ''
                separate_sign = 2
            if state == '.' and separate_sign == 2:
                continue
            if state == ':' and separate_sign == 2:
                compare_dict["head_repository"] = str_path
                str_path = ''
                separate_sign == 3
        if separate_sign == 3:
            compare_dict["compare_branch"] = str_path
        else:
            compare_dict["head_repository"] = username
            compare_dict["base_branch"] = str_path
        return compare_dict
