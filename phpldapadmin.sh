   
   docker run -p 6443:443 \
        --env PHPLDAPADMIN_LDAP_HOSTS=jump.xxxx.com \
        --detach osixia/phpldapadmin:latest

