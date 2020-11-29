"""
Ball-Trampoline Illlusion by Barry Z
ICS 3UI Array Assignment
May 1, 2020
"""

from tkinter import *
from time import *
from math import *
master = Tk()
screen = Canvas(master, width = 1000, height = 1000, background = "white")
screen.pack()



##### CONSTANTS #####

numRings = 6 #Number of rings excluding outermost ring   
numThreads = 36 #Number of threads in each ring          
initialBallDia = 320 #Diameter of ball at its max height 
colour = "purple1" #Colour of trampoline web             
ballColour = "dodgerblue" #Colour of ball                
tFrames = 10 #Duration of trampoline cycle
jFrames = 22 #Duration of ball in free fall before hitting trampoline 



##### INFO FOR TRAMPOLINE RINGS #####

restStateDia = [] #Diameter of each ring in their initial/rest state

minDia = [] #Minimum diameter of each ring

angleA = [] #Used for cosine function that determines each ring's diameter
            #during main cycle

angleB = [] #Used for sine function that determines each ring's diameter
            #when the trampoline vibrates

ring = [] #Array of each screen.create_oval representing the rings

vibrate = [] #Array for how much each ring's diameter increases/decreases by
             #when the trampoline vibrates

#Filling Arrays
for i in range(numRings):
    ringGap = 900/(2*numRings)
    restStateDia.append((900-2*ringGap)-2*ringGap*i)

    shrinkFactor = 0.85*0.8**i
    """ ^^^ Percentage of each ring's rest state diameter that it retains when
    the ring is compressed to its minimum diameter.
    The smaller the second number is, the "bouncier" the trampoline will look.
    Each ring's minimum diameter becomes exponentially smaller, creating a
    "telescope" effect. """
    
    minDia.append(shrinkFactor*restStateDia[i])

    vibrate.append(6*1.37**i)
    
    angleA.append(0) #0 placeholder
    ring.append(0) 
    angleB.append(0)



##### INFO FOR TRAMPOLINE THREADS AND CROSSES #####  

#Cross: Represented by the "X" shaped lines
#Threads: Represented by the lines between the crosses
    
thread = [] #Array of each screen.create_line that represents a thread
cross = [] #Array of each screen.create_line that represents a cross

threadCounter = 0
crossCounter = 0
""" ^^^ These counters keep track of total number of threads and crosses in the
trampoline.
The counters increase by 1 with each thread or cross that's created.
Each thread or cross' index in the "thread[]" or "cross[]" arrays is equal to
the current thread/cross count.
This allows us to delete all the threads/crosses at once via a for loop at the
end of each frame."""

threadAngleEven = [] #Angle of threads in even numbered rings
threadAngleOdd = []  #Angle of threads in odd numbered rings

#Filling arrays
for i in range(numThreads):
    threadAngleEven.append(pi/(numThreads/2)*i) 
    threadAngleOdd.append(pi/numThreads + pi/(numThreads/2)*i) 
    for i in range(numRings):
        thread.append(0)
        for i in range(2):
            cross.append(0)

prevRingDia = [900] #Diameter of previous ring wrapped around it
for i in range(numRings-1):
    prevRingDia.append(0)


xThreadNext = [0,0]
yThreadNext = [0,0]
""" ^^^ 2 ordered pairs of the next thread. These arrays are used for creating
the crosses, which are dependent on the ordered pairs of the current thread
and the next thread adjacent to it).

Since each cross consists of two lines and 4 points, two of which lie on the
next/adjacent thread, we need two indices in these arrays to store the two points."""



##### FUNCTION FOR CREATING RINGS #####

def createRings(ringDia):
    x1 = 500-ringDia/2
    y1 = x1
    x2 = x1 + ringDia
    y2 = x2

    ring[r] = screen.create_oval(x1,y1,x2,y2,outline=colour,width=1)



##### FUNCTION FOR CREATING THREADS AND CROSSES #####
    
