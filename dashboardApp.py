import pygal 
import csv
import socket
from sys import exit
import os 
import time
import webbrowser

#defined passwords and number of reattempts
allowedReattempts = 2
password = 'password'


#path to the file where the data is stored

#ip address of rasberry pi and port we want to connect to
serverHost = ""  
serverPort = 12345

#path to the file that the data will be stored in after being transferred
filePath = ""
#path to the html file that the dashboard app display is in
pathToDashboardApp = ""


#function that asks user for a password and validates if it is true or not
def passwordChecker():
	#setting allowed access to false and setting how many the attemps the user has had
	allowedAccess = False
	attempts = 0


	#input message
	passwordQuestion = input('Please enter the password to access the dashboard application: ')

	
	while attempts < allowedReattempts:
		#checking if password input is not the same as password	
		if passwordQuestion != password:
			passwordQuestion = input('\nThe password you entered was not correct please try again: ')
		#if password input is the same as password set allowed access to true and break from loop
		elif passwordQuestion == password:
			allowedAccess = True
			break
		#increment attempts by one
		attempts += 1
	#return wheather allowed access is true or false	
	return allowedAccess

#function that is reaching out to listening socket
def receiveFileFromServer(host, port, savePath):
	#creating socket instance
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Connecting to listening socket 
    clientSocket.connect((host, port))

    #creating file if the one at the path specified does not exist 
    os.makedirs(os.path.dirname(savePath), exist_ok=True)  

    #opening file that data will be written to in write binary mode
    with open(savePath, "wb") as file:
    	#receiving data in chunks of 1024 bytes 
        data = clientSocket.recv(1024)
        while data:
        	#everytime data received it is written to file
            file.write(data)
            data = clientSocket.recv(1024)

    print("File received successfully")



#creating csv reader that will be used in all graph functions to read each row of csv file
def csvFileReader(fileToRead):
	reader = csv.reader(fileToRead)
	row = list(reader)
	return row

