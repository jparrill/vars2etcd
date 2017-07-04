# ETCD Var Parser
This script will parse your variables files to be uploaded on ETCD, supported formats:

- Shell
```
DOMAIN="example.com"
PUBLIC_DOMAIN="public.example.com"
PROXY="22.75.135.87:80"
OS_CTL_NET="10.10.0"
INBAND_MGMT_NET="10.10.128"
REPO_SERVER="${INBAND_MGMT_NET}.72"
VIP_FRONTEND="${INBAND_MGMT_NET}.101"
VIP_SDN="${INBAND_MGMT_NET}.230"
VIP_DB="${OS_CTL_NET}.43"
VIP_LDAP="${INBAND_MGMT_NET}.44"
LDAP_URL="ldap://$VIP_LDAP"
```

- Yaml
```
environment_variables:
  OS_REGION_NAME: RegionOne
  OS_VOLUME_API_VERSION: 2
  OS_ENDPOINT_TYPE: internal
  CINDER_ENDPOINT_TYPE: internalURL
  OS_USERNAME: admin
  OS_PASSWORD: "{{ admin_password }}"
  OS_PROJECT_NAME: admin
  OS_TENANT_NAME: admin
  OS_AUTH_URL: "http://{{ internal_vip }}:35357/v2.0"
create_availability_zones: True
availability_zones:
  HA_LAB_1:
    name: HA_FAP_1
    availability_zone: EL_FAP-I-1
  HA_LAB_2:
    name: HA_FAP_2
    availability_zone: EL_FAP-I-2
```


## How it works

### Requirements
- python-etcd
- python-click

### Execution

- Input

```
python etcd_var_parser.py --help
```

- Output

```
Usage: etcd_var_parser.py [OPTIONS] ENTRYFILE

Options:
  -v, --verbose             Debug mode
  -t, --file-type [yml|sh]  File type to load
  --help                    Show this message and exit.
```

#### Loading Yaml Vars

- Input

```
python etcd_var_parser.py -t yml samples/example.yaml -v
```

- Output

```
➜  vars2etcd git:(master) ✗ python etcd_var_parser.py -t yml example.yaml -v
Verbose mode On
File Type: yml
Entryfile: example.yaml

Start Logging
Reading parameters file...
Logging parameters
Adding - Key: /netapp_glance_shares/share1/url Value: 10.38.52.33:/VES1T0Z1_ES_CLOUD_glance
Adding - Key: /netapp_glance_shares/share1/path Value: /var/lib/glance/images
Adding - Key: /netapp_glance_shares/share1/type Value: nfs
Adding - Key: /netapp_glance_shares/share1/name Value: NetApp1
Creating folder /netapp_cinder_shares/10.38.52.22:/TEST01_ES_CLOUD_cinder1
Creating folder /netapp_cinder_shares/10.38.52.21:/TEST02_ES_CLOUD_cinder1
Creating folder /netapp_cinder_shares/10.38.52.24:/TEST03_ES_CLOUD_cinder1
Adding - Key: /admin_user Value: admin
Adding - Key: /reverse_zone Value: 48.20.in-addr.arpa
Creating folder /ntp_clients_ip/20.48.26.11
Adding - Key: /ns_infoblox_group Value: DNS_GRID
Adding - Key: /create_availability_zones Value: True
Adding - Key: /IPAM_network Value: 10.38.52.0/18
Adding - Key: /netapp_storage_protocol Value: nfs
...
...
```

- Logfile (etcd_parser.log)

