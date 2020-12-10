"""Tests related to sync ansible plugin collection content type."""
import os
import unittest

import pytest

from pulpcore.client.pulp_ansible import (
    ContentCollectionVersionsApi,
    DistributionsAnsibleApi,
    PulpAnsibleGalaxyApiCollectionsApi,
    RepositoriesAnsibleApi,
    RepositorySyncURL,
    RemotesCollectionApi,
)
from pulp_smash.pulp3.utils import gen_distribution, gen_repo

from pulp_ansible.tests.functional.constants import (
    ANSIBLE_DEMO_COLLECTION_REQUIREMENTS as DEMO_REQUIREMENTS,
    ANSIBLE_COLLECTION_REQUIREMENT,
    GALAXY_ANSIBLE_BASE_URL,
)
from pulp_ansible.tests.functional.utils import SyncHelpersMixin
from pulp_ansible.tests.functional.utils import gen_ansible_client, gen_ansible_remote, monitor_task
from pulp_ansible.tests.functional.utils import set_up_module as setUpModule  # noqa:F401


@unittest.skipUnless(
    "AUTOMATION_HUB_TOKEN_AUTH" in os.environ,
    "'AUTOMATION_HUB_TOKEN_AUTH' env var is not defined",
)
class AutomationHubV3SyncCase(unittest.TestCase, SyncHelpersMixin):
    """Test syncing from Pulp to Pulp."""

    @classmethod
    def setUpClass(cls):
        """Create class-wide variables."""
        cls.client = gen_ansible_client()
        cls.repo_api = RepositoriesAnsibleApi(cls.client)
        cls.remote_collection_api = RemotesCollectionApi(cls.client)
        cls.distributions_api = DistributionsAnsibleApi(cls.client)
        cls.collections_api = PulpAnsibleGalaxyApiCollectionsApi(cls.client)
        cls.cv_api = ContentCollectionVersionsApi(cls.client)

    def test_sync_with_token_from_automation_hub(self):
        """Test whether we can sync with an auth token from Automation Hub."""
        repo = self.repo_api.create(gen_repo())
        self.addCleanup(self.repo_api.delete, repo.pulp_href)

        aurl = "https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token"
        body = gen_ansible_remote(
            url="https://cloud.redhat.com/api/automation-hub/",
            requirements_file=ANSIBLE_COLLECTION_REQUIREMENT,
            auth_url=aurl,
            token=os.environ["AUTOMATION_HUB_TOKEN_AUTH"],
            tls_validation=False,
        )
        remote = self.remote_collection_api.create(body)
        self.addCleanup(self.remote_collection_api.delete, remote.pulp_href)

        repo = self._create_repo_and_sync_with_remote(remote)
        body = gen_distribution()
        body["repository"] = repo.pulp_href
        distribution_create = self.distributions_api.create(body)
        distribution_url = monitor_task(distribution_create.task)
        distribution = self.distributions_api.read(distribution_url[0])

        import pdb

        pdb.set_trace()

        # Check content of both repos.
        original_content = self.cv_api.list(repository_version=f"{repo.pulp_href}versions/1/")
        self.assertTrue(len(original_content.results) >= 3)  # check that we have at least 3 results


@unittest.skipUnless(
    "CI_AUTOMATION_HUB_TOKEN_AUTH" in os.environ,
    "'CI_AUTOMATION_HUB_TOKEN_AUTH' env var is not defined",
)
class AutomationHubCIV3SyncCase(unittest.TestCase, SyncHelpersMixin):
    """Test syncing from Pulp to Pulp."""

    @classmethod
    def setUpClass(cls):
        """Create class-wide variables."""
        cls.client = gen_ansible_client()
        cls.repo_api = RepositoriesAnsibleApi(cls.client)
        cls.remote_collection_api = RemotesCollectionApi(cls.client)
        cls.distributions_api = DistributionsAnsibleApi(cls.client)
        cls.collections_api = PulpAnsibleGalaxyApiCollectionsApi(cls.client)
        cls.cv_api = ContentCollectionVersionsApi(cls.client)
        cls.aurl = (
            "https://sso.qa.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token"
        )

    def test_mirror_from_automation_hub_ci_with_auth_token(self):
        """Test whether we can mirror from Automation Hub CI with an auth token."""
        body = gen_ansible_remote(
            url="https://ci.cloud.redhat.com/api/automation-hub/content/synctest/",
            auth_url=self.aurl,
            token=os.environ["CI_AUTOMATION_HUB_TOKEN_AUTH"],
            tls_validation=False,
        )
        remote = self.remote_collection_api.create(body)
        self.addCleanup(self.remote_collection_api.delete, remote.pulp_href)

        repo = self._create_repo_and_sync_with_remote(remote)

        # Assert at least one hundred CollectionVersions are returned
        content = self.cv_api.list(repository_version=f"{repo.pulp_href}versions/1/")
        self.assertTrue(len(content.results) >= 100)

    def test_sync_from_automation_hub_ci_with_auth_token_and_requirements_file(self):
        """Test sync from Automation Hub CI with an auth token and requirements file."""
        name = "collection_dep_a_fdqqyxou"
        namespace = "autohubtest2"
        body = gen_ansible_remote(
            url="https://ci.cloud.redhat.com/api/automation-hub/",
            requirements_file=f"collections:\n  - {namespace}.{name}",
            auth_url=self.aurl,
            token=os.environ["CI_AUTOMATION_HUB_TOKEN_AUTH"],
            tls_validation=False,
        )
        remote = self.remote_collection_api.create(body)
        self.addCleanup(self.remote_collection_api.delete, remote.pulp_href)

        repo = self._create_repo_and_sync_with_remote(remote)

        # Assert that at least one CollectionVersion was downloaded
        content = self.cv_api.list(repository_version=f"{repo.pulp_href}versions/1/")
        self.assertTrue(len(content.results) >= 1)

    def test_install_collection_with_invalid_token_from_automation_hub_ci(self):
        """Test whether we can mirror from Automation Hub CI with an invalid auth token."""
        body = gen_ansible_remote(
            url="https://ci.cloud.redhat.com/api/automation-hub/content/synctest/",
            auth_url=self.aurl,
            token="invalid token string",
            tls_validation=False,
        )
        remote = self.remote_collection_api.create(body)
        self.addCleanup(self.remote_collection_api.delete, remote.pulp_href)

        repo = self._create_repo_and_sync_with_remote(remote)

        # Assert that the sync did not produce a new repository version
        self.assertEqual(repo.latest_version_href, f"{repo.pulp_href}versions/0/")
