# ETCD Var Parser
This script will parse your variables files to work with ETCD

## How it works

### Requirements
- python-etcd
- python-click

### Execution

- [Upload Content to ETCD](docs/comparing_vars_with_etcd.md)
- [Compare Content with ETCD](docs/uploading_vars_to_etcd.md)
- [Export Content from ETCD](docs/exporting_vars_from_etcd.md)

### Supported Formats

Check the sample folder to view how looks like all of them.

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
python etcd_var_parser.py upload -t sh samples/sample_params_file.cfg
python etcd_var_parser.py upload -t yml samples/example.yml
python etcd_var_parser.py compare -t yml samples/example2.yml
python etcd_var_parser.py export -t yml -o output/test.yml
```

## References
Credits to [Felipe Martin](https://github.com/fmartingr) for BashDict Class ;)

## Bonus
PEP8 Friendly
