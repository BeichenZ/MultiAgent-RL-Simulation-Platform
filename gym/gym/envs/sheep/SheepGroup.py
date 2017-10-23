import numpy

class SheepGroup():
    NEIGHBOR_RADIUS = 50
    def __init__(self,sheepCount):
        self.sheepCount = sheepCount
        self.SheepList = []
        for i in range(sheepCount):
            self.SheepList.append(SingleSheep())
    def updateLocations(self):
        for thisSheep in self.SheepList:
            sheepNeighbors = []
            for otherSheep in self.SheepList:
                if otherSheep == thisSheep:
                    continue #skip for itself
                #TO-DO add the DistanceTo function
                distance = thisSheep.DistanceTo(otherSheep,False)
                if distance < self.NEIGHBOR_RADIUS:
                    sheepNeighbors.append(otherSheep)

            #TO-DO make boids to do random stuff if they do not move

            #TO-DO cohesion function
            thisSheep.cohesion(sheepNeighbors)
            #TO-DO alignment function
            thisSheep.alignment(sheepNeighbors)
            # TO-DO separation function
            thisSheep.separation(sheepNeighbors)
            # TO-DO update funtion
            thisSheep.update(False)

        return


class SingleSheep():
    X_def = numpy.random.random_integers(0,600);
    Y_def = numpy.random.random_integers(0,600);
    cohesionW_def = 10;
    alignmentW_def = 4;
    separationW_def = 0.5;
    ObstacleAvoidW_def = 1;
    goalW_def = 6;
    fieldofView_def = 6;
    MaxVelocity_def = 60;
    #Place-holder for later Image
    sheepImage_def = "/resource/sheep1.png"


    def __init__(self,X=X_def,Y=Y_def,
                 cohesionW=cohesionW_def,alignmentW = alignmentW_def,separationW = separationW_def,
                 MaxVelocity = MaxVelocity_def,sheepImage = sheepImage_def):
        self.X = X;
        self.Y = Y;

        self.cohesionW = cohesionW;
        self.alignmentW = alignmentW;
        self.separationW = separationW;
        self.MaxVelocity = MaxVelocity;
        self.sheepImagePath = sheepImage;






