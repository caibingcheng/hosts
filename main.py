# /usr/bin/env python
# _*_coding:utf-8_*_
import os
import json
import dns.resolver


def get(dnsname, hostname):
    hostcontent = []
    for domain in hostname:
        try:
            A = dns.resolver.query(domain, 'A')
            for i in A.response.answer:
                for j in i.items:
                    if isinstance(j, dns.rdtypes.IN.A.A):
                        ip = j.address
                        hostcontent.append([ip, domain])
        except:
            print('query', domain, 'failed')
    return hostcontent


def dump(dnsname, hostcontent):
    curdir = os.getcwd()
    dumpath = os.path.join(curdir, 'dns', dnsname)
    with open(dumpath, 'w') as f:
        f.write('{} HOST {} START {}\n'.format('#'*10, dnsname, '#'*10))
        f.writelines(['{} {}\n'.format(ip, domain)
                      for ip, domain in hostcontent])
        f.write('{} HOST {}   END {}\n'.format('#'*10, dnsname, '#'*10))


def hosts():
    curdir = os.getcwd()
    hostdir = os.path.join(curdir, 'hostname')

    def hostpath(hostfile):
        return os.path.join(hostdir, hostfile)

    def ishostfile(hostfile):
        isfile = os.path.isfile(hostpath(hostfile))
        isjson = hostfile.endswith("hostname.json")
        return isfile and isjson

    candfiles = os.listdir(hostdir)
    hostfiles = [hostfile for hostfile in candfiles if ishostfile(hostfile)]

    for hostfile in hostfiles:
        hostconf = None
        with open(hostpath(hostfile), 'r') as f:
            hostconf = json.load(f)
        yield hostconf['dnsname'], hostconf['hostname']


def main():
    for dnsname, hostname in hosts():
        dns = get(dnsname, hostname)
        dump(dnsname, dns)


if __name__ == '__main__':
    main()
