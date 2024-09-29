from testcontainers.opensearch import OpenSearchContainer

import pytest


@pytest.fixture(autouse=True)
def disable_logging():
    import logging
    import warnings

    warnings.filterwarnings("ignore")
    logging.getLogger("opensearch").setLevel(logging.CRITICAL)

    yield
    warnings.resetwarnings()
    logging.getLogger("opensearch").setLevel(logging.NOTSET)


def test_docker_run_opensearch():
    with OpenSearchContainer() as opensearch:
        client = opensearch.get_client()
        assert client.cluster.health()["status"] == "green"


def test_docker_run_opensearch_with_security():
    with OpenSearchContainer(security_enabled=True) as opensearch:
        client = opensearch.get_client()
        assert client.cluster.health()["status"] == "green"


def test_docker_run_opensearch_v1():
    with OpenSearchContainer(image="opensearchproject/opensearch:1.3.6") as opensearch:
        client = opensearch.get_client()
        assert client.cluster.health()["status"] == "green"


def test_docker_run_opensearch_v1_with_security():
    with OpenSearchContainer(image="opensearchproject/opensearch:1.3.6", security_enabled=True) as opensearch:
        client = opensearch.get_client()
        assert client.cluster.health()["status"] == "green"


def test_docker_run_opensearch_v2_12():
    with OpenSearchContainer(
        image="opensearchproject/opensearch:2.12.0", initial_admin_password="Testing!#345"
    ) as opensearch:
        client = opensearch.get_client()
        assert client.cluster.health()["status"] == "green"


def test_search():
    with OpenSearchContainer() as opensearch:
        client = opensearch.get_client()
        client.index(index="test", body={"test": "test"})
        client.indices.refresh(index="test")
        result = client.search(index="test", body={"query": {"match_all": {}}})
        assert result["hits"]["total"]["value"] == 1
