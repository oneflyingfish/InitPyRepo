import subprocess


def _run_cmd(cmd=list[str]) -> str | None:
    res = subprocess.run(
        cmd,
        text=True,
        cwd=".",
        capture_output=True,
    )
    if res.returncode == 0:
        return res.stdout.strip()
    else:
        return None


class GitOperator:
    @staticmethod
    def get_commit_id(ref: str = None) -> str | None:
        """ref can be commit_id, tag, branch_name"""

        if ref is None:
            ref = "HEAD"
        return _run_cmd(
            ["git", "rev-parse", "--quiet", "--verify", f"{ref}^{{commit}}"]
        )

    @staticmethod
    def get_current_branch_name() -> str | None:
        return _run_cmd(["git", "rev-parse", "--abbrev-ref", "HEAD"])

    @staticmethod
    def get_stage_files(ends=None) -> list:
        cmd = ["git", "diff", "--cached", "--name-only"]
        diff_out = _run_cmd(cmd)
        if diff_out is None:
            return []
        else:
            return [
                p
                for p in diff_out.splitlines()
                if (ends is None or len(ends) < 1 or p.endswith(tuple(ends)))
            ]

    @staticmethod
    def get_uncommit_files(ends=None) -> list:
        cmd = ["git", "ls-files", "-m", "-o", "--exclude-standard"]
        diff_out = _run_cmd(cmd)
        if diff_out is None:
            return []
        else:
            return [
                p
                for p in diff_out.splitlines()
                if (ends is None or len(ends) < 1 or p.endswith(tuple(ends)))
            ]

    @staticmethod
    def get_committed_files(from_commit: str, to_commit: str = None) -> str:
        """
        get file change list from <from_commit> to <to_commit>

        :param from_commit: history commit id
        :type from_commit: str
        :param to_commit: None means HEAD
        :type to_commit: str
        """

        from_commit = GitOperator.get_commit_id(from_commit)
        to_commit = GitOperator.get_commit_id(to_commit)
        assert from_commit is not None and to_commit is not None, "invalid commit"

        cmd = ["git", "diff", "--name-only", f"{from_commit}", f"{to_commit}"]
        diff_out = _run_cmd(cmd)
        if diff_out is None:
            return []
        else:
            return [p for p in diff_out.splitlines()]

    @staticmethod
    def switch_branch(branch_name: str):
        cmd = ["git", "switch", branch_name]
        return _run_cmd(cmd)

    @staticmethod
    def delete_branch(branch_name: str):
        cmd = ["git", "branch", "-d", branch_name]
        return _run_cmd(cmd)

    @staticmethod
    def checkout_new(branch_name: str):
        assert (
            len(branch_name) > 0 and GitOperator.get_commit_id(branch_name) is None
        ), f"{branch_name} is already exist"

        cmd = ["git", "checkout", "-b", branch_name]
        return _run_cmd(cmd)

    @staticmethod
    def reset_to(ref: str):
        commit_id = GitOperator.get_commit_id(ref)
        assert commit_id is not None, f"{ref} is not refer a valid commit"

        cmd = ["git", "reset", "--hard", commit_id]
        return _run_cmd(cmd)

    @staticmethod
    def zip_commit(last_remain_commit: str, comment: str):
        last_remain_commit = GitOperator.get_commit_id(last_remain_commit)
        assert last_remain_commit is not None, "invalid commit"
        cmd = ["git", "reset", "--soft", last_remain_commit]
        _run_cmd(cmd)
        cmd = ["git", "commit", "-m", comment]
        _run_cmd(cmd)
