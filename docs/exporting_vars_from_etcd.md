# Exporting Vars from ETCD

This file will explain how to export key-vars from etcd using this script

## Requirements

- Start a ETCD server on port 2379
- Libraries:
	- python-etcd
	- python-click
- Previously populated ETCD

## Help & Verbose

The script has verbose mode, just add -v after the script execution, as follows

```
python etcd_var_parser.py -v export --help

Usage: etcd_var_parser.py export [OPTIONS]

Options:
  -t, --file-type [yml|sh]  File type to load
  -o, --output-file TEXT    Output File
  --help                    Show this message and exit.
```

## How to Export ETCD Content?

- Input

```
python etcd_var_parser.py -v export -t yml -o output/test.yml
```

- Output

```
Verbose mode is on
File Type: yml
Ouput File: output/test.yml

Start Logging
ETCD:
{u'IPAM_network': u'10.38.52.0/18',
 u'add_host_availability_zone': u'True',
 u'admin_user': u'admin',
 u'availability_zones': {u'HA_LAB_1': {u'availability_zone': u'EL_FAP-I-1',
                                       u'name': u'HA_FAP_1'},
                         u'HA_LAB_2': {u'availability_zone': u'EL_FAP-I-2',
                                       u'name': u'HA_FAP_2'},
                         u'HA_LAB_3': {u'availability_zone': u'EL_FAP-I-3',
                                       u'name': u'HA_FAP_3'},
                         u'HA_LAB_4': {u'0': u'100.130.130.22',
                                       u'1': u'100.130.130.23',
                                       u'2': u'100.130.130.24',
                                       u'3': u'100'}},
 u'country': u'es',
 u'create_availability_zones': u'True',
 u'default_password': u'test01',
 u'emergency_user': u'sos1',
 u'environment_variables': {u'CINDER_ENDPOINT_TYPE': u'internalURL',
                            u'OS_AUTH_URL': u'http://{{ internal_vip }}:35357/v2.0',
                            u'OS_ENDPOINT_TYPE': u'internal',
                            u'OS_PASSWORD': u'{{ admin_password }}',
                            u'OS_PROJECT_NAME': u'admin',
                            u'OS_REGION_NAME': u'RegionOne',
                            u'OS_TENANT_NAME': u'admin',
                            u'OS_USERNAME': u'admin',
                            u'OS_VOLUME_API_VERSION': u'2'},
 u'external_haproxy_enabled': u'True',
 u'keystone_apache_wsgi': u'False',
 u'netapp_cinder_backup_shares': {u'0': u'10.38.52.32:/TESTBCK_ES_CLOUD_'},
 u'netapp_cinder_shares': {u'0': u'10.38.52.22:/TEST01_ES_CLOUD_cinder1',
                           u'1': u'10.38.52.21:/TEST02_ES_CLOUD_cinder1',
                           u'2': u'10.38.52.24:/TEST03_ES_CLOUD_cinder1'},
 u'netapp_glance_shares': {u'share1': {u'name': u'NetApp1',
                                       u'path': u'/var/lib/glance/images',
                                       u'type': u'nfs',
                                       u'url': u'10.38.52.33:/VES1T0Z1_ES_CLOUD_glance'}},
 u'netapp_storage_protocol': u'nfs',
 u'new_installation': u'True',
 u'ns_infoblox_group': u'DNS_GRID',
 u'ntp_clients_ip': {u'0': u'20.48.26.11'},
 u'reverse_zone': u'48.20.in-addr.arpa',
 u'ssl_enabled': u'True',
 u'ssl_horizon_enabled': u'True'}

File Generated: output/test.yml

```

- Logfile

```
2017-07-18 15:26:24,704 root  INFO     Etcd Parsing started...
2017-07-18 15:26:24,708 root  INFO     ETCD Key-Value Map:
2017-07-18 15:26:24,708 root  INFO     {u'netapp_glance_shares': {u'share1': {u'url': u'10.38.52.33:/VES1T0Z1_ES_CLOUD_glance', u'path': u'/var/lib/glance/images', u'type': u'nfs', u'name': u'NetApp1'}}, u'netapp_cinder_shares': {u'1': u'10.38.52.21:/TEST02_ES_CLOUD_cinder1', u'0': u'10.38.52.22:/TEST01_ES_CLOUD_cinder1', u'2': u'10.38.52.24:/TEST03_ES_CLOUD_cinder1'}, u'availability_zones': {u'HA_LAB_4': {u'1': u'100.130.130.23', u'0': u'100.130.130.22', u'3': u'100', u'2': u'100.130.130.24'}, u'HA_LAB_1': {u'name': u'HA_FAP_1', u'availability_zone': u'EL_FAP-I-1'}, u'HA_LAB_2': {u'name': u'HA_FAP_2', u'availability_zone': u'EL_FAP-I-2'}, u'HA_LAB_3': {u'name': u'HA_FAP_3', u'availability_zone': u'EL_FAP-I-3'}}, u'ssl_horizon_enabled': u'True', u'new_installation': u'True', u'reverse_zone': u'48.20.in-addr.arpa', u'country': u'es', u'add_host_availability_zone': u'True', u'ns_infoblox_group': u'DNS_GRID', u'create_availability_zones': u'True', u'netapp_storage_protocol': u'nfs', u'admin_user': u'admin', u'IPAM_network': u'10.38.52.0/18', u'external_haproxy_enabled': u'True', u'environment_variables': {u'OS_PROJECT_NAME': u'admin', u'OS_USERNAME': u'admin', u'OS_VOLUME_API_VERSION': u'2', u'OS_TENANT_NAME': u'admin', u'OS_AUTH_URL': u'http://{{ internal_vip }}:35357/v2.0', u'OS_ENDPOINT_TYPE': u'internal', u'OS_REGION_NAME': u'RegionOne', u'CINDER_ENDPOINT_TYPE': u'internalURL', u'OS_PASSWORD': u'{{ admin_password }}'}, u'default_password': u'test01', u'keystone_apache_wsgi': u'False', u'ssl_enabled': u'True', u'emergency_user': u'sos1', u'ntp_clients_ip': {u'0': u'20.48.26.11'}, u'netapp_cinder_backup_shares': {u'0': u'10.38.52.32:/TESTBCK_ES_CLOUD_'}}
2017-07-18 15:26:24,712 root  INFO
2017-07-18 15:26:24,712 root  INFO     File Generated: output/test.yml
```
