# koipond
Koi Pond Monitoring with Raspberry Pi, Zabbix and Grafana.

Raspberry Pi Zero with multiple sensors to track pond water temperature as well as ambient air humidity and temperature.
Backup power supplied by a UPS Lite V1.2 Power Hat. 
Battery stats collected and written to the data file along with temperature and humidity data.

Hardware:
* UPS-Lite 1.2 battery backup and Raspberry Pi Zero

* 1-Wire sensors from Adafruit:
  * Waterproof temerature sensors: https://www.adafruit.com/product/381
  * Air temperature & humidity sensor: https://www.adafruit.com/product/4099


Install Zabbix agent on Raspberry Pi
Add the following lines to /etc/zabbix/zabbix_agentd.conf
```
# Battery data
UserParameter=koipond.battery_voltage,grep Voltage /home/pi/koipond/pond-data.txt | cut -f3 -d ' '
UserParameter=koipond.battery_percentage,grep Percentage /home/pi/koipond/pond-data.txt | cut -f3 -d ' '

# Water temp sensors
UserParameter=koipond.temperature_sensor1,grep Pond-1 /home/pi/koipond/pond-data.txt | cut -f3 -d ' '
UserParameter=koipond.temperature_sensor2,grep Pond-2 /home/pi/koipond/pond-data.txt | cut -f3 -d ' '
UserParameter=koipond.temperature_sensor3,grep Pond-3 /home/pi/koipond/pond-data.txt | cut -f3 -d ' '
 snesor
# Air temp and humidity
UserParameter=koipond.ambient_temperature,grep "Ambient Temperature" /home/pi/koipond/pond-data.txt | cut -f3 -d ' '
UserParameter=koipond.ambient_humidity,grep "Ambient Humidity" /home/pi/koipond/pond-data.txt | cut -f3 -d ' '
```

Data is then fed via Zabbix to Grafana for the pretty dashboards.


![alt text](https://github.com/zinkwazi/koipond/blob/main/image.png?raw=true)


![alt text](https://github.com/zinkwazi/koipond/blob/main/pi.jpg?raw=true)
