# /usr/bin/env python
# _*_coding:utf-8_*_
import os


def dnshosts():
    curdir = os.getcwd()
    dnsdir = os.path.join(curdir, 'dns')
    candhosts = os.listdir(dnsdir)

    def dnspath(dnsfile):
        return os.path.join(dnsdir, dnsfile)

    def isdnshost(dnshost):
        isfile = os.path.isfile(dnspath(dnshost))
        iskeep = dnshost == '.keep'
        return isfile and not iskeep
    return [dnshost for dnshost in candhosts if isdnshost(dnshost)]


def template():
    content = ""
    curdir = os.getcwd()
    readme = os.path.join(curdir, '.README.md')
    with open(readme, 'r') as f:
        content = f.read()
    return content


def replace(content, match, string):
    return content.replace(match, string)


def dump(content):
    curdir = os.getcwd()
    readme = os.path.join(curdir, 'README.md')
    with open(readme, 'w') as f:
        f.write(content)


def gen_readme_host_list(hosts):
    content = ""
    for host in hosts:
        content = content + "- `{}`\n".format(host)
    return content


def gen_readme_host_urls(hosts):
    content = \
        '''
|DNS|FROM|URL|
|---|---|---|
'''

    def jsdelivr(host):
        fmt = "https://cdn.jsdelivr.net/gh/caibingcheng/hosts@main/dns/{}"
        return fmt.format(host)

    def gitee(host):
        fmt = "https://gitee.com/caibingcheng/hosts/raw/main/dns/{}"
        return fmt.format(host)

    for host in hosts:
        content = content + \
            "|`{}`|jsdelivr|`{}`|\n".format(host, jsdelivr(host))
        content = content + "|`{}`|gitee|`{}`|\n".format(host, gitee(host))
    return content


def main():
    hosts = dnshosts()
    readme_host_list = gen_readme_host_list(hosts)
    readme_host_urls = gen_readme_host_urls(hosts)

    content = template()
    content = replace(content, '{{ HOSTNAMELIST }}', readme_host_list)
    content = replace(content, '{{ HOSTURL }}', readme_host_urls)
    dump(content)


if __name__ == '__main__':
    main()
