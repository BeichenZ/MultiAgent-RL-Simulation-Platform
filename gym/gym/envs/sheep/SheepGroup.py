import numpy
from math import sqrt

screen_Width = 0
screen_Height = 0

class SheepGroup():
    NEIGHBOR_RADIUS = 600
    
    def __init__(self,sheepCount,screenWidth,screenHeight):
        self.sheepCount = sheepCount
        self.SheepList = []
        global screen_Width
        global screen_Height
        screen_Width=screenWidth
        screen_Height = screenHeight
        for i in range(sheepCount):
            self.SheepList.append(SingleSheep())
    def updateLocations(self):
        for thisSheep in self.SheepList:
            sheepNeighbors = []
            for otherSheep in self.SheepList:
                if otherSheep == thisSheep:
                    continue #skip for itself
                distance = thisSheep.distanceTo(otherSheep)
                if distance < self.NEIGHBOR_RADIUS:
                    sheepNeighbors.append(otherSheep)

            #TO-DO make boids to do random stuff if they do not move

            #TO-DO cohesion function
            thisSheep.cohesion(sheepNeighbors)
            #TO-DO alignment function
            thisSheep.alignment(sheepNeighbors)
            # TO-DO separation function
            thisSheep.separation(sheepNeighbors,minDistance=5)
            # Validate location and velocityt adjusted in previous functions
            thisSheep.validateParams()
            # Update Next Location with by adding the new velocity calculated up to this line.
            thisSheep.validateAndUpdateLocation()

        return


class SingleSheep():
    cohesionW_def = 10;
    alignmentW_def = 4;
    separationW_def = 0.5;
    ObstacleAvoidW_def = 1;
    goalW_def = 6;
    fieldofView_def = 6;
    MaxVelocity_def = 6;
    #Place-holder for later Image
    sheepImage_def = "/resource/sheep1.png"


    def __init__(self,X=None,Y=None,
                 cohesionW=cohesionW_def,alignmentW = alignmentW_def,separationW = separationW_def,
                 MaxVelocity = MaxVelocity_def,sheepImage = sheepImage_def):
        global screen_Height
        global screen_Width
        self.X = numpy.random.randint(0, screen_Width) if X is None else X
        self.Y = numpy.random.randint(0, screen_Height) if Y is None else Y

        self.cohesionW = cohesionW;
        self.alignmentW = alignmentW;
        self.separationW = separationW;
        self.MaxVelocity = MaxVelocity;
        self.sheepImagePath = sheepImage;
        self.velocityX = numpy.random.random_integers(0,1000)/100;
        self.velocityY = numpy.random.random_integers(0,1000)/100;

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

    def validateParams(self):
        if self.X < 0 and self.velocityX < 0:
            self.velocityX = -self.velocityX
        if self.X > screen_Width and self.velocityX > 0:
            self.velocityX = -self.velocityX
        if self.Y < 0 and self.velocityY < 0:
            self.velocityY = -self.velocityY
        if self.Y > screen_Height and self.velocityY > 0:
            self.velocityY = -self.velocityY
        return

    def validateAndUpdateLocation(self):
        self.validateParams()
        self.X = self.X + self.velocityX
        self.Y = self.Y + self.velocityY



