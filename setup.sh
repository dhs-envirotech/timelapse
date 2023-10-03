#/bin/bash

echo "DO NOT RUN. THIS SCRIPT IS NOT FULLY DEVELOPED AND MANAGES LINUX DAEMONS. EXITING."
exit 1

# Variables
dhcpcd="dhcpcd.conf"
hostapd="hostapd.conf"
networkNumber=""

read -p "The name of the wifi network and password will end in a number.
Enter network number: " networkNumber

if [[ -n ${networkNumber//[0-9]/} ]] ;
then
    echo "Not a number. Exiting..."
    exit 1
fi

cd /home/pi

sudo apt update
sudo apt -y upgrade

sudo apt install -y hostapd dnsmasq imagemagick ffmpeg

# https://www.raspberrypi.com/documentation/computers/configuration.html#before-you-begin
sudo systemctl unmask hostapd
sudo systemctl enable hostapd

sudo DEBIAN_FRONTEND=noninteractive apt install -y netfilter-persistent iptables-persistent

# Add the following to the end of /etc/dhcpcd.conf
if ! grep -Fxq "nohook" $dhcpcd; then
    # \n -> new line
    # \t -> tab
   printf "\ninterface wlan\n\t0static ip_address=192.168.4.1/24\n\tnohook wpa_supplicant" >> $dhcpcd
else
    echo "$dhcpcd already setup. Skipping..."
fi

# https://www.raspberrypi.com/documentation/computers/configuration.html#wifi-cc-rfkill
sudo rfkill unblock wlan

# write the following to /etc/hostapd/hostapd.conf
$ssid="RaspberryPi$networkNumber"
$password="raspberrypi$networkNumber"
rm $hostapd
echo "country_code=US
interface=wlan0
ssid=$ssid
hw_mode=g
channel=7
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=$password
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP"

# Print out wifi network and password
echo "Setup completed!

SSID:     $ssid
PASSWORD: $password

Please reboot to enable all services. Please note your wifi network name and password as your SSH connection will be lost and this access point should start its own. `sudo reboot now`."