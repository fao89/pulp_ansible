#!/bin/bash

# WARNING: DO NOT EDIT!
#
# This file was generated by plugin_template, and is managed by it. Please use
# './plugin-template --github pulp_ansible' to update this file.
#
# For more info visit https://github.com/pulp/plugin_template

set -euv

# make sure this script runs at the repo root
cd "$(dirname "$(realpath -e "$0")")"/../..

pip install twine

export REPORTED_VERSION=$(http pulp/pulp/api/v3/status/ | jq --arg plugin ansible -r '.versions[] | select(.component == $plugin) | .version')
export DESCRIPTION="$(git describe --all --exact-match `git rev-parse HEAD`)"
if [[ $DESCRIPTION == 'tags/'$REPORTED_VERSION ]]; then
  export VERSION=${REPORTED_VERSION}
else
  # Daily publishing of development version (ends in ".dev" reported as ".dev0")
  if [ "${REPORTED_VERSION%.dev*}" == "${REPORTED_VERSION}" ]; then
    echo "Refusing to publish bindings. $REPORTED_VERSION does not contain 'dev'."
    exit 1
  fi
  export EPOCH="$(date +%s)"
  export VERSION=${REPORTED_VERSION}${EPOCH}
fi

export response=$(curl --write-out %{http_code} --silent --output /dev/null https://pypi.org/project/pulp-ansible-client/$VERSION/)

if [ "$response" == "200" ];
then
  exit
fi

cd ../pulp-openapi-generator

./generate.sh pulp_ansible python $VERSION
cd pulp_ansible-client
python setup.py sdist bdist_wheel --python-tag py3
twine check dist/* || exit 1
twine upload dist/* -u pulp -p $PYPI_PASSWORD
exit $?