#class that contains all of the functions that create and render graphs	
class Graphs:
	#initialising Graphs class attribute 
	def __init__(self, fileIn):
		#self.f is the file that data is in 
		self.f = fileIn
	
	
	
	#function that creates line chart that 
	def brakingGforcesAgainstTotalAccelerationLineChart(self):
		#creating a list for both acceleration and G-forces that will hold all of the figures to plot 
		accelerationValueList = []
		gForceValueList = []
		
		#creating the chart and setting its attributes
		lineChart = pygal.Line()
		lineChart.title = 'Total Acceleration And Braking G-Forces Being Displayed On a Line Chart'
		lineChart.x_labels = map(str, range(0, 200, 20))
		
		#opening file in read mode
		with open(self.f, 'r') as f:
			 
			#calling function to create csv reader
			row = csvFileReader(f)
			

			#looping through data file 
			for i, element in enumerate(row):
				#disregarding the first line in the file as these are titles 
				if i == 0:
					pass
				else:
					#adding acceleration value to a list
					accelerationValueList.append(float(element[1]))
					#disregarding braking G-Forces value if it is equal to N/A
					if element[0] == 'N/A':
						pass
					else:
						#if not equal to N/A adding it to a list
						gForceValueList.append(float(element[0]))
			#closing the file
			f.close()
		
		
		#adding two lines to chart passing the corresponding list as the values that will be plotted	
		lineChart.add('Total Acceleration', accelerationValueList)
		lineChart.add('Braking G-Forces', gForceValueList)
		
		#returning line chart
		return lineChart
		
	
	#function that creates a horizontal bar chart which displays the highest values for acceleration and braking G-Forces	
	def highestTotalAccelerationAndHighestBrakingGForcesHorizontalChart(self):
		#variables that will hold the current highest values for each measurement
		highestCurrentTotalAcceleration = 0
		highestCurrentBrakingGForces = 0
		
		#creating horizontal bar chart 
		barChart = pygal.HorizontalBar()
		barChart.title = 'Highest Total Acceleration And Highest Braking G-Forces'
		
		#opening the data file in read mode
		with open(self.f, 'r') as f:
			
			#calling function to create csv reader
			row = csvFileReader(f)
			
			#looping through data file
			for i, element in enumerate(row):
				#disregarding first line as it is the titles
				if i == 0:
					pass
					
				else:
					#disregarding any braking G-Forces value that is eqaul to N/A
					if element[0] == 'N/A':
						pass
					else:
						#comparing the current highest value for braking G-Forces with the one in the line and if the one that is in the current line is higher assigning that value to the variable  
						if float(element[0]) > highestCurrentBrakingGForces:
							highestCurrentBrakingGForces = float(element[0])
						
				#disregarding first line as it is the titles
				if i == 0:
					pass
				else:
					#comparing the current highest value for total acceleration with the one in the line and if the one that is in the current line is higher assigning that value to the variable 
					if float(element[1]) > highestCurrentTotalAcceleration:
						highestCurrentTotalAcceleration = float(element[1])
					
					
		#closing the file				
		f.close()
		
		#creating bars in the chart and assigning their values to the current total highest values for each measurement	
		barChart.add('Highest Total Acceleration Value', highestCurrentTotalAcceleration)
		barChart.add('Highest Braking G-Forces Value', highestCurrentBrakingGForces)
		
		#returning bar chart
		return barChart
		
	
	
	#function that creates a bar chart that displays the average's for roll pitch and yaw
	def averageRollPitchYawBarChart(self):
		
		#variables that will hold a running total of the values
		totalRoll = 0
		totalYaw = 0
		totalPitch = 0
		
		#variables that will hold a running total of how many values there are
		totalRollValues = 0
		totalYawValues = 0
		totalPitchValues = 0
		
		
		#creating the bar chart
		barChart = pygal.Bar()
		barChart.title = 'Average Roll, Pitch And Yaw Values'
		
		
		
		#opening data file in read mode
		with open(self.f, 'r') as f:
			
			#calling function to create csv reader
			row = csvFileReader(f)
			
			
			#looping through data file 
			for i, element in enumerate(row):
				
				#disregarding first line in file as it holds titles 
				if i == 0:
					pass
				else:
					#adding the values to their corresponding totals and incrementing the number of each values by one
					totalRoll = totalRoll + float(element[2])
					totalRollValues += 1
					totalYaw = totalYaw + float(element[4])
					totalYawValues += 1
					totalPitch = totalPitch + float(element[3])
					totalPitchValues += 1
					
			#closing the file
			f.close()
		
		
		#finding the average's for each value by dividing the totals by the total amount of values and rounding the results to 0 decimal places
		averageRoll = round(totalRoll/totalRollValues, 0)
		averagePitch = round(totalPitch/totalPitchValues, 0)
		averageYaw = round(totalYaw/totalYawValues, 0)
		
		#adding bars to the chart that display average values
		barChart.add('Roll', averageRoll)
		barChart.add('Pitch', averagePitch)
		barChart.add('yaw', averageYaw)
		
		#returning bar chart
		return barChart
	

	
	#function that creates a line chart that displays all of the recorded environmental data
	def environmentalValuesLineChart(self):
		#lists that will hold all of the data that will be plotted 
		temperature = []
		humidity = []
		pressure = []

		#opening data file
		with open(self.f, 'r') as f:

			#creating csv reader
			row = csvFileReader(f)

			#creating line chart and setting title
			lineChart = pygal.Line()
			lineChart.title = 'environmental values'

			#looping through the data
			for i, element in enumerate(row):
				#skipping first line
				if i == 0:
					pass

				else:
					#appending data to corresponding lists
					temperature.append(float(element[7]))
					humidity.append(float(element[8]))
					pressure.append(float(element[6]))


			#closing file 
			f.close()

		#adding data to chart	
		lineChart.add('Temperature', temperature)
		lineChart.add('Humidity', humidity)
		lineChart.add('Pressure', pressure)

		#returning chart
		return lineChart
			    
	#function that creates a line chart that displays acceleration over time	
	def accelerationOverTimeLineChart(self):
		#creating lists that will hold data 
		acceleration = []
		time = []


		#creating line chart and setting titles 
		lineChart = pygal.Line(x_label_rotation=20)
		lineChart.title = 'Acceleration Versus Time'
		lineChart.x_title = 'Time'
		lineChart.y_title = 'Acceleration'

		#opening csv file
		with open(self.f, 'r') as f:
			#creating csv reader
			row = csvFileReader(f)

			#looping through data
			for i, element in enumerate(row):
				#skips first line
				if i == 0:
					pass
				else:
					#appends data to corresponding lists
					time.append(element[5])
					acceleration.append(float(element[1]))
			#closing file 			
			f.close()

		#adding acceleration data to chart and setting the time values as the labels for the x axis	
		lineChart.add('Acceleration', acceleration)
		lineChart.x_labels = time


		#returning chart
		return lineChart

	#function that creates chart that displays braking G-Forces over time	
	def brakingGForcesOverTimeLineChart(self):
		#lists that will hold data
		gForces = []
		time = []

		#creating line chart and setting titles
		lineChart = pygal.Line(x_label_rotation=20)
		lineChart.title = 'G-Forces Exerted Over Time'
		lineChart.x_title = 'Time'
		lineChart.y_title = 'G-Forces'

		#opening data file
		with open(self.f, 'r') as f:
			#creating csv reade
			row = csvFileReader(f)

			#looping through data 
			for i, element in enumerate(row):
				#skips first line
				if i == 0:
					pass
				else:
					#checks if braking G-forces is equal to N/A
					if element[0] == 'N/A':
						pass
					else:
						#if not == N/A appends the rows data to corresponding lists 
						time.append(element[5])
						gForces.append(float(element[0]))

			#closing file			
			f.close()

		
		#adding data to chart and setting x axis labels to the time data 	
		lineChart.add('Braking G-Forces', gForces)
		lineChart.x_labels = time

		#returning chart 
		return lineChart


