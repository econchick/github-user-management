import ldap

LDAP_BASE = 'cn=users,dc=carmen,dc=int,dc=sto,dc=spotify,dc=net'


class LdapClient(object):
    def __init__(self, ldap_url):
        self.ldap_url = ldap_url

    def __enter__(self):
        self.conn = ldap.initialize(self.ldap_url)
        return self

    def __exit__(self, *ignored):
        self.conn.unbind_s()

    def user_from_github_login(self, github_login):
        result = self.conn.search_s(
            LDAP_BASE, ldap.SCOPE_ONELEVEL,
            '(githubcomAccount=%s)' % github_login, ('uid',))
        if not result:
            return None
        return result[0][1]['uid'][0]

    def get_github_users(self):
        result = self.conn.search_s(
            LDAP_BASE, ldap.SCOPE_ONELEVEL,
            '(githubcomAccount=*)', ('uid', 'loginShell', 'githubcomAccount')
        )
        for dn, e in result:
            yield e['uid'][0], e['loginShell'][0], e['githubcomAccount'][0]
