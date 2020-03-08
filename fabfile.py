from fabric import task
from invoke import Responder
from ._credentials import github_username, github_password


def _get_github_auth_responders():
    """
    返回 github 用户名密码自动填充器
    """
    username_responder = Responder(
        pattern="Username for 'https://github.com'",
        response=f'{github_username}\n'
    )
    password_responder = Responder(
        pattern=f"Password for 'https://{github_username}@github.com'",
        response=f'{github_password}\n'
    )
    return [username_responder, password_responder]


@task()
def deploy(c):
    supervisor_conf_path = '~/etc/'
    supervisor_program_name = 'zhoujun_blog'

    project_root_path = '~/apps/zhoujun_blog'

    # 先停止应用
    with c.cd(supervisor_conf_path):
        cmd = f'supervisorctl stop {supervisor_program_name}'

    # 进入项目根目录，从git拉去新代码
    with c.cd(supervisor_conf_path):
        cmd = 'git pull'
        responders = _get_github_auth_responders()
        c.run(cmd, watchers=responders)

    # 重新启动应用
    with c.cd(supervisor_conf_path):
        cmd = f'supervisorctl start {supervisor_program_name}'
        c.run(cmd)
