# InitPyRepo
some style-check config for Python Repo

# Usage

```bash
git clone https://github.com/oneflyingfish/InitPyRepo.git

# check if override your exist files first, .git,README.md,.gitignore are auto ignore
rsync -a --exclude={.git,README.md,.gitignore} InitPyRepo/ $your_repo_path/
```

# Env

```bash
pip install pre-commit
pre-commit install

# run check
pre-commit
```