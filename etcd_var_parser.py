#!/usr/bin/python

import yaml
import logging
import etcd
import os
import re
import click
from os.path import dirname
from os.path import realpath


class ShellVars(object):
    """
    Class to load and format shell variables
    """

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.eload = EtcdParser(self.verbose)
        self.etcd_handler = self.eload.etcd_conn()
        self.file_path = self.eload.file_path

    def shell_loader(self, params_file):
        '''
        This function will load all configuration from main config file
        '''
        self.d = BashDict()
        self.parameters_file = params_file

        print 'Reading parameters file...'
        with open(self.file_path + "/" + self.parameters_file, 'r') as f:
            logging.info('Reading parameters file {}'.format(f))
            for line in f.readlines():
                if (not line.startswith('#')
                        and not line.startswith(' ')
                        and not line.startswith('\n')):
                    key = line.split('=')[0]
                    value = line.split('=', 1)[1]
                    value = value.replace('"', '')
                    self.d[key] = value.rstrip('\n')

            logging.info('Getting variables from bash file')

            # Logging all varaibles into logfile
            print 'Logging parameters'
            for key, value in self.d.items():
                if '$' in value:
                    logging.info('{} = {}'.format(key, self.d.get(key)))
                else:
                    logging.info('{} = {}'.format(key, value))

    def shell_formatter(self):
        try:
            top_ns = self.d.get('TOP_NS').strip("'")

        except KeyError:
            top_ns = ''
            logging.warn('There is not set a TOP_NS variable con parameters file, using /')

        for inner_key, value in self.d.items():
            concat = '{}/{}'.format(top_ns, inner_key)
            conflict = self.eload.etcd_check_conflict(self.etcd_handler, concat, value)

            if not conflict:
                self.eload.etcd_uploader(self.etcd_handler, concat, value)


class YamlVars(object):
    """
    Class to load and format yaml variables
    """

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.eload = EtcdParser(self.verbose)
        self.etcd_handler = self.eload.etcd_conn()

    def yaml_loader(self, yaml_file):
        '''
        This function will receive a yaml file path and will return a dict
        '''
        content = {}
        print 'Reading parameters file...'
        logging.info('Reading parameters file {}'.format(yaml_file))

        with open(yaml_file, 'r') as stream:
            try:
                content = yaml.load(stream)
            except Exception as exc:
                logging.error("Error opening {} file".format(yaml_file))
                raise yaml.YAMLError(str(exc))

        return content

    def yaml_formatter(self, entry, parent):
        for k, v in entry.iteritems():
            if isinstance(v, dict):
                concat = parent + k + '/'
                self.yaml_formatter(v, concat)
            elif isinstance(v, list):
                for key in v:
                    concat = parent + k + '/' + key
                    # if There is an Array at the last tree hierarchi
                    # I create an empty folder to emulate an array
                    logging.info('Folder: {}'.format(concat))
                    conflict = self.eload.etcd_check_conflict(self.etcd_handler, concat, None, True)
                    if not conflict:
                        self.eload.etcd_uploader(self.etcd_handler, concat, None, True)

            else:
                concat = parent + k
                logging.info('{} = {}'.format(concat, v))
                conflict = self.eload.etcd_check_conflict(self.etcd_handler, concat, v)

                if not conflict:
                    self.eload.etcd_uploader(self.etcd_handler, concat, v)


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
    """
    Class to load variables into ETCD
    """

    def __init__(self, verbose=False):
        # Get Env Variables
        self.verbose = verbose
        self.etcd_host = os.getenv('ETCD_HOST', '127.0.0.1')
        self.etcd_port = os.getenv('ETCD_PORT', 4001)
        self.etcd_ver = os.getenv('ETCD_API_VER', 'v2')
        self.file_path = dirname(realpath(__file__))
        self.logger()

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

    def etcd_conn(self):
        '''
        Function to connect with ETCD
        '''
        kwargs = {
            'host': self.etcd_host,
            'port': self.etcd_port,
        }

        return etcd.Client(**kwargs)

    def etcd_uploader(self, etcd_handler, key, value, _dir=None):
        '''
        Function to upload variables to ETCD
        '''
        if _dir is not None:
            if self.verbose:
                print "Creating folder {}".format(key)
            etcd_handler.write(key, None, None, True)
        else:
            if self.verbose:
                print "Adding - Key: {} Value: {}".format(key, value)
            etcd_handler.write(key, value)

    def etcd_check_conflict(self, etcd_handler, key, value, _dir=False):
        '''
        This function will check if your key exists already on ETCD DB
        '''
        response = False

        old_val = {}
        try:
            old_fold = etcd_handler.get(key).key
            old_val = etcd_handler.get(key).value

        except etcd.EtcdKeyNotFound:
            return response

        if not _dir:
            if old_val == '':
                old_val = None

            new_val = value

            if str(old_val):
                logging.warn('Warning: This Key already exists')
                logging.warn('\tParameter: {}'.format(key))
                logging.warn('\tFile: {}'.format(new_val))
                logging.warn('\tEtcd: {}'.format(old_val))
                if self.verbose:
                    print 'Warning: This Key already exists'
                    print '\tParameter: {}'.format(key)
                    print '\tFile: {}'.format(new_val)
                    print '\tEtcd: {}'.format(old_val)

                response = True

        else:
            if old_fold:
                logging.warn('Warning: The folder already exists')
                logging.warn('\tFolder: {}'.format(old_fold))
                if self.verbose:
                    print 'Warning: The folder already exists'
                    print '\tFolder: {}'.format(old_fold)

                response = True

        return response


@click.command()
@click.option('-v', '--verbose', is_flag=True, default=False, help='Debug mode')
@click.option('-t', '--file-type', type=click.Choice(['yml', 'sh']), help='File type to load')
@click.argument('entryfile')
def cli(verbose, file_type, entryfile):
    if verbose:
        click.echo("Verbose mode On")
        click.echo("File Type: {}".format(file_type))
        click.echo("Entryfile: {}".format(entryfile))
        click.echo()

    if file_type == 'sh':
        # Shell
        ShlVar = ShellVars(verbose)
        ShlVar.shell_loader(entryfile)
        ShlVar.shell_formatter()

    elif file_type == 'yml':
        # Yaml
        YmlVar = YamlVars(verbose)
        MAP = YmlVar.yaml_loader(entryfile)
        print 'Logging parameters'
        YmlVar.yaml_formatter(MAP, "/")

    else:
        raise ValueError('File type {} not supported'.format(file_type))


if __name__ == '__main__':
    cli()
