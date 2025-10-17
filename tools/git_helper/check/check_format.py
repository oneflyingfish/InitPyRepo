from pathlib import Path
import black
import os


def check_format(files, only_check=True):
    ok = True

    if isinstance(files, str):
        files = [files]

    for file in files:
        if not os.path.exists(file):
            continue
        content = Path(file).read_text(encoding="utf-8")
        mode = black.FileMode()  # default line_length=88
        try:
            content_format = black.format_file_contents(content, fast=False, mode=mode)
        except black.NothingChanged:
            continue
        except Exception as e:
            print(f"{files} may meet syntax error: {e}")

        if only_check:
            ok = False
            print(f"{file} need to format as:")
            print(f">>>>>>>>>>>> start {file} >>>>>>>>>>>>>>>>")
            print(content_format)
            print(f"<<<<<<<<<<<< end {file} <<<<<<<<<<<<<<<<\n")
        else:
            try:
                Path(file).write_text(content_format, encoding="utf-8")
            except Exception as e:
                ok = False
                print(f"{file} need to format, fail to fix auto: {e}")
            print(f"AUTO: format {file} to google style")
    return ok
