#!/bin/bash

count_csv() {
    local IFS=,
    local -a arr=($1)
    echo "${#arr[@]}"
}