```
2017-07-04 14:48:40,035 root  INFO     Etcd Parsing started...
2017-07-04 14:48:40,035 root  INFO     Reading parameters file example.yaml
2017-07-04 14:48:40,042 root  INFO     /netapp_glance_shares/share1/url = 10.38.52.33:/VES1T0Z1_ES_CLOUD_glance
2017-07-04 14:48:40,042 urllib3.connectionpool INFO     Starting new HTTP connection (1): 127.0.0.1
2017-07-04 14:48:40,046 root  INFO     /netapp_glance_shares/share1/path = /var/lib/glance/images
2017-07-04 14:48:40,048 root  INFO     /netapp_glance_shares/share1/type = nfs
2017-07-04 14:48:40,050 root  INFO     /netapp_glance_shares/share1/name = NetApp1
2017-07-04 14:48:40,052 root  INFO     Folder: /netapp_cinder_shares/10.38.52.22:/TEST01_ES_CLOUD_cinder1
2017-07-04 14:48:40,054 root  INFO     Folder: /netapp_cinder_shares/10.38.52.21:/TEST02_ES_CLOUD_cinder1
2017-07-04 14:48:40,056 root  INFO     Folder: /netapp_cinder_shares/10.38.52.24:/TEST03_ES_CLOUD_cinder1
2017-07-04 14:48:40,058 root  INFO     /admin_user = admin
2017-07-04 14:48:40,064 root  INFO     /reverse_zone = 48.20.in-addr.arpa
2017-07-04 14:48:40,066 root  INFO     Folder: /ntp_clients_ip/20.48.26.11
2017-07-04 14:48:40,068 root  INFO     /ns_infoblox_group = DNS_GRID
2017-07-04 14:48:40,070 root  INFO     /create_availability_zones = True
2017-07-04 14:48:40,071 root  INFO     /IPAM_network = 10.38.52.0/18
2017-07-04 14:48:40,074 root  INFO     /netapp_storage_protocol = nfs
2017-07-04 14:48:40,076 root  INFO     /keystone_apache_wsgi = False
2017-07-04 14:48:40,078 root  INFO     /ssl_horizon_enabled = True
2017-07-04 14:48:40,084 root  INFO     /new_installation = True
2017-07-04 14:48:40,086 root  INFO     /availability_zones/HA_LAB_1/name = HA_LAB_1
2017-07-04 14:48:40,088 root  INFO     /availability_zones/HA_LAB_1/availability_zone = TC_LAB-I-1
...
...
```

#### Loading Shell Vars

- Input

```
python etcd_var_parser.py -t sh samples/sample_params_file.cfg -v
```

- Output

```
Verbose mode On
File Type: sh
Entryfile: samples/sample_params_file.cfg

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
```

- Logfile (etcd_parser.log)

```
2017-07-04 14:59:33,804 root  INFO     Etcd Parsing started...
2017-07-04 14:59:33,804 root  INFO     Reading parameters file <open file u'/home/jparrill/ownCloud/projects/vars2etcd/samples/sample_params_file.cfg', mode 'r' at 0x7fbd023b4c90>
2017-07-04 14:59:33,805 root  INFO     Getting variables from bash file
2017-07-04 14:59:33,805 root  INFO     REPO_SERVER = 10.10.128.72
2017-07-04 14:59:33,805 root  INFO     DOMAIN = example.com
2017-07-04 14:59:33,805 root  INFO     VIP_DB = 10.11.0.43
2017-07-04 14:59:33,805 root  INFO     OS_CTL_NET = 10.11.0
2017-07-04 14:59:33,805 root  INFO     VIP_LDAP = 10.10.128.44
2017-07-04 14:59:33,805 root  INFO     VIP_SDN = 10.10.128.230
2017-07-04 14:59:33,805 root  INFO     VIP_FRONTEND = 10.10.128.101
2017-07-04 14:59:33,805 root  INFO     LDAP_URL = ldap://10.10.128.44
2017-07-04 14:59:33,805 root  INFO     TOP_NS = 'SAMPLE'
2017-07-04 14:59:33,805 root  INFO     PROXY = 22.74.135.87:80
2017-07-04 14:59:33,805 root  INFO     PUBLIC_DOMAIN = public.example.com
2017-07-04 14:59:33,805 root  INFO     INBAND_MGMT_NET = 10.10.128

```

## How to try in local
Use docker to start a ETCD container and publish it there
```
export HostIP=$(ip a | grep -w inet | grep enp0s31f6 | awk '{print $2}' | cut -f1 -d /)
docker run -it --rm -v /usr/share/ca-certificates/:/etc/ssl/certs -p 4001:4001 -p 2380:2380 -p 2379:2379 --name etcd quay.io/coreos/etcd etcd --name etcd0 -advertise-client-urls http://${HostIP}:2379,http://${HostIP}:4001 -listen-client-urls http://0.0.0.0:2379,http://0.0.0.0:4001 -initial-advertise-peer-urls http://${HostIP}:2380 -listen-peer-urls http://0.0.0.0:2380 -initial-cluster-token etcd-cluster-1 -initial-cluster etcd0=http://${HostIP}:2380 -initial-cluster-state new
```

Modify Those env vars to point to another server

- ETCD_HOST: The default value is '127.0.0.1' (Type: str)
- ETCD_PORT: The default value is 4001 (Type: int)
- ETCD_API_VER: The default value is 'v2' (Type: str)

Then execute it:
```
python etcd_var_parser.py -t sh samples/sample_params_file.cfg
```

## References
Credits to [Felipe Martin](https://github.com/fmartingr) for BashDict Class ;)

## Bonus
PEP8 Friendly
