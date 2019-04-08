# slowloris-py
Slowloris attack implementation

Project implemented for ECED 4404 (Dalhousie University)

Implemented by Derek Capone and Finlay Miller

This is the code we used to perform a slowloris attack an Apache server running
 on a Raspberry Pi 0 W. Slowloris attacks function by opening as many 
 connections as possible to the target server and trickling data just slowly
 enough so that the server doesn't close the connection.
 
The logging functions are used to measure the impact of the attack on the target
and transmit the data over an MQTT network. More information on running the
scripts can be found [here](https://github.com/finlaymiller/mqtt_logger).
