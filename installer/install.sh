# staging
echo [*] Staging process...
mkdir ~/.winlocal
cd ..
mv win/* ~/.winlocal
rm -rf win
cd ~/.winlocal
echo [+] Completed

#  get tools
echo [*] Installing tools...
sudo apt update
sudo apt-get install sshpass
sudo apt-get install python3
echo [+] Completed

# set up alias workflow
echo [*] Setting up alias...
echo "alias winlocal=\"python3 $(pwd)/main.py\"" >> ~/.bashrc
echo "alias winlocal=\"python3 $(pwd)/main.py\"" >> ~/.zshrc
echo [+] Completed

# clean up
echo [+] Installation Completed
echo "- please restart your terminal"
echo "- type 'winlocal' to launch WinLocal"
