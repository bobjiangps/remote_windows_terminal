# remote_windows_terminal
connect and run command on remote windows as what you can do on remote linux / 连接远程的windows机以及运行命令行，就像连接linux和运行linux命令差不多的操作

need to turn on winrm service on windows.
* winrm quickconfig
* winrm set winrm/config/service/auth @{Basic="true"}
* Enable-WSManCredSSP -Role Server -Force
* Set-Item -Path "WSMan:\localhost\Service\Auth\CredSSP" -Value $true

sample picture:
![Image text](https://www.byincd.com/media/upload/Bo/2019/03/26/command_remote_win_Fb9zbGf.png)
