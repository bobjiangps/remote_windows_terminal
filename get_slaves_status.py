from urllib import request
import re


def get_html_source(url):
    response = request.urlopen(url, data=None, timeout=10)
    if response.code == 200:
        source_data = response.read().decode("utf-8")
        response.close()
        return source_data
    else:
        print("http code is not 200")
        return None


def categorize_slave_status(slave_dict, prefix):
    free_slaves = []
    busy_slaves = []
    offline_slaves = []
    other_status = []
    for s in slave_dict.items():
        if s[1] == "free":
            free_slaves.append(s[0])
        elif s[1] == "busy":
            busy_slaves.append(s[0])
        elif s[1] == "offline":
            offline_slaves.append(s[0])
        else:
            other_status.append(s[0])
    print("%d %s slaves status:\nfree: %d, busy: %d, offline: %d, other: %d" % (len(slave_dict), prefix, len(free_slaves), len(busy_slaves), len(offline_slaves), len(other_status)))
    if offline_slaves:
        print("offline slaves are: %s" % str(offline_slaves)[1:-1])
    if other_status:
        print("other status slaves are: %s" % str(other_status)[1:-1])


if __name__ == "__main__":
    win10_slaves = {}
    linux_slaves = {}
    page_num = 1
    while True:
        win10_url = "http://slave_url?keyword=win10" % page_num
        page_source = get_html_source(win10_url)
        reg_win = "<tr>\s*<td>.*slave_assignments.*(Win10Slave-\d+)</a></td>\s*<td>.*</td>\s*<td>.*</td>\s*<td>(.*)</td>.*"
        slave_list = re.findall(reg_win, page_source)
        for slave in slave_list:
            win10_slaves[slave[0]] = slave[1]
        if page_source.find("""<span class="next">""") > 0:
            page_num += 1
        else:
            break
    categorize_slave_status(win10_slaves, "windows")

    page_num = 1
    while True:
        linux_url = "http://slave_url?keyword=linux-slave-rancher2-" % page_num
        page_source = get_html_source(linux_url)
        reg_linux = "<tr>\s*<td>.*slave_assignments.*(linux-slave-rancher2-\d+)</a></td>\s*<td>.*</td>\s*<td>.*</td>\s*<td>(.*)</td>.*"
        slave_list = re.findall(reg_linux, page_source)
        for slave in slave_list:
            linux_slaves[slave[0]] = slave[1]
        if page_source.find("""<span class="next">""") > 0:
            page_num += 1
        else:
            break
    categorize_slave_status(linux_slaves, "linux")
