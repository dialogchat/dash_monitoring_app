# Battery Monitoring App on a PI
Web App for monitoring data from CAN Bus on a RPi.

This Web App is based on the Python-Plotly-Dash Framework. It is running multiple threads. The first thread reads in the Can-Bus data from the PiCan2 Board into a global queue. The second thread takes values from the global queue and filters the CAN messages into different local queques. The third thread runs the dash-app with multiple callbacks updating the values from the local queques into live plotting visualizations. 

#### Sample Image

This App is build as SPA. On the left side, there is a controller panel. On the right side, you will find the visualizations.


#### Instructions

First, install all dependencies in the requirements.txt file:
```
pip install -r requirements.txt
```
