import numpy as n
class Obj:
    def __init__(self,posx,posy,wbox,hbox, mycolor):
        self.position = (posx, posy)
        self.dims = (wbox, hbox)
        
        self.sectionAy = (posx, posy - hbox/2) #left upper corner is (0,0))
        self.sectionBx = (posx + wbox/2, posy)
        self.sectionCy = (posx, posy + hbox/2)
        self.sectionDx = (posx - wbox/2, posy)
        ## self.absorbance
        
        self.sections = [self.sectionAy,self.sectionBx,self.sectionCy,self.sectionDx]
        self.filler = mycolor



class Source:
    def __init__(self, initial_x, initial_Y,dims, intensity):
        self.x = initial_x
        self.y = initial_Y
        self.dims = dims
        self.filler = intensity
        self.photon_vectors = []
        self.classified_vectors = []
        
        ## initiating here will allow us to save the data and use it throughout the object
    def generate_vectors(self, precision):
        a = n.linspace(start = 0, stop = (2*3.14), num = precision)
        all_rations = n.array([(n.tan(elements), elements) for elements in a])
        self.photon_vectors = all_rations
        ## reverse order du to the strange nature of computer cartesian system
        
        self.classified_vectors = [[elements[0] for elements in self.photon_vectors if elements[1] >= 0 and elements[1] <= 3.14/2],
[elements[0] for elements in self.photon_vectors if elements[1] >= 3.14/2 and elements[1] <= 3.14],
[elements[0] for elements in self.photon_vectors if elements[1] >= 3.14 and elements[1] <= 3.14/2 + 3.14],
[elements[0] for elements in self.photon_vectors if elements[1] >= 3.14/2 + 3.14 and elements[1] <= 3.14*2]]
