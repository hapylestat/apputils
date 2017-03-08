#!/usr/bin/env bash

pip install twine

cat > ~.piprc <<< EOF
[distutils]
index-servers = pypi

[pypi]
username=${USER}
password=${PASS}
EOF

