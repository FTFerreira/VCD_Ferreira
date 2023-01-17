#This program estimates the speed and distance during braking, according to the following input's:
#- Dynamic friction coefficient
#- Initial speed
#- Road inclination angle
#- A final plot is saved in pdf

#import libraries
import numpy as np
import matplotlib.pyplot as plt

#Dynamic friction coefficient input and validation
fcoef = float(input("Please input the dynamic friction coefficient between 0.05 and 0.5: "))
if fcoef<0.05 or fcoef>0.5:
    print("Value is not valid!")
    print("The value has to be between 0.05 and 0.5!")

#Velocity input and validation
velocity = float(input("Please input the initial velocity (in km/h) of the vehicle: "))
if velocity <= 0:
    print("Value is not valid! Velocity value needs to be higher than 0!")
    quit()

#Inclination of the road input and validation
inc = float(input("Please input the inclination angle (in %) between -15 to 15, with positive for uphill"
                    " and negative for downhill: "))
if inc < -15 or inc > 15:
    print("Value is not valid! Inclination value out of range!")
    quit()

#Reaction time input and validation
rTime = float(input("Please input the breaking reaction time (in seconds): "))
if rTime < 0:
    print("Value is not valid! Reaction time value needs to be equal or higher than 0!")
    quit()

fileName = str(input("Please write the file name for your pdf: "))

#Convert velocity from Km/h to m/s
v0 = velocity/3.6

#Convert inclination % to theta angle in rad
thetarad = np.arctan(inc/100)

#Compute distance of stop
Sstop = (v0**2)/(2*9.81*(fcoef*np.cos(thetarad)+np.sin(thetarad)))

#Compute the time needed to stop
Tstop = (Sstop/(1.5*v0))

#Compute de-acceleration
a = v0/Tstop

#Define a vector equally spaced (50 values) in time for the braking period
time = np.linspace (rTime,Tstop+rTime)

#Add a need element to the time vector to include t = 0
tZero = [0]
time = np.concatenate([tZero, time])

#Computing velocity along time
v = 3.6*(v0 - a*(time-rTime))
#Adjust speed values to V0 value during the reaction time
v[0] = velocity
v[1] = velocity

#Computing position along time
s = v0*time + 0.5*a*(time**2)

#Define plot
fig, ax = plt.subplots(figsize = (12, 6))
plt.title('Distance and Velocity vs Time')

#Define double Y axis graph
ax2 = ax.twinx()

#Define graph colors
ax.plot(time, s, color = 'g')
ax2.plot(time, v, color = 'b')

# naming the x axis
ax.set_xlabel('Time (s)')

# naming the y axis
ax.set_ylabel('Distance (m)', color = 'g')
ax2.set_ylabel('Velocity (Km/h)', color = 'b')

# add information about the DFC and road inclination to the plot
plt.text(0.01, 0.95, 'Dynamic friction coefficient: '+str(fcoef), fontsize=11, transform=plt.gcf().transFigure)
plt.text(0.01, 0.91, 'Road inclination: '+str(inc)+'%', fontsize=11, transform=plt.gcf().transFigure)

# save figure in pdf file
plt.savefig(fileName+'.pdf')

# function to show the plot
plt.show()