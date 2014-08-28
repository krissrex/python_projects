# -*- coding: utf-8 -*-
"""
Created on Wed Aug 27 22:23:08 2014

@author: kristian
"""

import tkinter
import math


class Link(object):
    def __init__(self, startNode, endNode):
        self.setStart(startNode)
        self.setEnd(endNode)
        self.l = None
        
    def setStart(self,node):
        if isinstance(node, Node):
            self.start = node
            node.links.append(self)
            
    def setEnd(self,node):
        if isinstance(node, Node):
            self.end = node
            node.links.append(self)
            
    def getStartNode(self):
        if isinstance(self.start, Node):
            return self.start
        else:
            return None
            
    def getEndNode(self):
        if isinstance(self.end, Node):
            return self.end
        else:
            return None
            
class Node(object):
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
        self.links  = []
    def setXY(self,x,y):
        self.x = x
        self.y = y
    def getLinks(self):
        return self.links
                

        
        
class NodeGrapher(object):
    def __init__(self,V=[],E=[]):
        self.V = self.getValidElementsList(V, Node)
        self.E = self.getValidElementsList(E, Link)
        self.initGUI()
    
    def show(self):
        tkinter.mainloop()
        
                        
    def getValidElementsList(self, elementList, className):
        if isinstance(elementList,list):
            tempList = []
            for i in elementList:
                if isinstance(i, className):
                    tempList.append(i)
            return tempList
            
    
    def initGUI(self):
        self.main = tkinter.Tk()
        self.main.title = "Node Grapher"
        self.main.bind("<Button-1>", self.clicked)
        self.main.bind("<B1-Motion>",self.dragging)        
        self.main.bind("<ButtonRelease-1>",self.released)
        
        self.canvas = tkinter.Canvas(self.main,width=680,height=500)
        self.canvas.pack()
        
        self.render()
        self.show()
    
    def clicked(self, event):
        x = event.x
        y = event.y
        dist = math.sqrt((self.V[0].x-x)**2+(self.V[0].y-y)**2)
        
        for node in self.V:
            nodeDist = math.sqrt((node.x-x)**2+(node.y-y)**2)
            if nodeDist <= dist:
                self.selectedNode = node
                dist = nodeDist

    def dragging(self, event):
        node = self.selectedNode
        if node:
            node.setXY(event.x, event.y)
            self.canvas.coords(node.p, int(node.x-5), int(node.y-5), int(node.x+5), int(node.y+5))
            for link in node.getLinks():
                s = link.getStartNode()
                e = link.getEndNode()
                self.canvas.coords(link.l, s.x, s.y, e.x, e.y)

            
    def released(self, event):
        self.selectedNode = None
    
    def render(self):
        self.canvas.create_rectangle(0,0,680, 500, fill="green")
        for line in self.E:
            start = line.getStartNode()
            end = line.getEndNode()
            points = [start.x, start.y, end.x, end.y]
            #x = end.x - start.x
            #y = end.y - start.y
            #startAngle = math.atan2(x, y)*(180/math.pi)
            
            l = self.canvas.create_line(points,tag="link")
            line.l = l
        for point in self.V:
            points = [point.x-5,point.y-5,point.x+5,point.y+5]
            p = self.canvas.create_oval(points, fill="cyan", tag="node")
            point.p = p
                    
                    
def main():
    nodes = []
    edges = []
    for x in range(0,500,50):
        nodes.append(Node(0.5*x+x%100,x+25))

    c = 0
    while (c < len(nodes)-1):
        edges.append(Link(nodes[c],nodes[c+1]))
        if c == 3:
            edges.append(Link(nodes[c],nodes[c+2]))
        c += 1
    
    window = NodeGrapher(nodes, edges)
    window.show()    
    
if __name__ == "__main__":
    main()
