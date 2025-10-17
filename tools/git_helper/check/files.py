import os
import subprocess
from .white_file import skip_check_file_prefix


def _run(cmd: list[str], **kw):
    return subprocess.check_output(cmd, text=True, **kw)


def set_local_env():
    os.environ["GITHUB_EVENT_NAME"] = "push"
    os.environ["GITHUB_SHA"] = _run(["git", "rev-parse", "HEAD"]).strip()
    os.environ["GITHUB_SHA_BEFORE"] = _run(["git", "rev-parse", "HEAD~"]).strip()
    os.environ["GITHUB_REF_NAME"] = _run(["git", "branch", "--show-current"]).strip()


def stage_files(ends=[".py"]):
    cmd = ["git", "diff", "--cached", "--name-only"]
    diff_out = _run(cmd)
    py_files = [
        p
        for p in diff_out.splitlines()
        if (ends is None or len(ends) < 1 or p.endswith(tuple(ends)))
        and not p.startswith(tuple(skip_check_file_prefix))
    ]
    return py_files


def committed_files(ends=[".py"]):
    event = os.environ.get("GITHUB_EVENT_NAME", None)
    if event is None:
        set_local_env()
        event = "push"
    else:
        _run(["git", "fetch", "origin", "+refs/heads/*:refs/remotes/origin/*"])

    if event == "pull_request":
        base_ref = os.environ["GITHUB_BASE_REF"]
        base_sha = f"origin/{base_ref}"
    elif event == "push":
        import json

        event_path = os.environ.get("GITHUB_EVENT_PATH", None)
        if event_path is None:
            before = os.environ.get("GITHUB_SHA_BEFORE", "0")
        else:
            with open(event_path) as fp:
                before = json.load(fp).get("before", "")
        if before and set(before) != {"0"}:
            base_sha = before
        else:
            base_sha = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"  # git empty hash
    else:
        print("warning: base branch cannot be determined. use main origin/default.")
        base_sha = "origin/main"

    cmd = ["git", "diff", "--name-only", f"{base_sha}", "HEAD"]
    diff_out = _run(cmd)
    py_files = [
        p
        for p in diff_out.splitlines()
        if (ends is None or len(ends) < 1 or p.endswith(tuple(ends)))
        and not p.startswith(tuple(skip_check_file_prefix))
    ]
    return py_files


if __name__ == "__main__":
    if "GITHUB_EVENT_NAME" not in os.environ:
        os.environ["GITHUB_EVENT_NAME"] = "push"
        os.environ["GITHUB_SHA"] = _run(["git", "rev-parse", "HEAD"]).strip()
        os.environ["GITHUB_SHA_BEFORE"] = _run(["git", "rev-parse", "HEAD~"]).strip()
        os.environ["GITHUB_REF_NAME"] = _run(
            ["git", "branch", "--show-current"]
        ).strip()
    print("\n".join(committed_files()))
