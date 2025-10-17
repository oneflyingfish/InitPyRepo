#!/bin/bash

# only make sense to file in git stage erea
python test/test_python_style.py  --only_check=false  --contain_stage=true --contain_commit=true