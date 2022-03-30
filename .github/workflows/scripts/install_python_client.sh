#!/bin/bash

# WARNING: DO NOT EDIT!
#
# This file was generated by plugin_template, and is managed by it. Please use
# './plugin-template --github pulp_ansible' to update this file.
#
# For more info visit https://github.com/pulp/plugin_template

set -euv

export PULP_URL="${PULP_URL:-https://pulp}"

# make sure this script runs at the repo root
cd "$(dirname "$(realpath -e "$0")")"/../../..

pip install twine wheel

export REPORTED_VERSION=$(http $PULP_URL/pulp/api/v3/status/ | jq --arg plugin ansible --arg legacy_plugin pulp_ansible -r '.versions[] | select(.component == $plugin or .component == $legacy_plugin) | .version')
export DESCRIPTION="$(git describe --all --exact-match `git rev-parse HEAD`)"
if [[ $DESCRIPTION == 'tags/'$REPORTED_VERSION ]]; then
  export VERSION=${REPORTED_VERSION}
else
  export EPOCH="$(date +%s)"
  export VERSION=${REPORTED_VERSION}${EPOCH}
fi

export response=$(curl --write-out %{http_code} --silent --output /dev/null https://pypi.org/project/pulp-ansible-client/$VERSION/)

if [ "$response" == "200" ];
then
  echo "pulp_ansible client $VERSION has already been released. Installing from PyPI."
  pip install pulp-ansible-client==$VERSION
  mkdir -p dist
  tar cvf python-client.tar ./dist
  exit
fi

cd ../pulp-openapi-generator
rm -rf pulp_ansible-client
./generate.sh pulp_ansible python $VERSION
cd pulp_ansible-client
python setup.py sdist bdist_wheel --python-tag py3
find . -name "*.whl" -exec pip install {} \;
tar cvf ../../pulp_ansible/python-client.tar ./dist

find ./docs/* -exec sed -i 's/Back to README/Back to HOME/g' {} \;
find ./docs/* -exec sed -i 's/README//g' {} \;
cp README.md docs/index.md
sed -i 's/docs\///g' docs/index.md
find ./docs/* -exec sed -i 's/\.md//g' {} \;
tar cvf ../../pulp_ansible/python-client-docs.tar ./docs
exit $?
