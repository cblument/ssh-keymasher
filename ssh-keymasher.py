import argparse
import json
import os
import paramiko
from getpass import getpass

class IgnorePolicy(paramiko.MissingHostKeyPolicy):
    def missing_host_key(self, client, hostname, key):
        return True

def get_files(ssh_dir):
    files = []
    for filename in os.listdir(ssh_dir):
        full_ssh_path = "/".join([ssh_dir, filename])
        if os.path.isdir(full_ssh_path):
            # Skip iteration if directory
            continue
        files.append(full_ssh_path)
    return files

def test_hosts(hosts=None, port=22, ssh_dir=None,
               username=os.getenv('USER')):
    ssh_keys = []
    for filename in get_files(ssh_dir):
        valid_key = False
        if not valid_key:
            try:
                keyobj = paramiko.rsakey.RSAKey(filename=filename)
                ssh_keys.append({'key_file': filename,
                                 'key_object': keyobj})
                valid_key = True
            except paramiko.ssh_exception.PasswordRequiredException:
                try:
                    pw = getpass("%s passphrase: " % filename)
                    keyobj = paramiko.rsakey.RSAKey(filename=filename,
                                                    password=pw)
                    ssh_keys.append({'key_file': filename,
                                     'key_object': keyobj})
                    valid_key = True
                except paramiko.ssh_exception.SSHException:
                    pass
            except paramiko.ssh_exception.SSHException:
                pass
        if not valid_key:
            try:
                keyobj = paramiko.dsskey.DSSKey(filename=filename)
                ssh_keys.append({'key_file': filename,
                                 'key_object': keyobj})
                valid_key = True
            except paramiko.ssh_exception.SSHException:
                pass
    data = {}
    for host in hosts.split(','):
        working_keys = []
        nonworking_keys = []
        for item in ssh_keys:
            client = paramiko.client.SSHClient()
            client.set_missing_host_key_policy(IgnorePolicy())
            try:
                client.connect(hostname=host,
                            username=username,
                            port=port,
                            pkey=item['key_object'],
                            allow_agent=False,
                            look_for_keys=False)
                stdin, stdout, stderr = client.exec_command('uptime')
                working_keys.append(item['key_file'])
            except paramiko.ssh_exception.AuthenticationException:
                nonworking_keys.append(item['key_file'])
            finally:
                client.close()
                data[host] = { 'valid': working_keys,
                               'invalid': nonworking_keys }
    return data

if __name__ == '__main__':
    description = "Tool to test keys in the user's home directory"
    dir_help = "directory containing keys to be tested (default: $HOME/.ssh)"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('ssh_hosts',
                        help='Host or hosts you want to test keys on. Multiple hosts seperated by comma')
    parser.add_argument('--directory', '-d',
                        help=dir_help,
                        default=os.path.expanduser("~/.ssh"))
    parser.add_argument('--user', '-u', help='User to ssh as')
    args = parser.parse_args()
    key_data = test_hosts(hosts=args.ssh_hosts,
                          username=args.user,
                          ssh_dir=args.directory)

    print json.dumps(key_data, sort_keys=True,indent=2)

