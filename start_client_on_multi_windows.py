from urllib import request
from util.connection import Connection
import configparser
import re
import os
import winrm


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
    return offline_slaves


def get_data(tag):
    config_file = os.path.join(os.getcwd(), "config", "slaves.ini")
    cf = configparser.ConfigParser()
    cf.read(config_file)
    return dict(cf.items(tag))


if __name__ == "__main__":
    win10_slaves_status = {}
    win10_slaves_project = {}
    page_num = 1
    while True:
        win10_url = "http://slave_url/slaves?page=%d&q[name_or_ip_address_or_project_name_or_status_cont]=win10" % page_num
        page_source = get_html_source(win10_url)
        reg_win = "<tr>\s*<td>.*slave_assignments.*(Win10Slave-\d+)</a></td>\s*<td>.*</td>\s*<td>(.*)</td>\s*<td>(.*)</td>.*"
        slave_list = re.findall(reg_win, page_source)
        for slave in slave_list:
            win10_slaves_status[slave[0]] = slave[2]
            win10_slaves_project[slave[0]] = slave[1]
        if page_source.find("""<span class="next">""") > 0:
            page_num += 1
        else:
            break
    offline_slaves = categorize_slave_status(win10_slaves_status, "windows")

    winrm.Session.run_cmd = Connection.new_run_cmd
    slave_config = get_data("Slaves")
    auth_config = get_data("Auth")
    exclude = get_data("Project")["exclude_keyword"]
    for slave_name in offline_slaves:
        if slave_name.lower() in slave_config.keys():
            if win10_slaves_project[slave_name].find(exclude) < 0:
                try:
                    new_session = Connection.connect_remote_windows(slave_config[slave_name.lower()], auth_config["name"], auth_config["passwd"])
                    Connection.run_command(new_session, r"C:\java_farm_client\run_client.bat", True)
                    print(f"{slave_name} start farm client success")
                except Exception as e:
                    print(f"--{slave_name} start farm client FAIL, error is {str(e)}--")
            else:
                print(f"{slave_name} not start farm client because of exclusion")
        else:
            print("the slave name is not in configuration data")

