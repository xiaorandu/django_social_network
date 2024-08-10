## **WeConnect: Backend Web Application for a Social Networking Platform**
+ [1. Introduction](#1-introduction)
+ [2. Architecture Overview](#2-Architecture-Overview)
+ [3. Virtual Environment Setup](#3-Virtual-Environment-Setup)
+ [4. Models](#4-Models)
+ [5. APIs](#5-APIs)

### 1. Introduction
+ **Technologies: Python, Django, MySQL, HBase, Redis, Memcached, Docker**
+ Developed the backend for a social networking platform using **Django**, deployed within a **Docker environment**, and implemented **RESTful APIs** for user accounts, posts, comments, friendships, likes, and newsfeeds.
+ Utilized **MySQL** and **HBase** for data storage, and employed **Redis** and **Memcached** for caching various types of data.
+ Implemented a **push model** for newsfeed fanout and leveraged **Redis** and **Celery** for asynchronous task processing.

### 2. Architecture Overview

<img src="diagram.png" alt="Alt text" width="50%"/>

### 3. Virtual Environment Setup
```
***** (1) docker setup *****
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

***** (2) Connect to Virtual Environment *****
docker ps
docker exec -it mineos /bin/bash
su - 'username'
cd /vagrant

***** (3) Initial Django Project *****
#1. project initiate
django-admin startproject social_network

#2. update social_network/setting.py -> DATEBASES
#3. execute migrate
cd social_network
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

#5. define and manage multi-container Docker applications: Memcached and Redis
#docker-compose -f docker-compose-tools.yaml up

#6. run the project
python manage.py runserver 0.0.0.0:8000
```

### 4. Models
+ Defining data models using Django's ORM. The models represent the database schema and are the foundations of the APIs. 
```
mysql> SHOW TABLES;
+----------------------------+
| Tables_in_social_network   |
+----------------------------+
| accounts_userProfile       |
| comments_comment           | 
| friendships_friendship     |
| likes_like                 |
| newsfeeds_newsfeed         |
| tweets_tweet               |  
+----------------------------+
```
**Schema**
| Model       | Fields                             |
|-------------|------------------------------------|
| userProfile | user (PK), created_at, updated_at  |
| Comment     | user (FK), tweet (FK), content, created_at, updated_at |
| Friendship  | from_user (FK), to_user, created_at |
| Like        | user (FK), object_id, content_type, content_object, created_at |
| NewsFeed    | user (FK), tweet (FK), created_at |
| Tweet       | user (FK), content, created_at, like_count, comments_count |

### 5. APIs
+ After creating serializers and defining ViewSets, Django Rest Frameworks' routers automatically map the viewsets to URL patterns, simplifying the process of defining the API endpoints. The URL patterns
can be defined in `urls.py` file.

```
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from accounts.api.views import UserViewSet, AccountViewSet, UserProfileViewSet
from friendships.api.views import FriendshipViewSet
from newsfeeds.api.views import NewsFeedViewSet
from tweets.api.views import TweetViewSet
from comments.api.views import CommentViewSet
from likes.api.views import LikeViewSet

router = routers.DefaultRouter()
router.register(r'api/users', UserViewSet)
router.register(r'api/accounts', AccountViewSet, basename='accounts')
router.register(r'api/tweets', TweetViewSet, basename='tweets')
router.register(r'api/friendships', FriendshipViewSet, basename='friendships')
router.register(r'api/newsfeeds', NewsFeedViewSet, basename='newsfeeds')
router.register(r'api/comments', CommentViewSet, basename='comments')
router.register(r'api/likes', LikeViewSet, basename='likes')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls',  namespace='rest_framework')),
    path('', include(router.urls))
]
```



