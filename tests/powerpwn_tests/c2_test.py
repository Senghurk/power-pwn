from typing import List

import pytest

from powerpwn.c2 import PowerPwnC2
from powerpwn.models.cmd_arguments import CommandToRunEnum
from powerpwn.models.cmd_results import (
    AgentRunErrors,
    AgentRunType,
    CleanupOutputs,
    CodeExecOutputs,
    CommandResults,
    ExfiltrationOutputs,
    RansomwareOutputs,
    StealCookieOutputs,
    StealPowerAutomateTokenOutputs,
)

POST_URL = ""
DEBUG = True


class DummyPowerPwnC2(PowerPwnC2):
    def __init__(self, post_url: str, debug: bool, command_to_run: CommandToRunEnum):
        super().__init__(post_url, debug)
        self.command_to_run = command_to_run

    def _run_cmd(self, arguments_as_dict: dict) -> dict:
        cmd_res = CommandResults.construct(
            is_success=True,
            agent_run_type=AgentRunType.attended.value,
            agent_run_errors=AgentRunErrors.construct(attended_run_error={}, unattended_run_error={}),
        )

        if self.command_to_run == CommandToRunEnum.CODE_EXEC:
            cmd_res.cmd_code_execution = CodeExecOutputs.construct()
        elif self.command_to_run == CommandToRunEnum.RANSOMWARE:
            cmd_res.cmd_ransomware = RansomwareOutputs.construct()
        elif self.command_to_run == CommandToRunEnum.EXFILTRATION:
            cmd_res.cmd_exfiltration = ExfiltrationOutputs.construct()
        elif self.command_to_run == CommandToRunEnum.CLEANUP:
            cmd_res.cmd_cleanup = CleanupOutputs.construct()
        elif self.command_to_run == CommandToRunEnum.STEAL_POWER_AUTOMATE_TOKEN:
            cmd_res.cmd_steal_power_automate_token = StealPowerAutomateTokenOutputs.construct()
        elif self.command_to_run == CommandToRunEnum.STEAL_COOKIE:
            cmd_res.cmd_steal_cookie = StealCookieOutputs.construct()
        else:
            raise ValueError(f"command_to_run has invalid value: {self.command_to_run}.")

        return cmd_res.json()


@pytest.mark.parametrize("exec_env", ["exec_py2", "exec_vb" "exec_js", "exec_ps", "exec_cmd"])
def test_code_exec(exec_env: str, command: str = ""):
    c2 = DummyPowerPwnC2(post_url=POST_URL, debug=DEBUG, command_to_run=CommandToRunEnum.CODE_EXEC)

    exec_env_command = getattr(c2, exec_env)
    exec_env_command(command=command)


def test_ransomware(crawl_depth: str = 0, dirs_to_init_crawl: List[str] = None, encryption_key: str = ""):
    if dirs_to_init_crawl is None:
        dirs_to_init_crawl = []
    c2 = DummyPowerPwnC2(post_url=POST_URL, debug=DEBUG, command_to_run=CommandToRunEnum.RANSOMWARE)
    c2.ransomware(crawl_depth=crawl_depth, dirs_to_init_crawl=dirs_to_init_crawl, encryption_key=encryption_key)


def test_exfiltration(target_file_path: str = ""):
    c2 = DummyPowerPwnC2(post_url=POST_URL, debug=DEBUG, command_to_run=CommandToRunEnum.EXFILTRATION)
    c2.exfiltrate(target_file_path=target_file_path)


def test_cleanup():
    c2 = DummyPowerPwnC2(post_url=POST_URL, debug=DEBUG, command_to_run=CommandToRunEnum.CLEANUP)
    c2.cleanup()


def test_steal_power_automate_token():
    c2 = DummyPowerPwnC2(post_url=POST_URL, debug=DEBUG, command_to_run=CommandToRunEnum.STEAL_POWER_AUTOMATE_TOKEN)
    c2.steal_power_automate_token()


def test_steal_cookie(fqdn: str = ""):
    c2 = DummyPowerPwnC2(post_url=POST_URL, debug=DEBUG, command_to_run=CommandToRunEnum.STEAL_COOKIE)
    c2.steal_cookie(fqdn=fqdn)
