import winrm
import sys
import configparser
import os


def run_command(session, command, not_wait_flag=False):
    if command == "q":
        sys.exit()
    else:
        result = session.run_cmd(command, not_wait=not_wait_flag)
        if not_wait_flag:
            print("not wait for response")
            return None
        else:
            if result.status_code:
                print("get error, check your command for windows")
                print(result.std_err.decode("utf-8"))
            output = result.std_out.decode("utf-8")
            print(output)
            return output


def connect_remote_windows(ip, name, passwd):
    s = winrm.Session('http://%s:5985/wsman' % ip, auth=(name, passwd), transport='ntlm')
    return s


def get_data(tag):
    config_file = os.path.join(os.getcwd(), "config", "slaves.ini")
    cf = configparser.ConfigParser()
    cf.read(config_file)
    return dict(cf.items(tag))


def new_run_cmd(self, command, not_wait=False, args=()):
    print("override cmd function")
    shell_id = self.protocol.open_shell()
    command_id = self.protocol.run_command(shell_id, command, args)
    if not_wait:
        return None
    else:
        rs = winrm.Response(self.protocol.get_command_output(shell_id, command_id))
        self.protocol.cleanup_command(shell_id, command_id)
        self.protocol.close_shell(shell_id)
        return rs


if __name__ == "__main__":
    winrm.Session.run_cmd = new_run_cmd
    slave_config = get_data("Slaves")
    auth_config = get_data("Auth")
    if len(sys.argv) <= 1:
        raise NameError("please assign one windows name")
    else:
        new_session = connect_remote_windows(slave_config[sys.argv[-1].lower()], auth_config["name"], auth_config["passwd"])
        while True:
            new_command = input("Command > ")
            if new_command.find("run_client") >= 0:
                run_command(new_session, new_command, True)
            else:
                run_command(new_session, new_command)
