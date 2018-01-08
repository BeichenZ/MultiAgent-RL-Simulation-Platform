import numpy
from math import sqrt
from time import time

screen_Width = 0
screen_Height = 0
minDistanceWeight = 20

class SheepGroup():
    NEIGHBOR_RADIUS = 200
    IDLE_RADIUS = 60

    def __init__(self,sheepCount,DogCount,screenWidth,screenHeight):
        self.sheepCount = sheepCount
        self.dogCount = DogCount
        global screen_Width
        global screen_Height
        global minDistanceWeight
        screen_Width = screenWidth
        screen_Height = screenHeight
        self.minInterSheepDistance = self.NEIGHBOR_RADIUS/ minDistanceWeight;
        self.SheepList = []
        self.DogList = []
        self.centroid = [screen_Width/2,screen_Height/2]
        self.dogDrivenFlag = False
        self.allSheepIdle = False
        for i in range(sheepCount):
            self.SheepList.append(SingleSheep())
            #Dog and Sheep are mathematically similar in nature. We do not feel a need to have a separate class
            if i < DogCount:
                self.DogList.append(SingleSheep())

    def cleanPreviousState(self):
        self.allSheepIdle = False
        self.dogDrivenFlag = False

    def updateLocations(self):
        #Assumption:All sheeps tend to form one single flocking ultimately
        #Set Flags influencing all sheeps
        self.centroid = self.get_sheep_centroid()
        if(self.all_sheep_in_Radius(self.centroid, self.IDLE_RADIUS)):
            if(self.dog_insight_of_anySheep()):
                self.dogDrivenFlag = True
            else:
                self.allSheepIdle = True

        #Calculate Velocity Change

        if (self.allSheepIdle):
            seedCounter=0;
            for sheep in self.SheepList:
                seedCounter += 1
                numpy.random.seed(int(time())+seedCounter)
                #sheep.velocityX = numpy.sign(numpy.random.randint(-100,100)/100)*numpy.random.randint(-300, 300)/100
                #sheep.velocityY = numpy.sign(numpy.random.randint(-100,100)/100)*numpy.random.randint(-300, 300)/100
                if(sheep.velocityX > sheep.MaxVelocity/10):
                    sheep.velocityX = sheep.velocityX/30
                if(sheep.velocityY > sheep.MaxVelocity/10):
                    sheep.velocityY = sheep.velocityY/30
                sheep.validateParams(IdleMode=self.allSheepIdle)
                sheep.UpdateLocation()
        else:
            #Check if all sheep are within preset radius
            for thisSheep in self.SheepList:
                sheepNeighbors = []
                #Obtain a list of neighboring sheep
                for otherSheep in self.SheepList:
                    if otherSheep == thisSheep:
                        continue #skip for itself
                    distance = thisSheep.distanceTo(otherSheep)
                    if distance < self.NEIGHBOR_RADIUS:
                        sheepNeighbors.append(otherSheep)


                for dog in self.DogList:
                    closeDogs = []
                    distance = thisSheep.distanceTo(dog)
                    if distance < thisSheep.fieldofView:
                        thisSheep.avoidFlag = True
                        closeDogs.append(dog)

                #TO-DO make boids to do random stuff if they do not move
                thisSheep.cohesion(sheepNeighbors)
                thisSheep.alignment(sheepNeighbors)
                thisSheep.separation(sheepNeighbors,minDistance=self.minInterSheepDistance)
                if thisSheep.avoidFlag:
                    thisSheep.flee(closeDogs)

                # Validate Velocity and Update Location Based on current iteration result
                thisSheep.validateParams()
                thisSheep.UpdateLocation()

        return

    def executeDogAction(self,action):
        #Single Dog
        #For 4-Actions Space: up, down,left,right
        ConstantSpeed = 30
        if(action == 0):#Up
            self.DogList[0].velocityY = ConstantSpeed
        elif(action == 1): #Down
            self.DogList[0].velocityY = -ConstantSpeed
        elif(action == 2):#Left
            self.DogList[0].velocityX = -ConstantSpeed
        elif(action ==3 ):#Right
            self.DogList[0].velocityX = ConstantSpeed
        #elif(action == 4):#Stay at where it is
           # self.DogList[0].velocityX = 0
           # self.DogList[0].velocityY = 0
        self.DogList[0].validateParams()
        self.DogList[0].UpdateLocation()
        

        return

    def get_sheep_centroid(self):
        x_sum = 0
        y_sum = 0
        for sheep in self.SheepList:
            x_sum += sheep.X
            y_sum += sheep.Y
        x_average = x_sum / len(self.SheepList)
        y_average = y_sum / len(self.SheepList)
        return [x_average, y_average]

    def get_DogsLocation(self):
        doglocationList = []
        for dog in self.DogList:
            doglocationList.append([dog.X,dog.Y])
        return doglocationList
    def all_sheep_in_Radius(self, centroid, radius):
        for sheep in self.SheepList:
            if (sqrt((centroid[0] - sheep.X) ** 2 + (centroid[1] - sheep.Y) ** 2) > radius):
                return False
        return True

    def dog_insight_of_anySheep(self):
        for sheep in self.SheepList:
            for dog in self.DogList:
                if(sheep.distanceTo(dog) < sheep.fieldofView):
                    return True
        return False



