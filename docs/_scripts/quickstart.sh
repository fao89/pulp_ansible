# This script will execute the component scripts and ensure that the documented examples
# work as expected.

# THIS SCRIPT CURRENTLY MUST BE RUN IN A PULPLIFT DEVELOPMENT ENVIRONMENT
# TODO: remove the usage of pulp-devel bash functions so they can be directly modified
# for user environments.

# From the _scripts directory, run with `source quickstart.sh` (source to preserve the environment
# variables)
source setup.sh

echo "Role - Workflows"
source repo.sh
source remote.sh
source sync.sh

echo "Collection - Workflows"
source repo.sh cfoo
source remote-collection.sh
source sync.sh
