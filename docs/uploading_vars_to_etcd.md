# Uploading Vars to ETCD

This file will explain how to upload vars to etcd using this script

## Requirements

- Start a ETCD server on port 2379
- Libraries:
	- python-etcd
	- python-click

## Help & Verbose

The script has verbose mode, just add -v after the script execution, as follows

```
> python etcd_var_parser.py -v upload --help 

Usage: etcd_var_parser.py upload [OPTIONS] ENTRYFILE

Options:
  -t, --file-type [yml|sh]  File type to load
  -p, --prefix TEXT         Top Namespace to upload yaml tree
  -f, --force               Override the ETCD parameters
  --help                    Show this message and exit.
```

## How to Upload Content to ETCD?

- Input

```
python etcd_var_parser.py -v upload -t sh samples/sample_params_file.cfg
python etcd_var_parser.py -v upload -t yml samples/example.yaml
```

- Output[1]

```
Verbose mode is on
File Type: sh
Entryfile: samples/sample_params_file.cfg

Uploading parameters from Bash file...
Start Logging
Reading parameters file...
Logging parameters
Adding - Key: SAMPLE/REPO_SERVER Value: ${INBAND_MGMT_NET}.72
Adding - Key: SAMPLE/DOMAIN Value: example.com
Adding - Key: SAMPLE/VIP_DB Value: ${OS_CTL_NET}.43
Adding - Key: SAMPLE/OS_CTL_NET Value: 10.11.0
Adding - Key: SAMPLE/VIP_LDAP Value: ${INBAND_MGMT_NET}.44
Adding - Key: SAMPLE/VIP_SDN Value: ${INBAND_MGMT_NET}.230
Adding - Key: SAMPLE/VIP_FRONTEND Value: ${INBAND_MGMT_NET}.101
Adding - Key: SAMPLE/LDAP_URL Value: ldap://$VIP_LDAP
Adding - Key: SAMPLE/TOP_NS Value: 'SAMPLE'
Adding - Key: SAMPLE/PROXY Value: 22.74.135.87:80
Adding - Key: SAMPLE/PUBLIC_DOMAIN Value: public.example.com
Adding - Key: SAMPLE/INBAND_MGMT_NET Value: 10.10.128
Done!
```

- Output[2]

```
Verbose mode is on
File Type: yml
Entryfile: samples/example.yaml

Uploading parameters from YML file...
Start Logging
Reading parameters file...
Logging parameters

Adding - Key: /data/netapp_glance_shares/share1/url Value: 10.38.52.33:/VES1T0Z1_ES_CLOUD_glance
Adding - Key: /data/netapp_glance_shares/share1/path Value: /var/lib/glance/images
Adding - Key: /data/netapp_cinder_shares/1 Value: 10.38.52.21:/TEST02_ES_CLOUD_cinder1
Adding - Key: /data/netapp_cinder_shares/2 Value: 10.38.52.24:/TEST03_ES_CLOUD_cinder1
Adding - Key: /data/availability_zones/HA_LAB_4/1 Value: 100.130.130.23
Adding - Key: /data/availability_zones/HA_LAB_4/2 Value: 100.130.130.24
Adding - Key: /data/availability_zones/HA_LAB_4/3 Value: 100
Adding - Key: /data/availability_zones/HA_LAB_3/availability_zone Value: EL_FAP-I-3
Adding - Key: /data/default_password Value: test01
Adding - Key: /data/ssl_enabled Value: True
Adding - Key: /data/emergency_user Value: sos1
Done!
-- Output simplified --
```

- Logfile

```
2017-07-18 12:37:57,829 root  INFO     Etcd Parsing started...
2017-07-18 12:37:57,829 root  INFO     Reading parameters file samples/example.yaml
2017-07-18 12:37:57,835 root  INFO     /data/netapp_glance_shares/share1/url = 10.38.52.33:/VES1T0Z1_ES_CLOUD_glance
2017-07-18 12:37:57,838 root  INFO     /data/netapp_glance_shares/share1/path = /var/lib/glance/images
2017-07-18 12:37:57,843 root  INFO     /data/netapp_glance_shares/share1/type = nfs
2017-07-18 12:37:57,847 root  INFO     /data/netapp_glance_shares/share1/name = NetApp1
2017-07-18 12:37:57,849 root  INFO     Folder: /data/netapp_cinder_shares/0
2017-07-18 12:37:57,850 root  INFO     Folder: /data/netapp_cinder_shares/1
2017-07-18 12:37:57,854 root  INFO     /data/admin_user = admin
2017-07-18 12:37:57,857 root  INFO     /data/reverse_zone = 48.20.in-addr.arpa
2017-07-18 12:37:57,860 root  INFO     Folder: /data/ntp_clients_ip/0
2017-07-18 12:37:57,861 root  INFO     /data/ns_infoblox_group = DNS_GRID
2017-07-18 12:37:57,863 root  INFO     /data/create_availability_zones = True
2017-07-18 12:37:57,879 root  INFO     Folder: /data/availability_zones/HA_LAB_4/1
2017-07-18 12:37:57,882 root  INFO     Folder: /data/availability_zones/HA_LAB_4/2
2017-07-18 12:37:57,884 root  INFO     Folder: /data/availability_zones/HA_LAB_4/3
2017-07-18 12:37:57,885 root  INFO     /data/availability_zones/HA_LAB_1/name = HA_FAP_1
2017-07-18 12:37:57,898 root  INFO     /data/availability_zones/HA_LAB_3/availability_zone = EL_FAP-I-3
2017-07-18 12:37:57,900 root  INFO     /data/external_haproxy_enabled = True
2017-07-18 12:37:57,901 root  INFO     /data/add_host_availability_zone = True
2017-07-18 12:37:57,913 root  INFO     /data/environment_variables/OS_TENANT_NAME = admin
2017-07-18 12:37:57,915 root  INFO     /data/environment_variables/OS_AUTH_URL = http://{{ internal_vip }}:35357/v2.0
2017-07-18 12:37:57,935 root  INFO     /data/default_password = test01
2017-07-18 12:37:57,937 root  INFO     /data/ssl_enabled = True
2017-07-18 12:37:57,940 root  INFO     /data/emergency_user = sos1
```
