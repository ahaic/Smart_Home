
#!/bin/sh
# LINKSYS WRT1200AC

# MQTT broker settings
BROKER="your_broker_ip"
PORT="1883"
USERNAME="your_username"
PASSWORD="your_password"
TOPIC="your_topic"

# Get router uptime in seconds
uptime_seconds=$(cut -d' ' -f1 /proc/uptime)
# Convert uptime to hours
uptime_hours=$(echo "$uptime_seconds / 3600" | bc)
# Get WAN IPv4 address
wan_ip_v4=$(ip -4 addr show dev wan | awk '/inet/{print $2}' | cut -d'/' -f1)
# Get WAN IPv6 address
wan_ip_v6=$(ip -6 addr show dev wan | awk '/inet6/{print $2}' | awk 'NR==1{print}' | cut -d'/' -f1)
# Get current date and time in ISO 8601 format
last_update=$(date -Iseconds)
# Get ping latency to example.com
ping_output=$(ping -c 1 $BROKER)
latency=$(echo "$ping_output" | awk '/time=/{print $7}' | cut -d '=' -f 2)
# Connect to MQTT broker and publish data
mosquitto_pub -h $BROKER -p $PORT -u $USERNAME -P $PASSWORD -t $TOPIC -m "{\"uptime\": \"$uptime_hours hours\", \"wan_ip_v4\": \"$wan_ip_v4\", \"wan_ip_v6\": \"$wan_ip_v6\",\"latency\": \"$latency\", \"last_updated\": \"$(date +%s)\"}"
# Print status message
echo "MQTT message sent: uptime=$uptime_hours hours, wan_ip_v4=$wan_ip_v4, wan_ip_v6=$wan_ip_v6,latency=$latency,last_update=$last_update"