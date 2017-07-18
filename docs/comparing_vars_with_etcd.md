# Comparing Vars with ETCD

This file will explain how to compare key-values with an entryfile and the content of etcd using this script

## Requirements

- Start a ETCD server on port 2379
- Libraries:
	- python-etcd
	- python-click
- Previously populated ETCD

## Help & Verbose

The script has verbose mode, just add -v after the script execution, as follows

```
> python etcd_var_parser.py -v compare

Usage: etcd_var_parser.py compare [OPTIONS] ENTRYFILE

Options:
  -t, --file-type [yml|sh]  File type to load
  --help                    Show this message and exit.
```

## How to compare?

This feature is implemented only with with yaml yet. This is an example about how to perform a comparision.

- Input

```
python etcd_var_parser.py compare -t yml samples/example.yaml
python etcd_var_parser.py -v compare -t yml samples/example.yaml
```

- Output[1] - Case: Comparision OK

```
Status: ETCD and YAML file are equal
```

- Output[1] - Case: Comparision NOK
```
Traceback (most recent call last):
  File "etcd_var_parser.py", line 429, in <module>
    cli(obj={})
  File "/usr/lib/python2.7/site-packages/click/core.py", line 722, in __call__
    return self.main(*args, **kwargs)
  File "/usr/lib/python2.7/site-packages/click/core.py", line 697, in main
    rv = self.invoke(ctx)
  File "/usr/lib/python2.7/site-packages/click/core.py", line 1066, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
  File "/usr/lib/python2.7/site-packages/click/core.py", line 895, in invoke
    return ctx.invoke(self.callback, **ctx.params)
  File "/usr/lib/python2.7/site-packages/click/core.py", line 535, in invoke
    return callback(*args, **kwargs)
  File "/usr/lib/python2.7/site-packages/click/decorators.py", line 17, in new_func
    return f(get_current_context(), *args, **kwargs)
  File "etcd_var_parser.py", line 388, in compare
    raise ValueError('Yaml and ETCD not contain the same data')
ValueError: Yaml and ETCD not contain the same data
```

- Output[2] Verbose Mode

```
Verbose mode is on
File Type: yml
Entryfile: samples/example.yaml

Start Logging
Reading parameters file...
Adding - Key: /_compare/netapp_glance_shares/share1/url Value: 10.38.52.33:/VES1T0Z1_ES_CLOUD_glance
Adding - Key: /_compare/netapp_glance_shares/share1/path Value: /var/lib/glance/images
Adding - Key: /_compare/netapp_glance_shares/share1/type Value: nfs
Adding - Key: /_compare/netapp_glance_shares/share1/name Value: NetApp1
Adding - Key: /_compare/netapp_cinder_shares/0 Value: 10.38.52.22:/TEST01_ES_CLOUD_cinder1
Adding - Key: /_compare/netapp_cinder_shares/1 Value: 10.38.52.21:/TEST02_ES_CLOUD_cinder1
Adding - Key: /_compare/netapp_cinder_shares/2 Value: 10.38.52.24:/TEST03_ES_CLOUD_cinder1
Adding - Key: /_compare/admin_user Value: admin
Adding - Key: /_compare/reverse_zone Value: 48.20.in-addr.arpa
Adding - Key: /_compare/ntp_clients_ip/0 Value: 20.48.26.11
Adding - Key: /_compare/ns_infoblox_group Value: DNS_GRID
Adding - Key: /_compare/create_availability_zones Value: True
Adding - Key: /_compare/IPAM_network Value: 10.38.52.0/18
Adding - Key: /_compare/netapp_storage_protocol Value: nfs
Adding - Key: /_compare/keystone_apache_wsgi Value: False
Adding - Key: /_compare/ssl_horizon_enabled Value: True
Adding - Key: /_compare/new_installation Value: True
Adding - Key: /_compare/availability_zones/HA_LAB_4/0 Value: 100.130.130.22
Adding - Key: /_compare/availability_zones/HA_LAB_4/1 Value: 100.130.130.23
Adding - Key: /_compare/availability_zones/HA_LAB_4/2 Value: 100.130.130.24
Adding - Key: /_compare/availability_zones/HA_LAB_4/3 Value: 100
Adding - Key: /_compare/availability_zones/HA_LAB_1/name Value: HA_FAP_1
Adding - Key: /_compare/availability_zones/HA_LAB_1/availability_zone Value: EL_FAP-I-1
Adding - Key: /_compare/availability_zones/HA_LAB_2/name Value: HA_FAP_2
Adding - Key: /_compare/availability_zones/HA_LAB_2/availability_zone Value: EL_FAP-I-2
Adding - Key: /_compare/availability_zones/HA_LAB_3/name Value: HA_FAP_3
Adding - Key: /_compare/availability_zones/HA_LAB_3/availability_zone Value: EL_FAP-I-3
Adding - Key: /_compare/external_haproxy_enabled Value: True
Adding - Key: /_compare/add_host_availability_zone Value: True
Adding - Key: /_compare/netapp_cinder_backup_shares/0 Value: 10.38.52.32:/TESTBCK_ES_CLOUD_
Adding - Key: /_compare/country Value: es
Adding - Key: /_compare/environment_variables/OS_USERNAME Value: admin
Adding - Key: /_compare/environment_variables/OS_VOLUME_API_VERSION Value: 2
Adding - Key: /_compare/environment_variables/OS_TENANT_NAME Value: admin
Adding - Key: /_compare/environment_variables/OS_AUTH_URL Value: http://{{ internal_vip }}:35357/v2.0
Adding - Key: /_compare/environment_variables/OS_ENDPOINT_TYPE Value: internal
Adding - Key: /_compare/environment_variables/OS_REGION_NAME Value: RegionOne
Adding - Key: /_compare/environment_variables/CINDER_ENDPOINT_TYPE Value: internalURL
Adding - Key: /_compare/environment_variables/OS_PROJECT_NAME Value: admin
Adding - Key: /_compare/environment_variables/OS_PASSWORD Value: {{ admin_password }}
Adding - Key: /_compare/default_password Value: test01
Adding - Key: /_compare/ssl_enabled Value: True
Adding - Key: /_compare/emergency_user Value: sos1
Deleting - Key: /_compare/

YAML:
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

Status: ETCD and YAML file are equal
```
