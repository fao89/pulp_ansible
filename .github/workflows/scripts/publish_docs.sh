#!/bin/bash

# WARNING: DO NOT EDIT!
#
# This file was generated by plugin_template, and is managed by it. Please use
# './plugin-template --github pulp_ansible' to update this file.
#
# For more info visit https://github.com/pulp/plugin_template

set -euv

# make sure this script runs at the repo root
cd "$(dirname "$(realpath -e "$0")")"/../../..

mkdir ~/.ssh
touch ~/.ssh/pulp-infra
chmod 600 ~/.ssh/pulp-infra
echo "$PULP_DOCS_KEY" > ~/.ssh/pulp-infra

echo "docs.pulpproject.org,8.43.85.236 ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBGXG+8vjSQvnAkq33i0XWgpSrbco3rRqNZr0SfVeiqFI7RN/VznwXMioDDhc+hQtgVhd6TYBOrV07IMcKj+FAzg=" >> /home/runner/.ssh/known_hosts
chmod 644 /home/runner/.ssh/known_hosts

pip3 install packaging

export PYTHONUNBUFFERED=1
export DJANGO_SETTINGS_MODULE=pulpcore.app.settings
export PULP_SETTINGS=$PWD/.ci/ansible/settings/settings.py
export WORKSPACE=$PWD

eval "$(ssh-agent -s)" #start the ssh agent
ssh-add ~/.ssh/pulp-infra

python3 .github/workflows/scripts/docs-publisher.py --build-type $1 --branch $2

if [[ "$GITHUB_WORKFLOW" == "Ansible changelog update" ]]; then
  # Do not build bindings docs on changelog update
  exit
fi

pip install mkdocs pymdown-extensions "Jinja2<3.1"

mkdir -p ../bindings
tar -xvf python-client-docs.tar --directory ../bindings
cd ../bindings
cat >> mkdocs.yml << DOCSYAML
---
site_name: PulpAnsible Client
site_description: Ansible bindings
site_author: Pulp Team
site_url: https://docs.pulpproject.org/pulp_ansible_client/
repo_name: pulp/pulp_ansible
repo_url: https://github.com/pulp/pulp_ansible
theme: readthedocs
DOCSYAML

# Building the bindings docs
mkdocs build

# publish to docs.pulpproject.org/pulp_ansible_client
rsync -avzh site/ doc_builder_pulp_ansible@docs.pulpproject.org:/var/www/docs.pulpproject.org/pulp_ansible_client/

# publish to docs.pulpproject.org/pulp_ansible_client/en/{release}
rsync -avzh site/ doc_builder_pulp_ansible@docs.pulpproject.org:/var/www/docs.pulpproject.org/pulp_ansible_client/en/"$2"