#function renders all graphs on one dashboard 
def createAndRenderCharts():
	#setting valid input to true
	validInput = True

	while validInput:
		userOption = input('Please Enter Y to launch the dashboard application and N to end the program: ')
		#checks if user inputted y if so valid input is set to false so loop ends 
		if userOption.lower() == 'y':
			validInput = False 
		#if user input is n program ends
		elif userOption.lower() == 'n':
			validInput = True
			exit()
		#if not n or y loop reoccurs 
		elif userOption.lower() == 'y' and userOption.lower() != 'n':
			pass 

	#calling function for password verification		
	passwordVerification = passwordChecker()
	
	#if password verification is passed program continues if not prgram ends
	if passwordVerification == True:
		pass
	else:
		print("You have failed password verification the program will end now")
		time.sleep(3)
		exit()


	#calling function that creates socket and writes data to file/// try and except block us for if socket isn't created on raspberry pi yet 	
	try:
		receiveFileFromServer(serverHost, serverPort, filePath)
	except ConnectionRefusedError:
		print('The socket has not been created yet turn off the program that is on the Raspberry Pi and try again')
	
	#creating an instance of the Graphs class passing through the path to the data file
	graphs = Graphs(filePath)


	#calling functions that will create and return all charts
	brakingGForcesAgainstTotalAccelerationLineChartInstance = graphs.brakingGforcesAgainstTotalAccelerationLineChart()
	highestTotalAccelerationAndHighestBrakingGForcesHorizontalChartInstance = graphs.highestTotalAccelerationAndHighestBrakingGForcesHorizontalChart()
	averageRollPitchYawBarChartInstance = graphs.averageRollPitchYawBarChart()
	environmentalValuesLineChartInstance = graphs.environmentalValuesLineChart()
	accelerationOverTimeLineChartInstance = graphs.accelerationOverTimeLineChart()
	brakingGForcesOverTimeLineChartInstance = graphs.brakingGForcesOverTimeLineChart()


	#html layout // this is how the dashboard is structured
	htmlLayout = f"""
	<!DOCTYPE html>
	<html>

	<head>
		<title>Dasboard</title>

	</head>

	<body>
	<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px;">
		<div style="border: 1px solid #ddd; padding: 10px;">
			<img src="{brakingGForcesAgainstTotalAccelerationLineChartInstance.render_data_uri()}"/>
		</div>

		<div style="border: 1px solid #ddd; padding: 10px;">
			<img src="{highestTotalAccelerationAndHighestBrakingGForcesHorizontalChartInstance.render_data_uri()}"/>
		</div>

		<div style="border: 1px solid #ddd; padding: 10px;">
			<img src="{averageRollPitchYawBarChartInstance.render_data_uri()}"/>
		</div>

		<div style="border: 1px solid #ddd; padding: 10px;">
			<img src="{environmentalValuesLineChartInstance.render_data_uri()}"/>
		</div>

		<div style="border: 1px solid #ddd; padding: 10px;">
			<img src="{accelerationOverTimeLineChartInstance.render_data_uri()}"/>
		</div>

		<div style="border: 1px solid #ddd; padding: 10px;">
			<img src="{brakingGForcesOverTimeLineChartInstance.render_data_uri()}"/>
		</div>





	</div>
		
	</body

	</html>

	"""

	#opening file and writing html layout to it // creates file if it does not already exist
	with open('dashboard.html', 'w') as htmlFile:
		htmlFile.write(htmlLayout)

		
	#opens the created html file in browser
	webbrowser.open('dashboard.html')


#calling the function that calls all functions
if __name__ == '__main__':
	createAndRenderCharts()		
		
		
		
		
