## Project Overview
#### 1. Virtual Environment Setup

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

#copy provision.sh and requirements.txt to the shared folder
cd /vagrant
dos2unix provision.sh
dos2unix requirements.txt

chmod +x provision.sh
./provision.sh

#add environment variable
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

```
#### 2. Connect to Virtual Environment
```
docker ps
docker exec -it mineos /bin/bash
su - 'username'
cd /vagrant
```
#### 3. Initial Django Project
```
#1. project initiate
django-admin startproject social_network

#2. update social_network/setting.py -> DATEBASES
#3. execute migrate
cd social_network
pip install mysqlclient
python manage.py migrate

#4. run mySQL
mysql -u root -p #mySQL login
show tables;
+----------------------------+
| Tables_in_social_network   |
+----------------------------+
| auth_group                 |
| auth_group_permissions     |
| auth_permission            |
| auth_user                  |
| auth_user_groups           |
| auth_user_user_permissions |
| django_admin_log           |
| django_content_type        |
| django_migrations          |
| django_session             |
+----------------------------+

#5.install django rest framework
pip install djangorestframework

#6. run the project
python manage.py runserver 0.0.0.0:8000
```
#### 4. Apps
  + **Account**
    ```
    python manage.py startapp accounts
    cd accounts/
    mkdir api
    #create views and serializers
    touch views.py
    touch serializers.py
    
    ```
