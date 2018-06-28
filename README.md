# Battery Monitoring App on a Raspberry PI
Web App for real-time monitoring data from CAN Bus on a Raspberry Pi.

This Web App is based on the [Python-Dash by Plotly Framework](https://plot.ly/products/dash/). It is running multiple threads. The first thread reads in the Can-Bus data from the [PiCAN2 Board](http://skpang.co.uk/catalog/pican2-canbus-board-for-raspberry-pi-23-p-1475.html) into a global queue. The second thread takes values from the global queue and filters the CAN messages into different local queques. The third thread runs the dash-web app with multiple callbacks updating the values from local queques into live plotting visualizations. 

#### Layout and HW Description

The app layout is build as SPA. On the left side, there is a Control Panel with various buttons the charge or stop charging the battery pack. On the right side, you will find visualizations for cell temperature and voltages.

[image_0]: ./misc/battery_app_sample.jpg
![alt text][image_0] 

Here is the an example of the complete Hardware Setup. There are two battery packs equipped with 6 battery cells each and a Battery Monitoring System (BMS). Each BMS sends out Voltages and Temperatures via CAN bus to the RPi (in the middle of the Picture). The Pi is connected to the internet (here: ethernet, or use wlan) and the Battery Monitoring Web App is diplayed in the browser of the host PC. You can see live plotting of Voltages and Temperatures of right Battery Pack (blue and green) while the left Battery Pack is currently disconnected (red Values).

[image_1]: ./misc/liveplotting_hw_setup.jpg
![alt text][image_1]

#### Install Instructions

First, install all dependencies in the requirements.txt file:
```
pip install -r requirements.txt
```

