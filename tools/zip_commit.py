import argparse
from pathlib import Path
import os
import sys

sys.path.insert(0, os.path.join(Path(__file__).parent))
from git_helper.git_operator import GitOperator


def main():
    parser = argparse.ArgumentParser(
        description="zip git commit",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--last_remain_commit",
        type=str,
        required=True,
        help="last remain hash",
    )

    parser.add_argument(
        "--commit_comment",
        type=str,
        required=True,
        help="your commit comment",
    )

    parser.add_argument(
        "--gen_branch",
        type=str,
        default="",
        required=False,
        help='gen branch name, "" means $name_zip',
    )

    args = parser.parse_args()

    last_commit = GitOperator.get_commit_id(args.last_remain_commit)
    assert (
        last_commit is not None
    ), f"error: you must provide valid commit_id, {args.last_remain_commit} not found"

    branch_name = GitOperator.get_current_branch_name()
    assert branch_name is not None

    current_commit = GitOperator.get_commit_id(ref=None)
    if current_commit == last_commit:
        print("you require zip 0 commits, just skip this run")
        return

    zip_branch_name = (
        f"{branch_name}_zip" if len(args.gen_branch) < 1 else args.gen_branch
    )
    assert (
        GitOperator.get_commit_id(zip_branch_name) is None
    ), f"{zip_branch_name} is already exist, please use --gen_branch to set new name"

    uncommit_files = GitOperator.get_uncommit_files()
    assert (
        uncommit_files is None or len(uncommit_files) < 1
    ), f"error: you still have uncommit files: {uncommit_files}, it is unsafe during zip commit, you can set they in .gitignore or add to commit. no change in this run"

    GitOperator.checkout_new(zip_branch_name)
    try:
        GitOperator.zip_commit(last_commit, args.commit_comment)
    except Exception as ex:
        print(f"error to zip commit, info: {ex}")
        GitOperator.switch_branch(branch_name)
        GitOperator.delete_branch(zip_branch_name)
        return
    GitOperator.switch_branch(branch_name)

    print(f"zip commits to {zip_branch_name}. \n\nrun below to make affect:")
    print(
        f"git reset --hard {last_commit} && git merge {zip_branch_name} # merge change"
    )
    print(f"git branch -d {zip_branch_name} # rm zip branch")
    print(f"git push -f # [choosable] push to remote\n")


if __name__ == "__main__":
    main()
