import numpy

'''
2 Dogs for now. 
First dog controlled by arrow keys
Second dog controlled by [W,A,S,D] keys
'''

screen_Width = 0
screen_Height = 0

class DogGroup():
    def __init__(self,screenWidth,screenHeight):
        global screen_Width
        global screen_Height
        screen_Width=screenWidth
        screen_Height = screenHeight

        self.DogList = []
        self.DogList.append(SingleDog())
        self.DogList.append(SingleDog())


class SingleDog():
    def __init__(self,X=None,Y=None):
        global screen_Height
        global screen_Width
        self.X = numpy.random.randint(0, screen_Width) if X is None else X
        self.Y = numpy.random.randint(0, screen_Height) if Y is None else Y