def createThreads(prevRingDia,ringDia,threadAngle,threadAngleNext):
    global crossCounter
 
    global threadCounter #"global" keyword allows us to change a variable that was assigned outside the function
    ### Making threads ###
    xThread = (prevRingDia/2)*cos(threadAngle)+500
    yThread = abs((prevRingDia/2)*sin(threadAngle)-500)
    """^^^ This point lies on the ring that encases the current ring,
    hence the use of prevRingDia/2, which is the radius of the previous ring."""


    xThread2 = (ringDia/2)*cos(threadAngle)+500
    yThread2 = abs((ringDia/2)*sin(threadAngle)-500)
    #^^^ This point lies on the current ring that's being created

    thread[threadCounter] = screen.create_line(xThread,yThread,xThread2,yThread2,fill=colour,width=1)

    threadCounter = threadCounter + 1


    ### Making crosses between threads ###
    xThreadNext[0] = (prevRingDia/2)*cos(threadAngleNext)+500
    yThreadNext[0] = abs((prevRingDia/2)*sin(threadAngleNext)-500)
    xThreadNext[1] = (ringDia/2)*cos(threadAngleNext)+500
    yThreadNext[1] = abs((ringDia/2)*sin(threadAngleNext)-500)
    
    crossX = xThread
    crossY = yThread
    crossX2 = xThreadNext[1]
    crossY2 = yThreadNext[1]

    cross[crossCounter] = screen.create_line(crossX,crossY,crossX2,crossY2,fill=colour,width=1)
                                            
    crossCounter = crossCounter + 1
    
    crossX = xThread2
    crossY = yThread2
    crossX2 = xThreadNext[0]
    crossY2 = yThreadNext[0]

    cross[crossCounter] = screen.create_line(crossX,crossY,crossX2,crossY2,fill=colour,width=1)

    crossCounter = crossCounter + 1



#####  INFO FOR BALL DIAMETER  #####

ballDia = initialBallDia

# Array for ball increment
ballIncrement = []
for i in range(26):
    ballIncrement.append(1.7*1.12**i)
""" ^^^The ball diameter is updated each frame by subtracting (if ball is dropping)
or adding (if ball is rising) an increment. This increment increases
exponentially each frame to simulate gravity."""

ballIncrementCounter = 0



##### FUNCTION FOR CALCULATING COORDINATES OF BALL #####

def ballCoordinates(ballDia):
    x1 = 500 - ballDia/2
    y1 = 500 - ballDia/2
    x2 = 500 + ballDia/2
    y2 = 500 + ballDia/2

    ball = screen.create_oval(x1,y1,x2,y2,fill=ballColour)


    screen.update()

    if f==0 or f==tFrames-1: 
        delay = 0.035
    else:
        delay = 0.015


    sleep(delay)
    screen.delete(ball) 



##### ANIMATION #####
    
screen.create_oval(50,50,950,950,outline="black",width=20) #Outermost ring (constant)

