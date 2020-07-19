#!/bin/bash

set -x -e

CI=true antora antora-playbook.yml

if [[ "$1" = "test" ]]; then
    cd build/site
    python3 -m http.server
fi

