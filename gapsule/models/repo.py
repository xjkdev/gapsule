from gapsule.utils.log_call import log_call

# 查询 repo的提交次数commits
@log_call()
def get_commits_num():
    return 1

# 修改 repo的提交次数commits
@log_call()
def set_commits_num(new_num):
    print('commits_num set as'+str(new_num)+' successfully')
    return True

# 查询  repo的分支数branch
@log_call()
def get_branches_name():
    return 1

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
    return 1


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

# 查询  对应版本对应路径下的某个文件夹包含的文件夹（名称）和文件（名称）
@log_call()
def get_specified_path():
    return '/specified_path'

# 查询  对应路径下的某个文件的内容
@log_call()
def get_file_content(path):
    return 'content:...'

# 查询  所有仓库文件
@log_call()
def get_all_files(repository_name):
    return 'files got from'+repository_name

# 查询  对应路径的文件（夹）是否存在
@log_call()
def path_exists():
    return True

# 查询  历史提交的版本与时间
@log_call()
def get_history():
    return 'edition:1 time:xxx'


class RepoNotFoundException(FileNotFoundError):
    pass

# 查询仓库是否为仓库对某用户可读，如果为不可读返回假，当且仅当可读或为公有仓库返回真，不存在raise RepoNotFoundException
# 当username=None时，表示查询匿名用户的权限，当且仅当为公有仓库时返回真，不存在raise exception，私有返回假。
@log_call()
def check_read_permission(owner, reponame, username=None):

    return True

# 查询仓库是否为仓库对某用户可写，当且仅当可写返回真，不存在raise RepoNotFoundException
@log_call()
def check_write_permission(owner, reponame, username):
    return True

# 查询仓库是否为仓库对某用户有管理权限，当且仅当有管理权限返回真，不存在raise RepoNotFoundException
@log_call()
def check_admin_permission(owner, reponame, username):
    return True
