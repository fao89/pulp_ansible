from urllib.parse import urljoin

from pulp_smash.pulp3.constants import (
    BASE_DISTRIBUTION_PATH,
    BASE_PUBLISHER_PATH,
    BASE_REMOTE_PATH,
    BASE_REPO_PATH,
    BASE_CONTENT_PATH,
)


GALAXY_ANSIBLE_BASE_URL = "https://galaxy.ansible.com"

ANSIBLE_ROLE_NAME = "ansible.role"

ANSIBLE_ROLE_CONTENT_PATH = urljoin(BASE_CONTENT_PATH, "ansible/roles/")

ANSIBLE_COLLECTION_VERSION_CONTENT_PATH = urljoin(BASE_CONTENT_PATH, "ansible/collection_versions/")

ANSIBLE_DISTRIBUTION_PATH = urljoin(BASE_DISTRIBUTION_PATH, "ansible/ansible/")

ANSIBLE_REMOTE_PATH = urljoin(BASE_REMOTE_PATH, "ansible/role/")

ANSIBLE_REPO_PATH = urljoin(BASE_REPO_PATH, "ansible/ansible/")

ANSIBLE_PUBLISHER_PATH = urljoin(BASE_PUBLISHER_PATH, "ansible/ansible/")

ANSIBLE_GALAXY_URL = urljoin(GALAXY_ANSIBLE_BASE_URL, "api/v1/roles/")

NAMESPACE_ANSIBLE = "?namespace__name=ansible"

NAMESPACE_ELASTIC = "?namespace__name=elastic"

NAMESPACE_PULP = "?namespace__name=pulp"

NAMESPACE_TESTING = "?namespace__name=testing"

ANSIBLE_FIXTURE_URL = urljoin(ANSIBLE_GALAXY_URL, NAMESPACE_ANSIBLE)

ANSIBLE_PULP_FIXTURE_URL = urljoin(ANSIBLE_GALAXY_URL, NAMESPACE_PULP)

ANSIBLE_ELASTIC_FIXTURE_URL = urljoin(ANSIBLE_GALAXY_URL, NAMESPACE_ELASTIC)

ANSIBLE_ELASTIC_ROLE_NAMESPACE_NAME = "elastic.elasticsearch"

ANSIBLE_ELASTIC_ROLE = "elastic.elasticsearch,6.6.0"

ANSIBLE_FIXTURE_COUNT = 5

ANSIBLE_FIXTURE_CONTENT_SUMMARY = {ANSIBLE_ROLE_NAME: ANSIBLE_FIXTURE_COUNT}

# FIXME: replace this with the location of one specific content unit of your choosing
ANSIBLE_URL = urljoin(ANSIBLE_FIXTURE_URL, "")

ANSIBLE_COLLECTION_REMOTE_PATH = urljoin(BASE_REMOTE_PATH, "ansible/collection/")

ANSIBLE_DEMO_COLLECTION = "testing.k8s_demo_collection"

ANSIBLE_DEMO_COLLECTION_REQUIREMENTS = f"collections:\n  - {ANSIBLE_DEMO_COLLECTION}"

ANSIBLE_COLLECTION_CONTENT_NAME = "ansible.collection_version"

ANSIBLE_COLLECTION_FIXTURE_COUNT = 1

ANSIBLE_COLLECTION_FIXTURE_SUMMARY = {
    ANSIBLE_COLLECTION_CONTENT_NAME: ANSIBLE_COLLECTION_FIXTURE_COUNT
}

COLLECTION_METADATA = {"name": "k8s_demo_collection", "version": "0.0.3"}
"""Metadata was extracted from
https://galaxy.ansible.com/api/v2/collections/testing/k8s_demo_collection/versions/0.0.3/"""

ANSIBLE_COLLECTION_FILE_NAME = "testing-k8s_demo_collection-0.0.3.tar.gz"

ANSIBLE_COLLECTION_UPLOAD_FIXTURE_URL = urljoin(
    GALAXY_ANSIBLE_BASE_URL, f"download/{ANSIBLE_COLLECTION_FILE_NAME}"
)

ANSIBLE_COLLECTION_REQUIREMENT = """
---
collections:
- a10.acos_cli
- amazon.aws
- ansible.netcommon
- ansible.posix
- ansible.tower
- ansible.utils
- arista.avd
- arista.cvp
- arista.eos
- arubanetworks.aoscx
- azure.azcollection
- check_point.gaia
- check_point.mgmt
- chocolatey.chocolatey
- cisco.aci
- cisco.asa
- cisco.ios
- cisco.iosxr
- cisco.mso
- cisco.nxos
- cloud.common
- cyberark.conjur
- cyberark.conjur_collection
- cyberark.pas
- dellemc.enterprise_sonic
- dellemc.isilon
- dellemc.powermax
- dellemc.powerstore
- dynatrace_innovationlab.dynatrace_collection
- f5networks.f5_modules
- fortinet.fortios
- frr.frr
- google.cloud
- hpe.nimble
- hpe.oneview
- ibm.ibm_zos_core
- ibm.ibm_zos_ims
- ibm.power_aix
- ibm.power_ibmi
- ibm.power_vios
- ibm.qradar
- ibm.spectrum_virtualize
- infoblox.nios_modules
- junipernetworks.junos
- kubernetes.core
- netapp.aws
- netapp.azure
- netapp.elementsw
- netapp.ontap
- newrelic.newrelic_agents
- nginxinc.nginx_controller
- nginxinc.nginx_core
- nvidia.cumulus_linux_roles
- opensvc.cluster
- openvswitch.openvswitch
- phoenixnap.bmc
- pureport.fabric
- purestorage.flasharray
- purestorage.flashblade
- redhat.insights
- redhat.openshift
- redhat.satellite
- rubrikinc.cdm
- sensu.sensu_go
- splunk.enterprise_security
- splunk.es
- tirasa.syncope
- vmware.vmware_rest
- vyos.vyos
- wti.remote
"""
# - redhat.rhv
