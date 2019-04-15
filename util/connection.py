import winrm
import sys


class Connection:

    def run_command(session, command, not_wait_flag=False):
        if command == "q":
            sys.exit()
        else:
            result = session.run_cmd(command, not_wait=not_wait_flag)
            if not_wait_flag:
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

    def new_run_cmd(self, command, not_wait=False, args=()):
        shell_id = self.protocol.open_shell()
        command_id = self.protocol.run_command(shell_id, command, args)
        if not_wait:
            return None
        else:
            rs = winrm.Response(self.protocol.get_command_output(shell_id, command_id))
            self.protocol.cleanup_command(shell_id, command_id)
            self.protocol.close_shell(shell_id)
            return rs
