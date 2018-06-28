# Battery Monitoring App on a PI
Web App for monitoring data from CAN Bus on a Raspberry Pi.

This Web App is based on the [Python-Dash by Plotly Framework](https://plot.ly/products/dash/). It is running multiple threads. The first thread reads in the Can-Bus data from the [PiCAN2 Board](http://skpang.co.uk/catalog/pican2-canbus-board-for-raspberry-pi-23-p-1475.html) into a global queue. The second thread takes values from the global queue and filters the CAN messages into different local queques. The third thread runs the dash- web app with multiple callbacks updating the values from the local queques into live plotting visualizations. 

#### Sample Layout

The app layout is build as SPA. On the left side, there is a Control Panel. On the right side, you will find the visualizations.

[image_0]: ./misc/battery_app_sample.png

![alt text][image_0] 

#### Install Instructions

First, install all dependencies in the requirements.txt file:
```
pip install -r requirements.txt
```

