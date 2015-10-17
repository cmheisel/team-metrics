#!/bin/bash
set -o nounset
set -o errexit

command -v tox >/dev/null 2>&1 || { echo >&2 "tox2travis requires tox but it's not installed. Aborting."; exit 1; }

if [ ! -f tox.ini ]; then
    echo "tox.ini not found. Aborting."
    exit 1
fi

echo "language: python"
echo "python: 2.7"
echo "env:"

for env in $(tox -l); do
    echo "  - TOX_ENV=${env}"
done

echo "install:"
echo "  - pip install tox"

echo "script:"
echo "  - tox -e \$TOX_ENV"
