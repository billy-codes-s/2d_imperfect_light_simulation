from p5 import *
import numpy as n
import lights_lib as lb

global frameW, frameH, primary_light, secondary_diffusion
frameW, frameH = 1000,800
global world


def setup():
    global primary_light, world
    primary_light = lb.Source(100, 100, 100, 254)
    primary_light.generate_vectors(100)
    size(frameW,frameH)
    world = world_creator()
    element_generator(world)
        
def draw():
    background(100)
    contact = light_object_association(primary_light.classified_vectors,world,mouse_x,mouse_y)
    begin_shape()
    first_point = contact[0]

    special_fill = 0
    for elements in contact:
        vertex(elements[1], elements[0])
    fill(255)
    end_shape()


    keep = 0
    for elements in contact:
        fill(230,0, special_fill)
        special_fill += 5
        text(str(keep), elements[1], elements[0])
        keep += 1
        ellipse(elements[1], elements[0],5,5)

    element_generator(world)
    fill(0,255,0)
    ellipse(mouse_x, mouse_y, 50, 50)

def world_creator():
    first_rect = lb.Obj(500,500,100,140,0)
    second_rect = lb.Obj(700,700, 80, 70, 0)
    third_rect = lb.Obj(200,300, 100, 124, 0)
    fifth_rect = lb.Obj(700, 200, 100, 150,0)
    ## walls
    wall_A = lb.Obj(frameW/2, 0, frameW, 20, 0)
    wall_B = lb.Obj(frameW, frameH/2, 20, frameH, 0)
    wall_C = lb.Obj(frameW/2, frameH, frameW, 20, 0)
    wall_D = lb.Obj(0, frameH/2, 20, frameH, 0)
    return [first_rect,second_rect,third_rect,fifth_rect, wall_A,wall_B,wall_C, wall_D]

def element_generator(list_of_rects):
    for elements in list_of_rects:
        stroke(elements.filler)
        fill(elements.filler)
        rect_mode(CENTER)
        rect(elements.position[0], elements.position[1], elements.dims[0], elements.dims[1])



## axiom, it is a closed system that light most certainly will hit an element, and there are no supperposition of objs...
def light_object_association(ordered_vectors, list_of_pe, x, y):
    ## quadrant3
    section_3_finalists = []
    points_of_contact = []
    for objects in list_of_pe:
        if objects.sectionBx[0] >= x and objects.sectionCy[1] >= y:
            section_3_finalists.append(objects)
        else:
            pass

    for elements in ordered_vectors[3]:
        minima = None

        for objects in section_3_finalists:
            system_for_a = n.array([[1, elements], [1,0]])
            const_a = n.array([elements*x + y, objects.sectionAy[1]])

            try:    
                point_c = n.linalg.solve(system_for_a,const_a)
                if point_c[1] > objects.sectionBx[0] or  point_c[1] < objects.sectionDx[0]:
                    raise ValueError
            except:
                system_for_d = n.array([[1, elements], [0,1]])
                const_d = n.array([elements*x + y, objects.sectionDx[0]])

                try:
                    point_c = n.linalg.solve(system_for_d,const_d)
                    if point_c[0] < objects.sectionAy[1] or point_c[0] > objects.sectionCy[1]:
                        raise ValueError
                except:
                    continue

            if minima is None:
                minima = point_c
            else:
                if (minima[1] - x)**2 + (minima[0] -y)**2 >= (point_c[1] - x)**2 + (point_c[0] -y)**2:
                    minima = point_c
        
        if minima is not None: points_of_contact.append(minima)
    ## section 0
    section_0_finalists = []
    for objects in list_of_pe:
        if objects.sectionBx[0] >= x and objects.sectionAy[1] <= y:
            section_0_finalists.append(objects)

    for elements in ordered_vectors[0]:
        minima = None
        for objects in section_0_finalists:
            ## section_a
            system_for_c = n.array([[1, elements], [1,0]])
            const_c = n.array([elements*x + y, objects.sectionCy[1]])
            try:    
                point_c = n.linalg.solve(system_for_c,const_c)
                if point_c[1] > objects.sectionBx[0] or  point_c[1] < objects.sectionDx[0]:
                    raise ValueError

            except:
                system_for_d = n.array([[1, elements], [0,1]])
                const_d = n.array([elements*x + y, objects.sectionDx[0]])

                try:
                    point_c = n.linalg.solve(system_for_d,const_d)
                    if point_c[0] < objects.sectionAy[1] or point_c[0] > objects.sectionCy[1]:
                        raise ValueError
                except:
                    continue

            if minima is None:
                minima = point_c
            else:
                if (minima[1] - x)**2 + (minima[0] -y)**2 >= (point_c[1] - x)**2 + (point_c[0] -y)**2:
                    minima = point_c
        
        if minima is not None: points_of_contact.append(minima)
            

    ## section1
    section_1_finalists = []
    for objects in list_of_pe:
        if objects.sectionDx[0] <= x and objects.sectionAy[1] <= y:
            section_1_finalists.append(objects)

    for elements in ordered_vectors[1]:
        minima = None
        for objects in section_1_finalists:
            ## section_a
            system_for_c = n.array([[1, elements], [1,0]])
            const_c = n.array([elements*x + y, objects.sectionCy[1]])
            try:    
                point_c = n.linalg.solve(system_for_c,const_c)
                if point_c[1] > objects.sectionBx[0] or  point_c[1] < objects.sectionDx[0]:
                    raise ValueError

            except:
                ## section b
                system_for_b = n.array([[1, elements], [0,1]])
                const_b = n.array([elements*x + y, objects.sectionBx[0]])

                try:
                    point_c = n.linalg.solve(system_for_b,const_b)
                    if point_c[0] < objects.sectionAy[1] or point_c[0] > objects.sectionCy[1]:
                        raise ValueError
                except:
                    continue

            if minima is None:
                minima = point_c
            else:
                if (minima[1] - x)**2 + (minima[0] -y)**2 >= (point_c[1] - x)**2 + (point_c[0] -y)**2:
                    minima = point_c
        
        if minima is not None: points_of_contact.append(minima)

    ## quadrant2
    section_2_finalists = []
    for objects in list_of_pe:
        if objects.sectionDx[0] <= x and objects.sectionCy[1] >= y:
            section_2_finalists.append(objects)

    for elements in ordered_vectors[2]:
        minima = None

        for objects in section_2_finalists:
            ## section_a
            system_for_a = n.array([[1, elements], [1,0]])
            const_a = n.array([elements*x + y, objects.sectionAy[1]])
            try:    
                point_c = n.linalg.solve(system_for_a,const_a)
                if point_c[1] > objects.sectionBx[0] or  point_c[1] < objects.sectionDx[0]:
                    raise ValueError

            except:
                ## section b
                system_for_b = n.array([[1, elements], [0,1]])
                const_b = n.array([elements*x + y, objects.sectionBx[0]])

                try:
                    point_c = n.linalg.solve(system_for_b,const_b)
                    if point_c[0] < objects.sectionAy[1] or point_c[0] > objects.sectionCy[1]:
                        raise ValueError
                except:
                    continue

            if minima is None:
                minima = point_c
            else:
                if (minima[1] - x)**2 + (minima[0] -y)**2 >= (point_c[1] - x)**2 + (point_c[0] -y)**2:
                    minima = point_c
        
        if minima is not None: points_of_contact.append(minima)

    return(points_of_contact)
        
    pass



if __name__ == '__main__':
   run()