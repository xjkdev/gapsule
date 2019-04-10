from typing import List, Tuple, Dict, Optional
import os
from logging import warning
import chardet
from gapsule.utils.log_call import log_call
from gapsule.models import git


def get_commits_num(owner, repo, branch):
    """ 查询 repo的提交次数commits """
    return len(git.git_commit_logs(owner, repo, branch, pretty=git.ONELINE))

# 修改 repo的提交次数commits
@log_call(warning)
def set_commits_num(new_num):
    print('commits_num set as'+str(new_num)+' successfully')
    return True


def get_branches_num(owner, repo):
    """ 查询  repo的分支数branch """
    return len(git.git_branches(owner, repo)[1])

# 修改  repo的分支数branch
@log_call()
def set_branches_num(new_num):
    print('branches_num set as'+str(new_num)+' successfully')
    return True

# （存入 + 查询 + 删除） 分支的成员
@log_call()
def create_new_member():
    print('Created a new member')
    return True


@log_call()
def get_member_info():
    print("Got member'info:")
    # return member.info


@log_call()
def delete_member():
    print('Deleted')
    return True

# （查询 + 修改） repo的releases数
@log_call()
def get_releases_num():
    return 0


@log_call()
def add_release(*args):
    return True

# （查询 + 修改） repo的contributors
@log_call()
def get_contributors_info():
    return


@log_call()
def set_contributors():
    return

# 存入  对应贡献成员
@log_call()
def set_specified_contributor():
    return


def get_specified_path(owner, reponame, branch, path=None) -> List[Tuple[str, str, bool]]:
    """ 查询  对应版本对应路径下的某个文件夹包含的文件夹（名称）和文件（名称）
        返回三元组，分别为name, hash, is_dir
    """
    return git.git_ls_files(owner, reponame, branch, path=path, show_tree=True)


_TEXTCHARS = bytearray({7, 8, 9, 10, 12, 13, 27} |
                       set(range(0x20, 0x100)) - {0x7f})


def _is_binary_string(bytes):
    return bool(bytes.translate(None, _TEXTCHARS))


@log_call()
def get_file_content(owner, reponame, branch, path) -> Optional[str]:
    """ 查询  对应路径下的某个文件的内容
        如果文件不存在或为目录，会抛出OSError
        如果为二进制文件或大文件，返回空
    """
    data = git.git_cat_file(owner, reponame, branch, path)
    if len(data) > 204800 or _is_binary_string(data[:20480]):  # big file
        return None
    det = chardet.detect(data)
    if det['confidence'] < 0.5:
        return None
    return data.decode(det['encoding'])


def get_all_files(owner, reponame, branch) -> List[Tuple[str, str]]:
    """ 查询  所有仓库文件 """
    return git.git_ls_files(owner, reponame, branch)


def path_exists(owner, reponame, branch, path) -> bool:
    """ 查询  对应路径的文件（夹）是否存在 """
    files = git.git_ls_files(owner, reponame, branch, show_tree=True)
    files = [info[0] for info in files]
    path = path.rstrip('/')
    return path in files


def get_history(owner, reponame, branch) -> List[Dict[str, str]]:
    """ 查询 历史提交的版本与时间 """
    return git.git_commit_logs(owner, reponame, branch, pretty=git.MEDIUM)


class RepoNotFoundException(FileNotFoundError):
    pass

# 查询仓库是否为仓库对某用户可读，如果为不可读返回假，当且仅当可读或为公有仓库返回真，不存在raise RepoNotFoundException
# 当username=None时，表示查询匿名用户的权限，当且仅当为公有仓库时返回真，不存在raise exception，私有返回假。
@log_call()
async def check_read_permission(owner, reponame, username=None):

    return True

# 查询仓库是否为仓库对某用户可写，当且仅当可写返回真，不存在raise RepoNotFoundException
@log_call()
async def check_write_permission(owner, reponame, username):
    return True

# 查询仓库是否为仓库对某用户有管理权限，当且仅当有管理权限返回真，不存在raise RepoNotFoundException
@log_call()
async def check_admin_permission(owner, reponame, username):
    return True