class SingleSheep():
    #Note: the contribution is proportional to 1/Weight, larger the weight, smaller the contribution
    cohesionW_def = 10;
    alignmentW_def = 50;
    separationW_def = 10;
    dog_avoidanceW_def = 10;
    goalW_def = 100;
    MaxVelocity_def = 25;
    FieldofView_def = 180;
    #Place-holder for later Image
    sheepImage_def = "/resource/sheep1.png"


    def __init__(self,X=None,Y=None,
                 cohesionW=cohesionW_def,alignmentW = alignmentW_def,separationW = separationW_def,dog_avoidanceW = dog_avoidanceW_def,
                 MaxVelocity = MaxVelocity_def,FieldofView = FieldofView_def,sheepImage = sheepImage_def):
        global screen_Height
        global screen_Width
        self.X = numpy.random.randint(0, screen_Width) if X is None else X
        self.Y = numpy.random.randint(0, screen_Height) if Y is None else Y

        self.cohesionW = cohesionW;
        self.alignmentW = alignmentW;
        self.separationW = separationW;
        self.dog_avoidanceW = dog_avoidanceW;
        self.MaxVelocity = MaxVelocity;
        self.sheepImagePath = sheepImage;
        self.velocityX = numpy.random.random_integers(0,1000)/100;
        self.velocityY = numpy.random.random_integers(0,1000)/100;
        self.fieldofView = FieldofView;
        self.avoidFlag = False;

        #Initialize Velocity Randomly

    def distanceTo (self,anotherObject):
        x=self.X-anotherObject.X;
        y=self.Y-anotherObject.Y;
        return sqrt(x*x+y*y)

    def cohesion(self,neighborList):
        neighborCount = len(neighborList)
        if neighborCount<1:
            return

        average_x = 0
        average_y = 0
        for neighborSheep in neighborList:
            # TO-DO: Two sheep cannot on same-point.Need to change!
            if neighborSheep.X == self.X and neighborSheep.Y == self.Y:
                continue

            average_x += (self.X - neighborSheep.X)
            average_y += (self.Y - neighborSheep.Y)

        average_x /= neighborCount
        average_y /= neighborCount

        # TO-DO: Expose Cohesion_weight as one of turning parameters

        self.velocityX -= (average_x / self.cohesionW)
        self.velocityY -= (average_y / self.cohesionW)

        return

    def alignment(self,neighborList):
        neighborCount = len(neighborList)
        if neighborCount < 1:
            return

        average_x = 0
        average_y = 0

        for sheep in neighborList:
            average_x += sheep.velocityX
            average_y += sheep.velocityY

        average_x /= neighborCount
        average_y /= neighborCount

        # set our velocity towards the others
        self.velocityX += (average_x / self.alignmentW)
        self.velocityY += (average_x / self.alignmentW)

        return

    def separation(self,neighborList,minDistance):

        #Move away from neighbors to avoid crowding
        neighborCount = len(neighborList)
        if neighborCount < 1:
            return

        distance_x = 0
        distance_y = 0
        num_close = 0

        for neighbor in neighborList:
            distance = self.distanceTo(neighbor)

            if distance < minDistance:
                num_close += 1
                xdiff = (self.X - neighbor.X)
                ydiff = (self.Y - neighbor.Y)

                if xdiff >= 0:
                    xdiff = sqrt(minDistance) - xdiff
                elif xdiff < 0:
                    xdiff = -sqrt(minDistance) - xdiff

                if ydiff >= 0:
                    ydiff  = sqrt(minDistance) - ydiff
                elif ydiff < 0:
                    ydiff = -sqrt(minDistance) - ydiff

                distance_x += xdiff
                distance_y += ydiff

        if num_close == 0:
            return

        self.velocityX -= distance_x / self.separationW
        self.velocityY -= distance_y / self.separationW

        return

    def flee(self,closeDogsList):
        for dog in closeDogsList:
            self.velocityX += (self.X-dog.X)/self.dog_avoidanceW
            self.velocityY += (self.Y - dog.Y) / self.dog_avoidanceW
        return

    def validateParams(self,IdleMode = False,isSheep=True):
        edgeSpeedModifier = 1
        nonCollidingModifier = 1
        if(IdleMode):
            edgeSpeedModifier = 2
            nonCollidingModifier = 1
        if self.X < 0 and self.velocityX < 0:
            self.velocityX = -edgeSpeedModifier*self.velocityX
            self.velocityY = nonCollidingModifier*self.velocityY
        if self.X > screen_Width and self.velocityX > 0:
            self.velocityX = -edgeSpeedModifier*self.velocityX
            self.velocityY = nonCollidingModifier*self.velocityY
        if self.Y < 0 and self.velocityY < 0:
            self.velocityY = -edgeSpeedModifier*self.velocityY
            self.velocityX = nonCollidingModifier*self.velocityX
        if self.Y > screen_Height and self.velocityY > 0:
            self.velocityY = -edgeSpeedModifier*self.velocityY
            self.velocityX = nonCollidingModifier*self.velocityX

        #validate within the maximum speed limit and scale down if needed
        tempVelocity = sqrt(self.velocityX*self.velocityX+self.velocityY*self.velocityY);
        if tempVelocity>self.MaxVelocity:
            self.velocityX = self.velocityX/tempVelocity*self.MaxVelocity;
            self.velocityY = self.velocityY/tempVelocity*self.MaxVelocity;


        return

    def UpdateLocation(self):
        self.X = self.X + self.velocityX
        self.Y = self.Y + self.velocityY
        
        return
class SingleDog(SingleSheep):
    pass

