from pathlib import Path
import sys, os

sys.path.insert(0, os.path.join(Path(__file__).parent.parent, "tools"))

from git_helper.check.check_character import check_only_assic
from git_helper.check.check_format import check_format
from git_helper.check.files import committed_files


def check() -> int:
    files = committed_files(ends=[".py"])
    if len(files) < 1:
        return 0, 0

    print("--------------------check files-------------------------")
    for file in files:
        print(f"> {file}")
    print("--------------------------------------------------------")

    if not check_only_assic(files):
        return -1, len(files)
    if not check_format(files):
        return -2, len(files)

    return 0, len(files)


if __name__ == "__main__":
    status_code, file_count = check()
    if status_code >= 0:
        print(f"SUCCESS: check total {file_count} files pass")
    else:
        print(f"ERROR: check total {file_count} files, failed. check log for detail")
    exit(status_code)
