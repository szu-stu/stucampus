**安装virtualenv**
```
pip install virtualenv
```

**新建virtualenv**

```
virtualenv stucampus_env
```
**启动虚拟环境**
```
cd stucampus_env
source bin/activate 
```

**下载源码**

```
 git clone https://github.com/jimczj/Stucampus.git
```

**安装依赖模块** 

```
sudo apt-get install libxml2-dev libxslt1-dev
sudo apt-get install PIL --allow-external PIL --allow-unverified PIL
pip install -r requirements.txt#如果有报错，自行谷歌，然后补充一下本文件
```
**更改配置**
copy一份stucampus/config/production.py.sample, 重命名为
production.py, 记得把DEBUG改成True

```
cp Stucampus/stucampus/config/production.py.sample Stucampus/stucampus/config/production.py
sudo vim Stucampus/stucampus/config/production.py
```
**在production.py添加数据库的配置**，可以参考下图

![这里写图片描述](http://img.blog.csdn.net/20160501014257812)

如果本地没有安装postgresql_psycopg2，就用sqlite3（python自带数据库），为了和主站保持一致，防止未知错误的出现，还是建议安装postgresql_psycopg

如果用**非sqlite3数据库**（Mysql，postgresql_psycopg2），数据库和用户，密码，需要自行登录数据库去添加，然后再配置上去，可以参考http://blog.csdn.net/qq_32445689/article/details/50988273

**用sqlite3的时候**，数据库会按配置文件自动生成在本地，直接填写好配置文件就执行数据库建表和同步操作

**数据库建表并同步**

```
python manage.py makemigrations
python manage.py migrate
```
**运行**

```
python manage.py runserver
```

**注意：**开发新项目的时候，建议自己开一个分支，然后将分支push上github，将github上的分支pull下来的时候，也建议新开分支再pull
比如pull newBrand这个分支

```
git checkout -b newBrand#新建分支并切换到该分支
git pull origin newBrand#将newBrand的代码pull下来
```


