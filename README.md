# Battery Monitoring App on a PI
Web App for monitoring data from CAN Bus on a Raspberry Pi.

This Web App is based on the [Python-Dash by Plotly Framework](https://plot.ly/products/dash/). It is running multiple threads. The first thread reads in the Can-Bus data from the [PiCAN2 Board](http://skpang.co.uk/catalog/pican2-canbus-board-for-raspberry-pi-23-p-1475.html) into a global queue. The second thread takes values from the global queue and filters the CAN messages into different local queques. The third thread runs the dash- web app with multiple callbacks updating the values from the local queques into live plotting visualizations. 

#### Sample Layout

The app layout is build as SPA. On the left side, there is a Control Panel. On the right side, you will find the visualizations.

[image_0]: ./misc/battery_app_sample.png
![alt text][image_0] 

Here is the an example of the complete Hardware Setup. There are two Battery Packs equipped with 6 Cells each and Battery Monitoring System (BMS). Each BMS sends out Voltages and Temperatures via CAN bus to the RPi (in the middle of the Picture). The Pi is connected to the internet (here: ethernet, or use wlan) and the Battery Monitoring Web App is diplayed in the browser of the host PC. You can see live plotting of Voltages and Temperatures of right Battery Pack (blue and green) while the left Battery Pack is currently disconnected (red Values).

[image_1]: ./misc/liveplotting_hw_setup.jpg
![alt text][image_1]

#### Install Instructions

First, install all dependencies in the requirements.txt file:
```
pip install -r requirements.txt
```

