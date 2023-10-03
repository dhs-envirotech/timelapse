#/bin/bash
networkNumber=""
dhcpcd="dhcpcd.conf"
hostapd="hostapd.conf"
read -p "The name of the wifi network and password will end in a number.
Enter network number: " networkNumber

if [[ -n ${networkNumber//[0-9]/} ]] ;
then
    echo "Not a number. Exiting..."
    exit 1
fi


# write the following to /etc/hostapd/hostapd.conf
ssid="RaspberryPi$networkNumber"
password="raspberrypi$networkNumber"

if [[ -d $hostpad ]]; then
    rm $hostapd
fi

touch $hostapd
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
rsn_pairwise=CCMP" > $hostapd

# Print out wifi network and password
YELLOW='\033[0;33m'
GREEN='\033[0;32m'
RESET='\033[0m'
clear
echo -e "Setup completed!

${YELLOW}SSID:${YELLOW}     ${GREEN}$ssid${RESET}
${YELLOW}PASSWORD:${YELLOW} ${GREEN}$password${RESET}

⚠️  Please reboot to enable all services. Please note your wifi network name and password as 
   your SSH connection will be lost and this access point should start its own."