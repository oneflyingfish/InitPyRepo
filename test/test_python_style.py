from pathlib import Path
import sys, os

sys.path.insert(0, os.path.join(Path(__file__).parent.parent, "tools"))

import argparse
from git_helper.check.check_character import check_only_assic
from git_helper.check.check_format import check_format
from git_helper.check.white_file import skip_check_file_prefix
from git_helper.check.files import stage_files, committed_files


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")


def do_check(
    only_check=False,
    contain_stage=True,
    contain_commit=True,
):
    files = stage_files(ends=[".py"]) if contain_stage else []
    files = files + (committed_files(ends=[".py"]) if contain_commit else [])

    if not check_only_assic(files):
        return -1, len(files)
    if not check_format(files, only_check=only_check):
        return -2, len(files)

    return 0, len(files)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="test style",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--only_check",
        type=str2bool,
        default=True,
        required=False,
        help="only check with no fix",
    )
    parser.add_argument(
        "--contain_stage",
        type=str2bool,
        default=True,
        required=False,
        help="range contain stage file",
    )
    parser.add_argument(
        "--contain_commit",
        type=str2bool,
        default=True,
        required=False,
        help="range contain last commit file",
    )
    args = parser.parse_args()

    status_code, file_count = do_check(
        only_check=args.only_check,
        contain_stage=args.contain_stage,
        contain_commit=args.contain_commit,
    )
    if status_code >= 0:
        print(f"SUCCESS: check total {file_count} files pass")
    else:
        print(f"ERROR: check total {file_count} files, failed. check log for detail")
    exit(status_code)
