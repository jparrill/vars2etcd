# ETCD Parser
This script will take 1 argument, that may contain all variables in bash that one OSP region will need to be deployed (sample):

```
REGION_NAME="BOAE"
DEFAULT_AZ="${REGION_NAME}-1"
AZ2="${REGION_NAME}-2"
AZ3="${REGION_NAME}-3"
OS_SERVICE_TOKEN="23ccdecfd7cbcfbbf36f"
CONFIG_FILE="/home/osp-test/boae.json
LDAP_URL="ldap://$VIP_LDAP"
```

## How it works
The script need to have installed **python-etcd** on your system and also the parameters files from **global-cloud-bash** repository.

- Input
```
./etcd_parser.py parameters-boae.cfg
```

- Output
```
Start Logging
Reading parameters file...
Logging parameters
Uploading parameters to etcd...
  Key BOAE/NUAGE_VSD_2 already exists as vmboae00vsdp02-oscp
  Key BOAE/NUAGE_VSD_3 already exists as vmboae00vsdp03-oscp
  Key BOAE/STF_NET_VIRTUAL already exists as 10.24.0
  Key BOAE/BE_CLUSTER_NAME already exists as backend
```

- Logfile (etcd_parser.log)
```
2017-03-16 16:10:12,027 root  INFO     Reading parameters file <open file '/home/jparrill/ownCloud/RedHat/RedHat_Consulting/Produban/repos/global-cloud-ansible/utils/osp/etcd_parser/parameters-boae.cfg', mode 'r' at 0x7f5a0dad4ae0>
2017-03-16 16:10:12,036 urllib3.connectionpool INFO     Starting new HTTP connection (1): 127.0.0.1
2017-03-16 16:10:12,037 root  INFO     Setting new key BOAE/CON_NODE_3_HOSTNAME_AZ2 as vmboae00osconp06
2017-03-16 16:10:12,048 root  INFO     Setting new key BOAE/CON_NODE_3_HOSTNAME_AZ3 as vmboae00osconp09
2017-03-16 16:10:12,052 root  INFO     Setting new key BOAE/KEYSTONE_CN as keystone.boae.gsnetcloud.corp
2017-03-16 16:10:12,054 root  INFO     Setting new key BOAE/CONFIG_FILE as /home/osp-test/boae.json
2017-03-16 16:10:12,058 root  INFO     Setting new key BOAE/BE_NODE_2_HOSTNAME as vmboae00osdbp02
2017-03-16 16:10:12,060 root  INFO     Setting new key BOAE/HA_CLUSTER_NAME as haproxy
...
...
```

That means that we have new keys installed on ETCD, if the parser tries to upload a key-value that already exists, will not be overrided, just will warn you trough log file and stdout that already exists

_Note: The parameter files are a sample from the real **global-cloud-bash** repository, use the original repository to work on a real environment_

## How to try in local
Use docker to start a ETCD container and publish it there
```
export HostIP=$(ip a | grep -w inet | grep enp0s31f6 | awk '{print $2}' | cut -f1 -d /)
docker run -it --rm -v /usr/share/ca-certificates/:/etc/ssl/certs -p 4001:4001 -p 2380:2380 -p 2379:2379 --name etcd quay.io/coreos/etcd etcd --name etcd0 -advertise-client-urls http://${HostIP}:2379,http://${HostIP}:4001 -listen-client-urls http://0.0.0.0:2379,http://0.0.0.0:4001 -initial-advertise-peer-urls http://${HostIP}:2380 -listen-peer-urls http://0.0.0.0:2380 -initial-cluster-token etcd-cluster-1 -initial-cluster etcd0=http://${HostIP}:2380 -initial-cluster-state new
```

Now modify the script to point to your etcd server:
```
def __init__(self):
    ## Modify this couple of vars to point to your server
    self.etcd_host = '127.0.0.1'
    self.etcd_port = 2379
    ##
```

Then execute it:
```
./etcd_parser.py parameters-boae.cfg
```

## References
Thanks to (Felipe Martin)[https://github.com/fmartingr] for helping me :P
