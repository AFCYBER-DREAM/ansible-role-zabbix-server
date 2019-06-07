ansible-role-zabbix-server
=========
[![Build Status](https://travis-ci.com/AFCYBER-DREAM/ansible-role-zabbix-server.svg?branch=master)](https://travis-ci.com/AFCYBER-DREAM/ansible-role-zabbix-server)

Deploys a zabbix server and web front end

Requirements
------------

This role requires a number of additional roles to deploy
- ansible-role-packages
- ansible-role-repositories
- ansible-role-apache

A mysql database will be needed to deploy

Role Variables
--------------
### List of configurable variables

There are many different options that can be modified depending on the use. Listed are the minimum that are required to have a functional sever

    - zabbix_server_dbhostname: 
        Hostname of the Database server
    - zabbix_server_dbuser: 
        Database username
    - zabbix_server_dbpassword: 
        Database password
    - zabbix_url:
        URL to Access the zabbix web interface


SELinux variables: 

SELinux configuration is the standard option if you are deploying on RHEL/CentOS based systems. All of the options are defined in the defaults along with a TE files that is require for proper usage. The ports defined here are also used to configure the firewall. 

```
zabbix_security:
  selinux_te_files:
    - {name: "zabbix_sock", version: "1.0", te_file: "zabbix_sock.te"}
  security_ports:
    - {port: 3306, protocol: 'tcp', port_type: 'mysqld_port_t'}
  sebooleans:
    - {name: 'httpd_can_network_connect_db', state: yes}
    - {name: "httpd_can_connect_zabbix", state: yes}
    - {name: "daemons_enable_cluster_mode", state: yes}
    - {name: "zabbix_can_network", state: yes}
```

Example Playbook
----------------

    - hosts: zabbix-servers
      roles:
         - { role: ansible-role-zabbix }

License
-------

MIT

Author Information
------------------
The Development Range Engineering, Architecture, and Modernization (DREAM) Team