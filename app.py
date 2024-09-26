from sense_hat import SenseHat
import csv 
import time
from math import sqrt
from sys import exit
import datetime as dt
import socket

#creating an instance of the SenseHat class and clearing the screen
s = SenseHat()
s.clear()

#constant value for how much time delay between cycles of measuring there is
TIME_BETWEEN_DETECTION_CYCLES = 1
G_FORCE_THRESHOLD_VALUE = 1

#constants that control the speed of the signals
ARROW_ROTATION_SPEED = 0.1
SCROLLING_MESSAGE_SCROLL_SPEED = 0.1
PITCH_SIGNAL_ANIMATION_SPEED = 0.1
PITCH_SIGNAL_CYCLES = 3
ACCELERATION_SIGNAL_DISPLAY_TIME_PAUSE = 2

#variables assigned to their colours
green = (0, 255, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
white = (255,255,255)
nothing = (0,0,0)
orange = (255, 153, 51)








#function that creates socket that listens and sends file 
def startSocketListening(host, port, filePath):
    #creating socket and setting it to listen
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((host, port))
    serverSocket.listen(1)

    print(f"Server listening on {host}:{port}")
    
    
    while True:
        #printing the client connection
        clientSocket, clientAddress = serverSocket.accept()
        print(f"Connection from {clientAddress}")
        
        #opening file in read mode
        with clientSocket, open(filePath, "rb") as file:
            #sending data when connection made
            data = file.read(1024)
            while data:
                #continues sending until no more data left
                clientSocket.send(data)
                data = file.read(1024)

        print("File sent successfully")
        break  



#function takes in an image displays that image to matrix then rotates the matrix clockwise for effect of rotating arrow  
def rotateArrowClockwise(arrow):
    s.set_pixels(arrow)
    time.sleep(ARROW_ROTATION_SPEED)
    s.set_rotation(90)
    time.sleep(ARROW_ROTATION_SPEED)
    s.set_rotation(180)
    time.sleep(ARROW_ROTATION_SPEED)
    s.set_rotation(270)
    time.sleep(ARROW_ROTATION_SPEED)
    s.set_rotation(0)
    time.sleep(ARROW_ROTATION_SPEED)
    
#function takes in an image displays that image to matrix then rotates the matrix anticlockwise for effect of rotating arrow     
def rotateArrowAntiClockwise(arrow):
    s.set_pixels(arrow)
    time.sleep(ARROW_ROTATION_SPEED)
    s.set_rotation(270)
    time.sleep(ARROW_ROTATION_SPEED)
    s.set_rotation(180)
    time.sleep(ARROW_ROTATION_SPEED)
    s.set_rotation(90)
    time.sleep(ARROW_ROTATION_SPEED)
    s.set_rotation(0)
    time.sleep(ARROW_ROTATION_SPEED)
    
    
#class that contains all of the functions that display the signal and values to the LED matrix
class Signals:
    #initialising classes attributes self.listOfValues is the list that is created by the getAllValueList function
    def __init__(self, listOfValues):
        self.listOfValues = listOfValues
    
    #function that displays signal for pitch and the pitch value
    def pitchSignal(self):
        #clearing screen before displaying signal
        s.clear()
        
        #assigning colours to make it easier to create the lists
        w = white
        g = green
  
  
        #all of the images that make up the signal that will be displayed in order to create the effect of animation
        img1 = [
        w,w,w,w,w,w,w,w,
        w,w,w,w,w,w,w,w,
        w,w,w,w,w,w,w,w,
        w,g,g,g,g,g,g,w,
        w,g,g,g,g,g,g,w,
        w,w,w,w,w,w,w,w,
        w,w,w,w,w,w,w,w,
        w,w,w,w,w,w,w,w
        ]
    
        img2 = [
            w,w,w,w,w,w,w,w,
            w,w,w,w,w,w,w,w,
            w,w,g,g,g,g,w,w,
            w,g,g,g,g,g,g,w,
            w,g,g,g,g,g,g,w,
            w,w,g,g,g,g,w,w,
            w,w,w,w,w,w,w,w,
            w,w,w,w,w,w,w,w
            ]
        
        img3 = [
            w,w,w,w,w,w,w,w,
            w,w,w,g,g,w,w,w,
            w,w,g,g,g,g,w,w,
            w,g,g,g,g,g,g,w,
            w,g,g,g,g,g,g,w,
            w,w,g,g,g,g,w,w,
            w,w,w,g,g,w,w,w,
            w,w,w,w,w,w,w,w
            ]



        img4 = [
            w,w,w,g,g,w,w,w,
            w,w,g,g,g,g,w,w,
            w,g,g,g,g,g,g,w,
            w,w,w,g,g,w,w,w,
            w,w,w,g,g,w,w,w,
            w,g,g,g,g,g,g,w,
            w,w,g,g,g,g,w,w,
            w,w,w,g,g,w,w,w
            ]
            
        img5 = [
            w,w,g,g,g,g,w,w,
            w,g,g,g,g,g,g,w,
            w,w,w,g,g,w,w,w,
            w,w,w,g,g,w,w,w,
            w,w,w,g,g,w,w,w,
            w,w,w,g,g,w,w,w,
            w,g,g,g,g,g,g,w,
            w,w,g,g,g,g,w,w
            ]
            
        img6 = [
            w,g,g,g,g,g,g,w,
            w,w,w,g,g,w,w,w,
            w,w,w,g,g,w,w,w,
            w,w,w,g,g,w,w,w,
            w,w,w,g,g,w,w,w,
            w,w,w,g,g,w,w,w,
            w,w,w,g,g,w,w,w,
            w,g,g,g,g,g,g,w
            ]
            
        img7 = [
            w,w,w,g,g,w,w,w,
            w,w,w,g,g,w,w,w,
            w,w,w,g,g,w,w,w,
            w,w,w,g,g,w,w,w,
            w,w,w,g,g,w,w,w,
            w,w,w,g,g,w,w,w,
            w,w,w,g,g,w,w,w,
            w,w,w,g,g,w,w,w
            ]
          
        img8 = [
            w,w,w,g,g,w,w,w,
            w,w,w,g,g,w,w,w,
            w,w,w,g,g,w,w,w,
            w,w,w,w,w,w,w,w,
            w,w,w,w,w,w,w,w,
            w,w,w,g,g,w,w,w,
            w,w,w,g,g,w,w,w,
            w,w,w,g,g,w,w,w
            ]

        img9 = [
            w,w,w,g,g,w,w,w,
            w,w,w,g,g,w,w,w,
            w,w,w,w,w,w,w,w,
            w,w,w,w,w,w,w,w,
            w,w,w,w,w,w,w,w,
            w,w,w,w,w,w,w,w,
            w,w,w,g,g,w,w,w,
            w,w,w,g,g,w,w,w
            ]
            
        img10 = [
            w,w,w,g,g,w,w,w,
            w,w,w,w,w,w,w,w,
            w,w,w,w,w,w,w,w,
            w,w,w,w,w,w,w,w,
            w,w,w,w,w,w,w,w,
            w,w,w,w,w,w,w,w,
            w,w,w,w,w,w,w,w,
            w,w,w,g,g,w,w,w
            ]
        
        img11 = [
            w,w,w,w,w,w,w,w,
            w,w,w,w,w,w,w,w,
            w,w,w,w,w,w,w,w,
            w,w,w,w,w,w,w,w,
            w,w,w,w,w,w,w,w,
            w,w,w,w,w,w,w,w,
            w,w,w,w,w,w,w,w,
            w,w,w,w,w,w,w,w
            ]
            
        #adding all of the images to a list so that it can be iterated through
        listOfImages = [img1, img2,img3,img4,img5,img6,img7,img8,img9,img10,img11]
        
        #variable that contains the value of how many times the loop has looped
        loop = 0
        
        #looping through the list and displaying each image to the matrix and then creating a small time gap inbetween displaying the next signal
        while loop < PITCH_SIGNAL_CYCLES:
            for i in listOfImages:
                s.set_pixels(i)
                time.sleep(PITCH_SIGNAL_ANIMATION_SPEED)
            
            
            loop +=1
            

        
        
        #displaying scrolling message that displays the pitch value
        s.show_message(str(self.listOfValues[3]), text_colour=g, back_colour=w, scroll_speed=SCROLLING_MESSAGE_SCROLL_SPEED)
        
    
    #function that displays the roll signal and the roll value
    def rollSignal(self):
        #assigning colours to their variables
        o = orange
        w = white
        
        
        #imgage that will be displayed
        arrow =[
        o,o,o,o,w,o,o,o,
        o,o,w,w,w,w,o,o,
        o,w,w,w,w,w,o,o,
        o,w,w,o,w,o,o,o,
        o,w,w,o,o,o,o,o,
        o,w,w,w,w,w,w,o,
        o,o,w,w,w,w,o,o,
        o,o,o,o,o,o,o,o
        ] 
        
        
        #variables that control the loop
        rotations = 0
        maxRotations = 3
        
        
        while rotations < maxRotations:
            #calling the function that will rotate the image clockwise
            rotateArrowClockwise(arrow)
            rotations += 1
            
        
        #displaying the go kart's roll value
        s.show_message(str(self.listOfValues[2]), text_colour=w, back_colour=o, scroll_speed=SCROLLING_MESSAGE_SCROLL_SPEED)
        
        
    #function that displays the signal for yaw and the yaw value    
    def yawSignal(self):
        #assigning colours to their variables 
        y = yellow
        n = nothing
        
        #image of arrow facing anti clockwise
        arrow = [
        n,n,n,y,n,n,n,n,
        n,n,y,y,y,y,n,n,
        n,n,y,y,y,y,y,n,
        n,n,n,y,n,y,y,n,
        n,n,n,n,n,y,y,n,
        n,y,y,y,y,y,y,n,
        n,n,y,y,y,y,n,n,
        n,n,n,n,n,n,n,n
        ]
        
        #variables that control the loop 
        maxRotations = 3
        rotations = 0
        
        while rotations < maxRotations:
            #calling the function that will rotate the image anti clockwise and passing the arrow image through it
            rotateArrowAntiClockwise(arrow)
            rotations += 1
        
        
        #displaying the go kart's yaw value as a scrolling message 
        s.show_message(str(self.listOfValues[4]), text_colour=y, back_colour=n, scroll_speed=SCROLLING_MESSAGE_SCROLL_SPEED)
        
        #clearing the screen as the yaw value is the last thing to be displayed to matrix before starting next detection cycle
        s.clear()
    
    
    #function that displays the signal for acceleration and acceleration value    
    def totalAccelerationSignal(self):
        #showing letter A which is the signal
        s.show_letter("A", text_colour=red, back_colour=white)
        time.sleep(ACCELERATION_SIGNAL_DISPLAY_TIME_PAUSE)
        #displaying the go kart's acceleration as a scrolling message
        s.show_message(str(self.listOfValues[1]), text_colour=red, back_colour=white, scroll_speed=SCROLLING_MESSAGE_SCROLL_SPEED)
        
    #function that displays the signal for braking G-Forces and braking G-Forces value
    def brakingGForcesSignal(self):
        #scrolling message of B.G which is the signal 
        s.show_message('B.G', text_colour=blue, back_colour=white, scroll_speed=SCROLLING_MESSAGE_SCROLL_SPEED)
        #displaying the go kart's braking G-Forces value as a scrolling message
        s.show_message(str(self.listOfValues[0]), text_colour=blue, back_colour=white, scroll_speed=SCROLLING_MESSAGE_SCROLL_SPEED)
        
#class that all functions are in which record some measurement
class Measurements:
    def __init__(self,orientationValues):
        self.orientationValues = orientationValues
    
    #detects pitch returns value to zero decimal place
    def detectPitch(self):
        pitch = self.orientationValues["pitch"]
        return round(pitch, 0)
  
      #detects roll returns value to zero decimal places
    def detectRoll(self):
        roll = self.orientationValues["roll"]
        return round(roll, 0)
  
    #detects yaw returns value to zero decimal places
    def detectYaw(self):
        yaw = self.orientationValues["yaw"]
        return round(yaw, 0)
    
    #records current time in H:M:S format    
    def detectTime(self):
        currentTime = dt.datetime.now()
        currentTimeHrMinSec = currentTime.strftime('%H:%M:%S')
        return currentTimeHrMinSec
    
    #detects pressure returns value to zero decimal places
    def detectPressure(self):
        pressure = s.get_pressure()
        return round(pressure, 0)
        
    #detects temperature returns value to zero decimal places 
    def detectTemperature(self):
        temperature = s.get_temperature()
        return round(temperature, 0)
    
    
    #detects temperature returns value to zero decimal places 
    def detectHumidity(self):
        humidity = s.get_humidity()
        return round(humidity, 0)
    
    #detects direction in which sense hat is facing returns value to zero decimal places
    def detectDirectionOfNorth(self):
        direction = s.get_compass()
        return round(direction, 0)
    

#class that all calculations are in     
class Calculations:
    def __init__(self, accelerationValue):
        #setting classes attributes
        self.accelerationValues = accelerationValue
         
    
    #calculates the total amount of G-forces acting on the sense hat returns a value in G-forces
    def calculateGForces(self):    
        x = self.accelerationValues['x']
        y = self.accelerationValues['y']
        z = self.accelerationValues['z']
        gForces = sqrt(x**2 + y**2 + z**2)/9.8
        return round(gForces, 1)
    
    #calculates total acceleration and returns value in metres per second 
    def calculateTotalAcceleration(self):
        x = self.accelerationValues['x']
        y = self.accelerationValues['y']
        z = self.accelerationValues['z']
        totalAcceleration = sqrt(x**2 + y**2 + z**2)
        return round(totalAcceleration, 1)
        
        
#class that any function that are required in the main loop are in         
class MainLoopFunctions:
    
    #function that returns a list of all values that will be saved to file 
    def getAllValueList():
        #instance of calculations class
        calculationInstance = Calculations(s.get_accelerometer_raw())
        
        #Instance of measurements class
        measurementInstance = Measurements(s.get_orientation_degrees())
        
        gForce = calculationInstance.calculateGForces()
        
        #checks if G-Force value is greater than the threshold value if it isn't the value for G-force is set to N/A
        if gForce >= G_FORCE_THRESHOLD_VALUE:
            pass
        else:
            gForce = 'N/A'
        
        #calling all functions from instances of measurements and calculations class
        tAcceleration = calculationInstance.calculateTotalAcceleration()
        roll = measurementInstance.detectRoll()
        pitch = measurementInstance.detectPitch()
        yaw = measurementInstance.detectYaw()
        time = measurementInstance.detectTime()
        pressure = measurementInstance.detectPressure()
        temp = measurementInstance.detectTemperature()
        humidity = measurementInstance.detectHumidity()
        directionNorth = measurementInstance.detectDirectionOfNorth()
        
        #adding all values to a list
        listOfValues = [gForce, tAcceleration, roll, pitch, yaw, time, pressure, temp, humidity, directionNorth]
        
        #returns list 
        return listOfValues
        
    
    
def mainLoop():
    #list of all labels for values that are being recorded 
    listOfTags = ["G-Forces : ", "Total Acceleration : ", "roll : ", "Pitch : ", "Yaw : ", "Time : ", "Pressure : ", "Temperature : ", "Humidity : ", "Direction of North : "]
    listOfTitles = ['Braking G-forces', 'Total Acceleration', 'Roll', 'Pitch', 'Yaw', 'Time', 'Pressure', 'Temperature', 'Humidity', 'Direction of North']
    
    #opening data file in write mode
    with open('data.CSV', 'w') as f:
        #creating csv writer
        csvWriter = csv.writer(f)
        #writing titles to the file
        csvWriter.writerow(listOfTitles)
    
        
        print("Press the Joystick down to begin the program then hold it down to stop it\n")
        while True: 
            #checks if stick input is middle being pressed if so starts loop
            for event in s.stick.get_events():
                if event.direction == 'middle' and event.action == 'pressed':
                    print("Program started\n")
                    time.sleep(0.5)
                    
            
                    while True:
                        #getting all of the values that are needed in a list 
                        listOfValues = MainLoopFunctions.getAllValueList()
                        #creating an instance of the signals class
                        signalsInstance = Signals(listOfValues)
                        
                        #calling all of the signal functions
                        signalsInstance.totalAccelerationSignal()
                        signalsInstance.brakingGForcesSignal()
                        signalsInstance.rollSignal()
                        signalsInstance.pitchSignal()
                        signalsInstance.yawSignal()
            
                        #loops through list of values then prints the values corresponding tag before printing the value then saves element to file 
                        for i, element in enumerate(listOfValues):
                            print(listOfTags[i], element)
                            
    
                            
                            #checking if element is last in the list takes new line in file if true
                            if i == len(listOfValues) - 1:
                                time.sleep(TIME_BETWEEN_DETECTION_CYCLES)
                                print("\n\n")
                        
                        #writing values to file        
                        csvWriter.writerow(listOfValues)
                        
                        #checks to see if stick held up if so closes file and ends program 
                        for event in s.stick.get_events():
                            if event.direction == 'middle' and event.action == 'held':
                                f.close()
                                s.clear()
                                
                                #listens on all available interfaces
                                serverHost = "0.0.0.0"  
                                #port on which client needs to connect
                                serverPort = 12345
                                #file that is going to be sent 
                                fileToSend = ""
                                #starts file server
                                startSocketListening(serverHost, serverPort, fileToSend)
                                exit()
                                print('Program complete')
                            else:
                                pass
                    
                    
                    
                                
                         

#calling main loop function 
if __name__ == "__main__":
    mainLoop()
    
        
        

        

    
