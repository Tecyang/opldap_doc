import ldap
from django_auth_ldap.config import LDAPSearch

if __name__ == "__main__":

    #ldap的连接基础配置
    AUTH_LDAP_SERVER_URI = "ldap://39.106.39.88:389"
    AUTH_LDAP_BIND_DN = "cn=admin,dc=66123123,dc=com"
    AUTH_LDAP_BIND_PASSWORD = "leading"

    con = ldap.initialize(AUTH_LDAP_SERVER_URI)
    con.simple_bind_s(AUTH_LDAP_BIND_DN, AUTH_LDAP_BIND_PASSWORD)
    searchScope = ldap.SCOPE_SUBTREE
    # searchFilter = '(objectClass=person)'
    searchFilter = '(uid=leading2018)'
    base_dn = 'ou=people,dc=66123123,dc=com'
    result = con.search_s(base_dn, searchScope, searchFilter, None)
    print(result)

    #修改Django认证先走ldap，再走本地认证
    AUTHENTICATION_BACKENDS = [
        'django_auth_ldap.backend.LDAPBackend',
        'django.contrib.auth.backends.ModelBackend',
    ]

    AUTH_LDAP_USER_DN_TEMPLATE = "uid=%{user}s,ou=archery,ou=group,dc=66123123,dc=com"

    AUTH_LDAP_ALWAYS_UPDATE_USER = True  # 每次登录从ldap同步用户信息
    AUTH_LDAP_USER_ATTR_MAP = {  # key为archery.sql_users字段名，value为ldap中字段名，用户同步信息
        "username": "ssssss",
        "display": "displayname",
        "email": "mail"
    }

# (&(objectClass=person)(uid=leading2018))
#  AUTH_LDAP_USER_SEARCH = LDAPSearch(
#  'ou=archery,ou=group,dc=66123123,dc=com',
#  ldap.SCOPE_SUBTREE,
#  # '(uid=%(user)s)',
#  )

# print(AUTH_LDAP_USER_SEARCH)