while True:
    
    for f in range(tFrames):
        
        for r in range(numRings):
            
            ### Rings animation ###
            a = (restStateDia[r]-minDia[r])/2 #amp = (max-min)/2
            k = (restStateDia[r]+minDia[r])/2 #vertical shift = (max+min)/2
            ringDia = a*cos(angleA[r])+ k

            #Call createRings function
            createRings(ringDia)

            #Update angleA
            if f < (tFrames-1):
                angleA[r] = angleA[r] + 2*pi/(tFrames-1)
            """ ^^^ Spreads 2*pi into a number of equal increments.
            The number of increments is equal to the number of
            frames (excluding first frame, which has already been made),
            so that angleA reaches an integer multiple of 2*pi by the
            final frame.

            We don't update angleA after drawing the last frame
            (when f == (tFrames-1) because we want the current value
            of angleA (an integer multiple of 2*pi) to be the starting
            value of angleA when the loop restarts.
            """

            ### Threads and crosses animation ###  
        
            if r < (numRings-1):
                prevRingDia[r+1] = ringDia
                
            for t in range(numThreads):

                if r%2==0:
                    threadAngle = threadAngleEven[t]
                    if t == (numThreads - 1):
                        threadAngleNext = threadAngleEven[0]
                    else:
                        threadAngleNext = threadAngleEven[t+1]
                else:
                    threadAngle = threadAngleOdd[t]
                    if t == (numThreads - 1):
                        threadAngleNext = threadAngleOdd[0]
                    else:
                        threadAngleNext = threadAngleOdd[t+1]

                #Call createThreads function
                createThreads(prevRingDia[r],ringDia,threadAngle,threadAngleNext)


        ### Ball falls and hits trampoline ###

        if f==0:
        # ^ Stops the trampoline animation at the first frame and starts the animation of the ball's descent   

            """Trampoline animation does not continue until this loop ends
                (aka when the ball "hits" the trampoline)"""
            for j in range(jFrames):
                
                #Call ballCoordinates function
                ballCoordinates(ballDia)

                #Update ballDia by subtracting increment
                ballDia = ballDia - ballIncrement[ballIncrementCounter]

                #Update index for ballIncrement array
                ballIncrementCounter = ballIncrementCounter + 1   


        #Executes until before the final frame (when f == tFrames-1)
        elif f<=(tFrames-2):
            
            #Executes before trampoline rings reach their minimum diameter
            if ballIncrementCounter <= 25:
                ballDia = ballDia - ballIncrement[ballIncrementCounter]

            #Executes after the trampoline rings reach their minimum diameter (when ballIncrementCounter==26)
            else: 
                if ballIncrementCounter == 26:
                    ballIncrement.reverse()
                    """ ^^^ After the ball and trampoline rings reach their
                    minimum diameter (when ballIncrementCounter==26), the ball
                    rebounds and begins to rise. The ball's speed decreases the
                    higher it gets, which means  the increment we update the
                    diameter by must also decrease. Thus, we need to order the
                    array of ballIncrements in decreasing order by reversing it."""
                
                ballDia = ballDia + ballIncrement[ballIncrementCounter-26]
                """             ^^^ we add the increment instead of subtract
                            because the ball is rising and getting biggger """

            ballCoordinates(ballDia)

            ballIncrementCounter = ballIncrementCounter + 1

        for d in range(numRings):
            screen.delete(ring[d])
        for d in range(threadCounter):
            screen.delete(thread[d])
        for d in range(crossCounter):
            screen.delete(cross[d])
        
        #Executes during final frame after the ball leaves the trampoline
        if f == (tFrames-1):
            threadCounter = 0 #Reset counter
            crossCounter = 0  #Reset counter

            energyLoss = 1
            
            for j in range(jFrames):
                for r in range(numRings):
                    
                    ### Trampoline vibrates ###

                    ## Rings Animation ##
                    if j<19:
                        if j>0 and j%6==0:
                            energyLoss = energyLoss*0.9 #Causes trampoline to vibrate less and less
                        
                        a = (restStateDia[r]+vibrate[r]*energyLoss - (restStateDia[r]-vibrate[r]*energyLoss))/2 #amp = (max-min)/2
                        k = (restStateDia[r]+vibrate[r]*energyLoss + (restStateDia[r]-vibrate[r]*energyLoss))/2 #vertical shift = (max+min)/2
                        ringDia = a*sin(angleB[r])+ k

                    else:
                        ringDia = restStateDia[r]

                    createRings(ringDia)

                    if j < 18:
                        angleB[r] = angleB[r] + 2*pi/6


                    ## Threads and crossea animation ##
                    if r < numRings-1:
                        prevRingDia[r+1] = ringDia
                        
                    for t in range(numThreads):
                        if r%2==0:
                            threadAngle = threadAngleEven[t]
                            if t == (numThreads - 1):
                                threadAngleNext = threadAngleEven[0]
                            else:
                                threadAngleNext = threadAngleEven[t+1]
                        else:
                            threadAngle = threadAngleOdd[t]
                            if t == (numThreads - 1):
                                threadAngleNext = threadAngleOdd[0]
                            else:
                                threadAngleNext = threadAngleOdd[t+1]

                        createThreads(prevRingDia[r],ringDia,threadAngle,threadAngleNext)

                ### Ball animation ### 
                ballDia = ballDia + ballIncrement[ballIncrementCounter-26]
                ballCoordinates(ballDia)
                ballIncrementCounter = ballIncrementCounter + 1


                for d in range(numRings):
                    screen.delete(ring[d])
                for d in range(threadCounter):
                    screen.delete(thread[d])
                for d in range(crossCounter):
                    screen.delete(cross[d])

                threadCounter = 0
                crossCounter = 0

        threadCounter = 0 
        crossCounter = 0  

    ballIncrementCounter = 0 #Reset counter
    ballIncrement.reverse() #Flip ballIncrement array back to increasing order
    ballDia = initialBallDia #Reset ball diameter

        
