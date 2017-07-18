#!/usr/bddin/python

import yaml
import json
import pprint 
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

    def __init__(self, verbose=False, force=False):
        self.verbose = verbose
        self.force = force
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

            if not conflict or self.force:
                self.eload.etcd_uploader(self.etcd_handler, concat, value)


class YamlVars(object):
    """
    Class to load and format yaml variables
    """

    def __init__(self, verbose=False, force=False):
        self.verbose = verbose
        self.force = force
        self.eload = EtcdParser(self.verbose)
        self.etcd_handler = self.eload.etcd_conn()

    def yaml_loader(self, yaml_file):
        '''
        This function will receive a yaml file path and will return a dict
        '''
        content = {}
        if self.verbose:
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
                    concat = parent + k + '/' + str(v.index(key))
                    # if There is an Array at the last tree hierarchi
                    # I create an empty folder to emulate an array
                    logging.info('Folder: {}'.format(concat))
                    conflict = self.eload.etcd_check_conflict(self.etcd_handler, concat, key, True)
                    if not conflict or self.force:
                        self.eload.etcd_uploader(self.etcd_handler, concat, key)

            else:
                concat = parent + str(k)
                logging.info('{} = {}'.format(concat, v))
                conflict = self.eload.etcd_check_conflict(self.etcd_handler, concat, v)

                if not conflict or self.force:
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
        if self.verbose:
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

    def etcd_delete(self, etcd_handler, key, folder=False):
        '''
        Function to delete a key or folder on ETCD
        '''
        etcd_handler.delete(key, folder, folder)

    def _parse_node(self, node):
        path = {}
        if node.get('dir', False):
            for n in node.get('nodes', []):
                path[n['key'].split('/')[-1]] = self._parse_node(n)

        else:
            path = node['value']

        return path

    def etcd_get_tree(self, etcd_handler, key):
        '''
        This function will return a dict coming from ETCD path
        '''
        final_tree = {}
        value = {}

        try:
            data = etcd_handler.read(key, recursive=True, sorted=True)

        except etcd.EtcdKeyNotFound:
            return response

        try:
            for element in data._children:
                value[element['key'].replace(key, '')] = self._parse_node(element)
            
            if 'errorCode' in data._children:
                # Here return an error when an unknown entry responds
                value = "ENOENT"

        except:
            raise
            pass

        return value
        

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


@click.group()
@click.option('-v', '--verbose', is_flag=True, default=False, help='Debug mode')
@click.pass_context
def cli(ctx, verbose):
    ctx.obj['verbose'] = ctx.params['verbose']  

@click.command()
@click.option('-t', '--file-type', type=click.Choice(['yml', 'sh']), nargs=1, help='File type to load')
@click.option('-p', '--prefix', default='/data/', help='Top Namespace to upload yaml tree')
@click.option('-f', '--force', is_flag=True, default=False, help='Override the ETCD parameters')
@click.argument('entryfile')
@click.pass_context
def upload(ctx, file_type, entryfile, prefix, force):
    if ctx.obj['verbose']:
        click.echo('Verbose mode is %s' % (ctx.obj['verbose'] and 'on' or 'off'))
        click.echo("File Type: {}".format(file_type))
        click.echo("Entryfile: {}".format(entryfile))
        click.echo()
    
    if force:
        click.echo('WARNING: Override mode on')

    if file_type == 'sh':
        # Shell
        click.echo('Uploading parameters from Bash file...')
        ShlVar = ShellVars(ctx.obj['verbose'], force)
        ShlVar.shell_loader(entryfile)
        ShlVar.shell_formatter()
        click.echo('Done!')

    elif file_type == 'yml':
        # Yaml
        click.echo('Uploading parameters from YML file...')
        YmlVar = YamlVars(ctx.obj['verbose'], force)
        MAP = YmlVar.yaml_loader(entryfile)
        if ctx.obj['verbose']:
            print 'Logging parameters'
            print
        YmlVar.yaml_formatter(MAP, prefix)
        click.echo('Done!')

    else:
        raise ValueError('File type {} not supported'.format(file_type))


@click.command()
@click.option('-t', '--file-type', type=click.Choice(['yml', 'sh']), nargs=1, help='File type to load')
@click.argument('entryfile')
@click.pass_context
def compare(ctx, file_type, entryfile):
    if ctx.obj['verbose']:
        click.echo('Verbose mode is %s' % (ctx.obj['verbose'] and 'on' or 'off'))
        click.echo("File Type: {}".format(file_type))
        click.echo("Entryfile: {}".format(entryfile))
        click.echo()

    if file_type == 'yml':
        # Yaml
        compare_basepath = '/_compare/'
        data_basepath = '/data/'
        YmlVar = YamlVars(ctx.obj['verbose'])
        etcd_map = YmlVar.eload.etcd_get_tree(YmlVar.etcd_handler, data_basepath)
        
        # Create structure bellow compare_basepath to copmare in the same conditions
        # I have no time to modify in the right way the lists coming from etcd, that
        # the representation is a 0: 'value'. 
        yaml_raw_map = YmlVar.yaml_loader(entryfile)
        YmlVar.yaml_formatter(yaml_raw_map, compare_basepath)
        yaml_map = YmlVar.eload.etcd_get_tree(YmlVar.etcd_handler, compare_basepath)
        
        # Clean /_compare folder
        YmlVar.eload.etcd_delete(YmlVar.etcd_handler, compare_basepath, True)

        if ctx.obj['verbose']:
            print 'YAML:'
            pprint.pprint(yaml_map)

            print 'ETCD:'
            pprint.pprint(etcd_map)

        if yaml_map != etcd_map:
            raise ValueError('Yaml and ETCD not contain the same data')

        else:
            print 'ETCD and YAML file are equal'


    else:
        raise ValueError('File type {} not supported'.format(file_type))

@click.command()
@click.option('-t', '--file-type', type=click.Choice(['yml', 'sh']), nargs=1, help='File type to load')
@click.option('-o', '--output-file', nargs=1, help='Output File')
@click.pass_context
def export(ctx, output_file, file_type):
    if ctx.obj['verbose']:
        click.echo('Verbose mode is %s' % (ctx.obj['verbose'] and 'on' or 'off'))
        click.echo("File Type: {}".format(file_type))
        click.echo("Ouput File: {}".format(output_file))
        click.echo()

    if file_type == 'yml':
        # Yaml
        data_basepath = '/data/'
        YmlVar = YamlVars(ctx.obj['verbose'])
        etcd_map = YmlVar.eload.etcd_get_tree(YmlVar.etcd_handler, data_basepath)

        if ctx.obj['verbose']:
            print 'ETCD:'
            pprint.pprint(etcd_map)

        with open(output_file, 'w') as yaml_file:
            yaml.safe_dump(etcd_map, yaml_file, default_flow_style=False)

    else:
        raise ValueError('File type {} not supported'.format(file_type))

if __name__ == '__main__':
    cli.add_command(upload)
    cli.add_command(compare)
    cli.add_command(export)
    cli(obj={})
