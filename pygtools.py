import pygame as pyg
import numpy as np
from time import sleep # type: ignore

class renderer(object):
    def __init__(self, rotations : tuple, offset : tuple, pixelsize : int, pixelmap : tuple, surface, screen : tuple, size = 50, show_edges = False, show_vertesies = False):
        self.rx = rotations[0]
        self.ry = rotations[1]
        self.rz = rotations[2]
        
        self.size = size

        self.ofs = [
            offset[0],
            offset[1],
            offset[2]
        ]

        self.screen = screen
        self.pxs = pixelsize
        self.pxm = pixelmap
        
        self.show_edges = show_edges
        self.show_vertesies = show_vertesies

        self.canvas = surface
        
        self.cube = [
            [
                [size,size,size],[size,-size,size],[-size,-size,size],[-size,size,size],[size,size,-size],[size,-size,-size],[-size,-size,-size],[-size,size,-size]
            ],
            [
                [0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],[0,4],[1,5],[2,6],[3,7]
            ],
            [
                [0,1,2,3],[4,5,6,7],[0,4,5,1],[1,5,6,2],[2,6,7,3],[3,7,4,0]
            ]
            ]

    def render(self):
        #rotation and offseting
        rmx = (
        [1,0,0],
        [0, np.cos(np.radians(self.rx)), 0 - np.sin(np.radians(self.rx))],
        [0, np.sin(np.radians(self.rx)), np.cos(np.radians(self.rx))]
        )
        rmy = (
        [np.cos(np.radians(self.ry)), 0, 0 - np.sin(np.radians(self.ry)) ],
        [0, 1, 0],
        [np.sin(np.radians(self.ry)), 0, np.cos(np.radians(self.ry))]
        )
        rmz = (
        [np.cos(np.radians(self.rz)), np.sin(np.radians(self.rz)), 0],
        [0 - np.sin(np.radians(self.rz)), np.cos(np.radians(self.rz)), 0],
        [0, 0, 1]
        )
        c1 = 0
        for i in self.cube[0]:
            self.cube[0][c1] = np.dot(rmx, self.cube[0][c1])
            self.cube[0][c1] = np.dot(rmy, self.cube[0][c1])
            self.cube[0][c1] = np.dot(rmz, self.cube[0][c1])
            c1 += 1
        c1 = 0
        for i in self.cube[0]:
            c2 = 0
            for i in self.cube[0][c1]:
                self.cube[0][c1][c2] += self.ofs[c2]
                c2 += 1
            c1 += 1
        projected = []
        flength = (self.screen[0]/2)*np.tan(np.radians(60/2))
        c1 = 0
        for i in self.cube[0]:
            projected.append([((self.cube[0][c1][0] * flength) / (self.cube[0][c1][2] + flength)) + self.screen[0]/2, ((self.cube[0][c1][1] * flength) / (self.cube[0][c1][2] + flength)) + self.screen[1]/2])
            c1 += 1
        
        if self.show_vertesies:
            c1 = 0
            for i in projected:
                pyg.draw.circle(self.canvas, (0,0,0), (projected[c1][0], projected[c1][1]), 1)
                c1 += 1

        if self.show_edges:
            c1 = 0
            for i in self.cube[1]:
                pyg.draw.line(self.canvas, (0,0,0), (projected[self.cube[1][c1][0]][0], projected[self.cube[1][c1][0]][1]), (projected[self.cube[1][c1][1]][0], projected[self.cube[1][c1][1]][1]), 5)
                c1 += 1
        """
        1) get the avg of z in the respected vertex point
        2) then get the colors of the respected faces and gather them in a list
        3) render the face colors using pyg.draw.polygon() funciton in a order where the avraged z is going from the smalles to the biggest aka from a point where its most away from
        the camera to the nearest.

        attempts = 7
        """
        
        #V1
        
        c1 = 0
        face_depth = []
        for face in self.cube[2]:
            avg_z = sum(self.cube[0][i][2] for i in face) / len(face)
            face_depth.append([avg_z, face, c1])
            c1 += 1
        
        face_depth.sort(reverse=True)
        
        for dept, face, facenum in face_depth:
            corners = [projected[i] for i in face]
            pyg.draw.polygon(canvas, self.pxm[facenum], corners)
        


if __name__ == "__main__":
    mainloop = True
    scX = 1000
    scY = 800
    pyg.display.init()
    mon = pyg.display.Info()
    fulls = False
    canvas = pyg.display.set_mode((scX, scY), pyg.RESIZABLE)
    pyg.display.set_caption('Testing da renderer')
    deg = 180
    while mainloop:
        #event handler
        for event in pyg.event.get():
            if event.type == pyg.QUIT: 
                pyg.display.quit()
                mainloop = False
            if event.type == pyg.KEYDOWN and event.key == pyg.K_F11:
                if not fulls:
                    scXr, scYr = canvas.get_size()
                    canvas = pyg.display.set_mode((mon.current_w, mon.current_h), pyg.RESIZABLE)
                    pyg.display.toggle_fullscreen()
                    fulls = True
                else:
                    canvas = pyg.display.set_mode((scXr, scYr), pyg.RESIZABLE)
                    fulls = False

        canvas.fill((255, 255, 255))
        scXre, scYre = canvas.get_size()
        renderer((0,-deg,0), (0,-100,0), 16, ((255,0,0), (0,255,0), (255,255,0), (0,0,255), (255,0,255), (0,255,255)), canvas,(scXre, scYre), 70, True).render()
        deg += 1
        if deg == 360:
            deg = 0
        pyg.display.flip()
        sleep(1/60)
    quit()