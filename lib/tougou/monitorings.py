from urlparse import urljoin
from HTMLParser import HTMLParser
import requests
from BeautifulSoup import BeautifulSoup
import inspect

class MonitoringPlugin(object):
    def __init__(self, user='', pwd='', url_plugin=''):
        self.user = user
        self.pwd = pwd
        self.url_plugin = url_plugin

    def available_commands(self):
        get_services = filter(lambda f: f[0].startswith('get_'), inspect.getmembers(self))
        return [service[0] for service in get_services]

    def cli_parser(self, parser):
        parser.add_argument('method_name')
        args = parser.parse_args()
        if args.method_name:
            if args.method_name in self.available_commands():
                f = getattr(self, args.method_name)
                print f()
            else:
                for cmd in self.available_commands():
                    print "%s %s" % (self.__class__.__name__.lower(), cmd)

class Nagios(MonitoringPlugin):
    def __init__(self, user, pwd, url_nagios):
        self.s = requests.Session()
        self.url_nagios = url_nagios
        self.s.auth = (user, pwd)

    def get_hosts(self):
        hostdetail_url =  urljoin(self.url_nagios, '/cgi-bin/nagios3/status.cgi?hostgroup=all&amp;style=hostdetail')
        res = self.s.get(hostdetail_url)
        return self._parse_hosts(res.text)

    def _parse_hosts(self, html):
        soup = BeautifulSoup(html)
        status = soup.find('table', {'class': 'status'})
        trs = status.findAll('tr', recursive=False)
        hosts = []
        for tr in trs[1:]:
            host = {}
            td = tr.findAll('td', recursive=False)
            host['status'] = td[1].string
            a = tr.findAll('a')
            host['ip'] = a[0]['title']
            host['hostname'] = a[0].string
            hosts.append(host)
        return hosts

    def get_services(self):
        url_services =  urljoin(self.url_nagios, '/cgi-bin/nagios3/status.cgi?host=all')
        res = self.s.get(url_services)
        return self._parse_services(res.text)

    def _parse_services(self, html):
        soup = BeautifulSoup(html)
        status = soup.find('table', {'class': 'status'})
        trs = status.findAll('tr', recursive=False)
        services_by_host = []
        FIRST = True
        for tr in trs[1:]:
            td = tr.findAll('td', recursive=False)
            if td[0].find('a') and td[0].a['title']:
                if not FIRST:
                    services_by_host.append({'host': host,'services': services})
                host = {}
                services = []
                host  = {'hostname': td[0].a.string,
                         'ip': td[0].a['title']}
            if len(td) > 3:
                service = {}
                service['name'] = td[1].a.string
                service['status'] = td[2].string
                service['time'] = td[3].string
                service['uptime'] = td[4].string
                h = HTMLParser()
                service['desc'] = h.unescape(td[6].string)
                services.append(service)
            FIRST = False
        return services_by_host


class Munin(MonitoringPlugin):
    def __init__(self, user, pwd, url_munin):
        self.s = requests.Session()
        self.user = user
        self.pwd = pwd
        self.url_munin = url_munin
        if self.user and self.pwd:
            self.s.auth = (self.user, self.pwd)

    def get_hosts(self, hosts=None):
        r = self.s.get(self.url_munin)
        return self._parse_hosts(r.text)

    def _parse_hosts(self, response):
        s = BeautifulSoup(response)
        domain = s.find('span', {'class': 'domain'}).parent
        hosts_raw = domain.findAll('span', {'class': 'host'})
        hosts = []
        for host_raw in hosts_raw:
            host_dict = {}
            host = host_raw.parent
            hostname = host.find('span', {'class': 'host'}).a.string
            host_dict = {'hostname': hostname}
            hosts.append(host_dict)
        return hosts


if __name__ == '__main__':
    pass
