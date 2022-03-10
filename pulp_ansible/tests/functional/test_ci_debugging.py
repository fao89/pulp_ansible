"""Tests related to sync ansible plugin collection content type."""
import os
import unittest
import requests

from pulpcore.client.pulp_ansible import (
    AnsibleRepositorySyncURL,
    ContentCollectionVersionsApi,
    DistributionsAnsibleApi,
    PulpAnsibleApiV3CollectionsApi,
    RepositoriesAnsibleApi,
    RemotesCollectionApi,
)
from pulp_smash.pulp3.bindings import PulpTaskError, PulpTestCase

from pulp_ansible.tests.functional.utils import (
    gen_ansible_client,
    gen_ansible_remote,
    monitor_task,
    tasks,
)
from pulp_ansible.tests.functional.utils import SyncHelpersMixin, TestCaseUsingBindings
from pulp_ansible.tests.functional.utils import set_up_module as setUpModule  # noqa:F401

from pulp_smash import config

class SyncCollectionsFromPulpServerTestCase(TestCaseUsingBindings, SyncHelpersMixin):
    """
    Test whether one can sync collections from a Pulp server.

    This performs two sync's, the first uses the V2 API and galaxy.ansible.com. The second is from
    Pulp using the V3 API and uses the content brought in from the first sync.

    """

    def setUp(self):
        """Set up the Sync tests."""
        self.requirements_file = "collections:\n  - testing.k8s_demo_collection"
        body = gen_ansible_remote(
            url="https://galaxy.ansible.com",
            requirements_file=self.requirements_file,
            sync_dependencies=False,
        )
        self.remote = self.remote_collection_api.create(body)
        self.addCleanup(self.remote_collection_api.delete, self.remote.pulp_href)

        self.first_repo = self._create_repo_and_sync_with_remote(self.remote)
        self.distribution = self._create_distribution_from_repo(self.first_repo)

    def test_sync_collections_from_pulp(self):
        """Test sync collections from pulp server."""
        cfg = config.get_config()

        username = cfg.pulp_auth[0]
        password = cfg.pulp_auth[1]

        print(username)
        print(password)
        print(self.distribution.client_url)

        second_body = gen_ansible_remote(
            url=self.distribution.client_url,
            requirements_file=self.requirements_file,
            sync_dependencies=False,
            # include_pulp_auth=True,
            username=username,
            password=password
        )
        second_remote = self.remote_collection_api.create(second_body)
        self.addCleanup(self.remote_collection_api.delete, second_remote.pulp_href)

        url = self.distribution.client_url + "api/v3/collections/all"

        print(url)

        response = requests.get(url, auth=(username, password))
        print(response.content)

        print(response)

        # this is where shit always goes belly up
        second_repo = self._create_repo_and_sync_with_remote(second_remote)
