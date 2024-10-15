# IoT-Sensor-Logging-System-For-Electric-Go-Kart
A Python based sensor logging package that is desinged for monitoring and analysing telemetry data from an electric go-kart. The system collects data using a Rasberry Pi Sense HAT and visualises the data using Pygal, providing insights into performance to help in go-kart optimisation. Creating this system was a part of my coursework for my IoT module, but I belive that I went above an beyond therefore I have posted it to my GitHub.

## Features
- Real time data collection using a Raspberry Pi Sense Hat
- Data transmission using WebSockets
- Data visualisation using Pygal

## Installation and Setup
- Clone the repository using the `git clone` command
- Navigate to the project directory: `cd repo-name`
- Change the fileToSend variable in the app.py script to the path of the file that the data will be saved to on the Raspberry PI. For a file named file.txt that is in the same directory as the script this is what it would be `./file.txt`
- Change the serverHost variable in the dashboardApp.py script to the IP address of the Raspberry PI
- Change the filePath variable in the dashboardApp.py script to the path of the file that the collected data will be stored in after transmission
- Change the pathToDashboardApp varible in the dashboardApp.py script to the path of the file that the html file containg all of the graphs will be saved to
- Move the app.py script to the Raspberry PI with a Sense Hat. Move the dashboardApp.py script to the computer that will be used to display the graphs
- Install the app.py files requirements by running `pip install app.py`
- Install the dashboardApp.py files requirements by running `pip install dashboardApp.py`
- Run the app.py script on the Raspberry PI
- Press the button down on the Sense Hat to start collecting data and press it down again to stop
- Once the button has been pressed down to stop data collection run the dashboardApp.py script on the computer
- The dashboardApp.py script will open your web browser and the 6 graphs will be displayed


