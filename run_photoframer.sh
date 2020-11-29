#!/bin/bash

function fail {
    printf '%s\n' "$1" >&2  ## Send message to stderr. Exclude >&2 if you don't want it that way.
    exit "${2-1}"  ## Return a code specified by $2 or 1 by default.
}

cd "$(dirname "$0")" || fail "Exit program" # go current dir
source ./venv/bin/activate
python3 ./main.py