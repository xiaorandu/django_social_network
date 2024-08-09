# django_social_network
### 1. Environment Setup

```
#download docker and check docker version
docker --version
docker info

#get ubuntu mirror
docker pull ubuntu:18.04
docker run -v "/django_social_network:/vagrant" -i -t --name mineos ubuntu:18.04 bash

#check system version
root@e928d367d8f1:/# cat /etc/issue
#Ubuntu 18.04.6 LTS \n \l

apt install vim
apt update
apt install python3 python3-pip wget dos2unix sudo lsb-release

#update root pw
root@e928d367d8f1:/# passwd root

#create sudo user
root@e928d367d8f1:/vagrant# adduser 'username'

root@e928d367d8f1:/vagrant# usermod -aG sudo 'username'
su - 'username'
```
