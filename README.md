# koipond
A Raspberry Pi Zero, with an array of sensors, monitors the water temperature of the pond/s, as well as the surrounding air's humidity and temperature levels. 
A UPS Lite V1.2 Power Hat provides more than three hours of backup power to the Raspberry Pi. 
Battery life, alongside environmental data, are logged to a file.

A Zabbix Agent, installed on the Raspberry Pi, reads the 'koipond' data file and relays it to the Zabbix server for monitoring. 
This data pipeline feeds into a Grafana dashboard, which transforms the data into pretty graphs.

## Hardware
* Raspberry Pi Zero
* UPS-Lite 1.2 battery backup

* 1-Wire sensors from Adafruit:
  * Waterproof temperature sensors: [Adafruit Product 381](https://www.adafruit.com/product/381)
  * Air temperature & humidity sensor: [Adafruit Product 4099](https://www.adafruit.com/product/4099)

## Installation
### Install Zabbix Agent on Raspberry Pi
Add the following lines to `/etc/zabbix/zabbix_agentd.conf`:

```bash
# Battery data
UserParameter=koipond.battery_voltage,grep Voltage /home/pi/koipond/pond-data.txt | cut -f3 -d ' '
UserParameter=koipond.battery_percentage,grep Percentage /home/pi/koipond/pond-data.txt | cut -f3 -d ' '

# Water temp sensors
UserParameter=koipond.temperature_sensor1,grep Pond-1 /home/pi/koipond/pond-data.txt | cut -f3 -d ' '
UserParameter=koipond.temperature_sensor2,grep Pond-2 /home/pi/koipond/pond-data.txt | cut -f3 -d ' '
UserParameter=koipond.temperature_sensor3,grep Pond-3 /home/pi/koipond/pond-data.txt | cut -f3 -d ' '
 
# Air temp and humidity
UserParameter=koipond.ambient_temperature,grep "Ambient Temperature" /home/pi/koipond/pond-data.txt | cut -f3 -d ' '
UserParameter=koipond.ambient_humidity,grep "Ambient Humidity" /home/pi/koipond/pond-data.txt | cut -f3 -d ' '
```

Data is then fed via Zabbix to Grafana for visual dashboards.

### Dashboard Visualization
Grafana dashboard displaying pond data:
![Grafana dashboard showing pond data](https://github.com/zinkwazi/koipond/blob/main/image.png?raw=true)

Raspberry Pi hardware setup for the koipond project:
(Not pretty but has been running in a plastic box outside without issue for 1+ year)
![Raspberry Pi setup for koipond project](https://github.com/zinkwazi/koipond/blob/main/pi.jpg?raw=true)

