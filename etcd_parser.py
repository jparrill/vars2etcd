#!/usr/bin/python

import sys
import os
from os.path import realpath
from os.path import dirname
from os.path import exists
import logging
import re
import etcd
import requests

class BashDict(dict):
    variable_regex = '(\$\{?([\w\d\-\_\,\.]+)\}?)'
    def _parse_variables(self, value):
        if '$' in value:
            def replace(match):
                return self.get(match.group(2))
            return re.sub(self.variable_regex,
                          replace,
                          value)
        return value

    def __getitem__(self, key):
        value = super(BashDict, self).__getitem__(key)
        return self._parse_variables(value)

    def get(self, key):
        value = super(BashDict, self).get(key)
        return self._parse_variables(value)

class EtcdParser(object):
    '''
    This script will parse all key=value from OSP parameters file from Produban
    and upload it to the correct namespace inside of ETCD
    '''
    def __init__(self):
        ## Modify this couple of vars to point to your server
        self.etcd_host = '127.0.0.1'
        self.etcd_port = 2379
        ##

        self.file_path = dirname(realpath(__file__))
        self.logger()
        self.parse_parameter_file()
        self.upload_parameters_to_etcd()

    def parse_parameter_file(self):
        '''
        This function will load all configuration from main config file
        '''
        self.parameters_file = sys.argv[1]
        self.d = BashDict()

        print 'Reading parameters file...'
        with open(self.file_path + "/" + self.parameters_file, 'r') as f:
            logging.info('Reading parameters file {}'.format(f))
            for line in f.readlines():
                if (not line.startswith('#') and
                not line.startswith(' ') and
                not line.startswith('\n')):
                    key = line.split('=')[0]
                    value = line.split('=', 1)[1]
                    value = value.replace('"','')
                    self.d[key] = value.rstrip('\n')

            logging.info('Getting variables from bash file')

            ## Logging all varaibles into logfile
            print 'Logging parameters'
            for key, value in self.d.items():
                if '$' in value:
                    logging.info('{}={}'.format(key, self.d.get(key)))
                else:
                    logging.info('{}={}'.format(key, value))

    def logger(self):
        '''
        Function to log all actions
        '''
        self.etcd_parser_log = 'etcd_parser.log'
        print 'Start Logging'
        log_file = self.file_path + '/' + self.etcd_parser_log
        logging.getLogger('').handlers = []
        if not os.path.exists(log_file):
            open(log_file, 'a').close()
            logging.basicConfig(
               filename=log_file,
               format='%(asctime)-15s %(name)-5s %(levelname)-8s %(message)s',
               level=logging.INFO
               )
        else:
            logging.basicConfig(
               filename=log_file,
               format='%(asctime)-15s %(name)-5s %(levelname)-8s %(message)s',
               level=logging.INFO
               )
        logging.info('Etcd Parsing started...')


    def upload_parameters_to_etcd(self):
        '''
        Upload all variables stored on the source dict on a
        REGION_NAME/Key=Value
        '''
        print 'Setting Top Namespace'
        try:
            top_ns = self.d.get('TOP_NS')
        except:
            top_ns = ''
            logging.warn('There is not set a TOP_NS variable con parameters file, using /')

        kwargs = {
            'host': self.etcd_host,
            'port': self.etcd_port,
        }

        print 'Uploading parameters to etcd...'
        client = etcd.Client(**kwargs)

        for inner_key, value in self.d.items():
            try:
                ## Getting ETCD top namespace
                get_val = client.get('{}/{}'.format(top_ns, inner_key)).value
                print '\tKey {}/{} already exists as {}'.format(top_ns, inner_key, get_val)
                logging.info('Key {}/{} already exists as {}'.format(top_ns, inner_key, get_val))

            except etcd.EtcdKeyNotFound:
                ## If the key pair do not exists, just post it
                if '$' in value:
                    up_key = '{}/{}'.format(top_ns, inner_key)
                    up_val = self.d.get(inner_key)
                else:
                    up_key = '{}/{}'.format(top_ns, inner_key)
                    up_vale = value

                logging.info('Setting new key {}/{} as {}'.format(top_ns, inner_key, value))
                set_res = client.write(up_key,  up_val)

if __name__ == "__main__":
    EtcdParser()
