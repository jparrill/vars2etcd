# ETCD Parser
This script will take 1 argument, that may contain all variables in bash that one OSP region will need to be deployed (sample):

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

## How it works
The script need to have installed **python-etcd** on your system as requirement.

- Input
```
./etcd_parser.py parameters-boae.cfg
```

- Output
```
Start Logging
Reading parameters file...
Logging parameters
Setting Top Namespace
Uploading parameters to etcd...
	Key 'SAMPLE'/REPO_SERVER already exists as 10.10.128.72
	Key 'SAMPLE'/DOMAIN already exists as 10.10.128.72
	Key 'SAMPLE'/VIP_DB already exists as 10.10.0.43
	Key 'SAMPLE'/OS_CTL_NET already exists as 10.10.0.43
	Key 'SAMPLE'/VIP_LDAP already exists as 10.10.128.44
	Key 'SAMPLE'/VIP_SDN already exists as 10.10.128.230
	Key 'SAMPLE'/VIP_FRONTEND already exists as 10.10.128.101
	Key 'SAMPLE'/LDAP_URL already exists as ldap://10.10.128.44
	Key 'SAMPLE'/TOP_NS already exists as ldap://10.10.128.44
	Key 'SAMPLE'/PROXY already exists as ldap://10.10.128.44
	Key 'SAMPLE'/PUBLIC_DOMAIN already exists as ldap://10.10.128.44
	Key 'SAMPLE'/INBAND_MGMT_NET already exists as ldap://10.10.128.44
```

- Logfile (etcd_parser.log)
```
2017-03-17 13:02:04,202 root  INFO     Etcd Parsing started...
2017-03-17 13:02:04,202 root  INFO     Reading parameters file <open file '/home/jparrill/projects/shellvars2etcd/sample_params_file.cfg', mode 'r' at 0x7fe430f34930>
2017-03-17 13:02:04,202 root  INFO     Getting variables from bash file
2017-03-17 13:02:04,202 root  INFO     REPO_SERVER=10.10.128.72
2017-03-17 13:02:04,202 root  INFO     DOMAIN=example.com
2017-03-17 13:02:04,202 root  INFO     VIP_DB=10.10.0.43
2017-03-17 13:02:04,202 root  INFO     OS_CTL_NET=10.10.0
2017-03-17 13:02:04,203 root  INFO     VIP_LDAP=10.10.128.44
2017-03-17 13:02:04,203 root  INFO     VIP_SDN=10.10.128.230
2017-03-17 13:02:04,203 root  INFO     VIP_FRONTEND=10.10.128.101
2017-03-17 13:02:04,203 root  INFO     LDAP_URL=ldap://10.10.128.44
2017-03-17 13:02:04,203 root  INFO     INBAND_MGMT_NET=10.10.128
2017-03-17 13:02:04,204 root  INFO     PROXY=22.75.135.87:80
2017-03-17 13:02:04,204 root  INFO     PUBLIC_DOMAIN=public.example.com
2017-03-17 13:02:04,205 root  WARNING  There is not set a TOP_NS variable con parameters file, using /
2017-03-17 13:02:04,205 urllib3.connectionpool INFO     Starting new HTTP connection (1): 127.0.0.1
2017-03-17 13:02:04,207 root  INFO     Setting new key /REPO_SERVER as ${INBAND_MGMT_NET}.72
2017-03-17 13:02:04,209 root  INFO     Setting new key /DOMAIN as example.com
2017-03-17 13:02:04,213 root  INFO     Setting new key /VIP_DB as ${OS_CTL_NET}.43
2017-03-17 13:02:04,216 root  INFO     Setting new key /OS_CTL_NET as 10.10.0
2017-03-17 13:02:04,218 root  INFO     Setting new key /VIP_LDAP as ${INBAND_MGMT_NET}.44
2017-03-17 13:02:04,219 root  INFO     Setting new key /VIP_SDN as ${INBAND_MGMT_NET}.230
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
./etcd_parser.py sample_params_file.cfg
```

## References
Thanks to (Felipe Martin)[https://github.com/fmartingr] for helping me :P
