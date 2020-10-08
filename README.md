# CDPnetworkMAP :
CDP network Discover and output Information Parser


## Requirment :

- Python3
- install requirements.txt
- Linux (ubuntu / Arch / manjaro ...)

## Instalation :

```bash
$ git clone https://github.com/HamzaOPLEX/CDPnetworkMAP
$ cd CDPnetworkMAP
$ sudo pip3 install -r requirements.txt
```

## How it work :

let say we have 3 cisco routers , you need to configure ssh connection information for each cisco router then he retrieved the CDP information from those CDP informations .

## configuration :

all device configuration will add to Hosts.yaml

####    1-Hosts.yaml options :
  - host = ip address of the device (require)
  - username = ssh username (require)
  - password = ssh password (not require if you use ssh key based authentication)
  - use_key  = True/False (not require if you use ssh password authentication )
  - device_type = cisco_ios for cisco (require)
  - port = default is 22 (not require)
  - key_file = default is "~/.ssh/id_rsa.pub" (require if you have the ssh pub key in diffrent location)

####    2-Hosts.yaml SSH Password Based Authentication :

![alt text](https://github.com/HamzaOPLEX/CDPnetworkMAP/blob/main/img/PasswordBasedAuthentication.png)

####    3-Hosts.yaml key Based Authentication :

![alt text](https://github.com/HamzaOPLEX/CDPnetworkMAP/blob/main/img/KeyBasedAuthentication.png)

####    4-Hosts.yaml Enable Mode:
![alt text](https://github.com/HamzaOPLEX/CDPnetworkMAP/blob/main/img/enablemode.png)

## running the script :

- Show Help : ```$python3 CDPnetworkMAP.py -h```
- run Basic CDP Discovery : ```$python3 CDPnetworkMAP.py -B```
- run Detailed CDP Discovery : ```$python3 CDPnetworkMAP.py -D```
- Generat a Grafical Network Topology : ```$python3 CDPnetworkMAP.py -T```

Enjoy :)
