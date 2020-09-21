## ldap 实现linux统一账号管理

### 参考  
[nsswitch.conf文件详解](https://blog.csdn.net/lcr_happy/article/details/59109163)

### 环境配置
```shell
sudo bash -c "echo '192.168.157.173   ldap.66123123.com' >> /etc/hosts"
```
### 软件安装
```shell
sudo yum install -y nss-pam-ldapd openldap-clients
```

#### 配置openLDAP-client
```shell
#配置ldapclient 配置文件
sudo cp /etc/openldap/ldap.conf /etc/openldap/ldap.conf.old
sudo bash -c "cat >> /etc/openldap/ldap.conf <<EOF
host ldap.66123123.com
BASE dc=66123123,dc=com
URI ldap://ldap.66123123.com ldap://ldap.66123123.com:389
ssl off
EOF"
```
通过如下命令测试客户端配置是否正确:
```shell
ldapsearch -x -W -D "cn=admin,dc=66123123,dc=com" -b "ou=people,dc=66123123,dc=com"
```
#### 配置 NSS 服务

> 如果想使 nss 可以查询ldap，那么首先就需要启用一个叫 nslcd 的服务， 以下是该服务的配置文件。

```shell
#备份 nslcd 配置
sudo cp /etc/nslcd.conf /etc/nslcd.conf.old
sudo vim /etc/nslcd.conf
#修改为如下配置:
uid nslcd
gid ldap

uri     ldap://ldap.66123123.com:389
base    dc=66123123,dc=com
binddn  cn=admin,dc=66123123,dc=com
bindpw  ******
ssl     off

#重启服务
sudo systemctl restart nslcd
```

> 文件/etc/nsswitch.conf (name service switch configuration，名字服务切换配置)规定通过哪些途径以及按照什么顺序通过这些途径来查找特定类型的信息。还可以指定某个方法奏效或失效时系统将采取什么动作。详情参考
[nsswitch.conf文件详解](https://blog.csdn.net/lcr_happy/article/details/59109163)
```shell
#备份默认配置
sudo cp /etc/nsswitch.conf /etc/nsswitch.conf.old

#让 NSS 服务使用 OpenLDAP 服务器
sudo bash -c "sed -i '/^passwd:.*$/s//&  ldap/g' /etc/nsswitch.conf
sed -i '/^shadow:.*$/s//&  ldap/g' /etc/nsswitch.conf
sed -i '/^group:.*$/s//&  ldap/g' /etc/nsswitch.conf"

#验证配置
getent passwd|grep leading

```

#### 配置pam配置 
```shell
#备份配置
sudo cp /etc/pam.d/password-auth /etc/pam.d/password-auth.old

#增加如下配置
auth        sufficient    pam_ldap.so use_first_pass
account     sufficient    pam_ldap.so
password    sufficient    pam_ldap.so use_authtok
session     optional      pam_ldap.so
```

#### 配置sshd配置
```shell
#备份配置
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.old

#修改如下配置
UsePAM yes
PasswordAuthentication yes

#重启服务
sudo systemctl restart sshd
```



#### 配置sftp分组权限
``` shell
#配置文件备份
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.old.2

#根目录创建sftp目录 
sudo mkdir /sftp
sudo chown root:root /sftp
sudo chmod 755 /sftp

#创建用户可操作目录
sudo mkdir /sftp/uploads
sudo chown sftp:sftp /sftp/uploads

#修改配置文件
sed -i '/^Subsystem.*sftp.*$/s/^/#/g' /etc/ssh/sshd_config

sed -i '$a\Subsystem       sftp    internal-sftp\
Match Group sftp\
PasswordAuthentication yes\
ChrootDirectory /sftp\
ForceCommand internal-sftp\
PermitTunnel no\
AllowAgentForwarding no\
AllowTcpForwarding no\
X11Forwarding no\
' /etc/ssh/sshd_config

#重启服务
sudo systemctl restart sshd

#设置同步目录绑定

mount --bind /home/produce/nas/leading_erp_file/guangfa guangfa

```
