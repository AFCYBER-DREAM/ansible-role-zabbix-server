import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('zabbix')


def test_zabbix_server_running_and_enabled(host):

    zabbix = host.service("zabbix-server")
    assert zabbix.is_enabled
    assert zabbix.is_running


@pytest.mark.parametrize("server", [("zabbix-server-mysql")])
def test_zabbix_package(server, host):

    zabbix_server = host.package(server)
    assert zabbix_server.version.startswith("4.2")
    assert zabbix_server.is_installed


def test_zabbix_server_dot_conf(host):

    zabbix_server_conf = host.file("/etc/zabbix/zabbix_server.conf")

    assert zabbix_server_conf.user == "zabbix"
    assert zabbix_server_conf.group == "zabbix"
    assert zabbix_server_conf.mode == 0o640

    assert zabbix_server_conf.contains("ListenPort=10051")
    assert zabbix_server_conf.contains("DebugLevel=3")


def test_zabbix_include_dir(host):

    zabbix_include_dir = host.file("/etc/zabbix/zabbix_server.conf.d")

    assert zabbix_include_dir.is_directory
    assert zabbix_include_dir.user == "zabbix"
    assert zabbix_include_dir.group == "zabbix"
    # assert zabbix_include_dir.mode == 0o644


def test_zabbix_server_connect_connection(host):

    zabbix_server_socket = host.socket('tcp://10050')
    zabbix_agent_socket = host.socket('tcp://10051')

    assert zabbix_server_socket.is_listening
    assert zabbix_agent_socket.is_listening


def test_zabbix_web_interface(host):

    zabbix_web = host.socket('tcp://80')

    assert zabbix_web.is_listening
