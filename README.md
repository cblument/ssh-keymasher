# ssh-keymasher
Test ssh keys in a directory against a host


## Installation

TODO

## Usage

```
derecho:ssh-keymasher$ python ssh-keymasher.py --help
usage: ssh-keymasher.py [-h] [--directory DIRECTORY] [--user USER] ssh_hosts

Tool to test keys in the user's home directory

positional arguments:
  ssh_hosts             Host or hosts you want to test keys on. Multiple hosts
                        seperated by comma

optional arguments:
  -h, --help            show this help message and exit
  --directory DIRECTORY, -d DIRECTORY
                        directory containing keys to be tested (default:
                        $HOME/.ssh)
  --user USER, -u USER  User to ssh as
  ```

```
derecho:ssh-keymasher$ python ssh-keymasher.py --user jdoe --directory ~/ssh_keys/ 10.0.1.8
{
  "10.0.1.8": {
    "invalid": [
      "/Users/cblument/git/piconf/ssh_keys//id_rsa_key3",
      "/Users/cblument/git/piconf/ssh_keys//id_rsa_key4"
    ],
    "valid": [
      "/Users/cblument/git/piconf/ssh_keys//id_rsa_key1",
      "/Users/cblument/git/piconf/ssh_keys//id_rsa_key2"
    ]
  }
}
```

## License

[Apache 2.0](http://www.apache.org/licenses/LICENSE-2.0)
