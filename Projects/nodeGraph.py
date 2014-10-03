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

    def setStart(self, node):
        if isinstance(node, Node):
            self.start = node
            node.links.append(self)

    def setEnd(self, node):
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
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.links = []

    def setXY(self, x, y):
        self.x = x
        self.y = y

    def getLinks(self):
        return self.links


class NodeGrapher(object):
    def __init__(self, V=[], E=[]):
        self.V = self.getValidElementsList(V, Node)
        self.E = self.getValidElementsList(E, Link)
        self.selectedLinkStart = None
        self.selectedLinkEnd = None
        self.initGUI()

    def show(self):
        tkinter.mainloop()

    def getValidElementsList(self, elementList, className):
        if isinstance(elementList, list):
            tempList = []
            for i in elementList:
                if isinstance(i, className):
                    tempList.append(i)
            return tempList

    def initGUI(self):
        self.main = tkinter.Tk()
        self.main.title("Node Grapher")
        self.main.bind("<Button-1>", self.clicked)
        self.main.bind("<B1-Motion>", self.dragging)
        self.main.bind("<ButtonRelease-1>", self.released)

        #For adding nodes
        self.main.bind("<Control-Button-1>", self.ctrlClicked)

        #add a canvas
        self.canvas = tkinter.Canvas(self.main, width=680, height=500)
        #For rightclicking a node
        self.canvas.tag_bind("node", "<Button-3>", self.nodeRightClicked)

        self.canvas.pack()

        #Draw nodes
        self.render()

        #Show the window (enter mainloop)
        #self.show()

    def ctrlClicked(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        node = Node(x, y)
        self.V.append(node)
        self.drawNode(node)

    def nodeRightClicked(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)

        node = self.getClosestNode(x, y)

        if not (self.selectedLinkStart):
            self.selectedLinkStart = node
            self.canvas.itemconfig(node.p, tags=("node", "selected"),
                                   fill="red")
        elif self.selectedLinkStart and (node != self.selectedLinkStart):
            self.selectedLinkEnd = node
            self._connectNodes()

    def _connectNodes(self):
        if isinstance(self.selectedLinkStart, Node) and \
                isinstance(self.selectedLinkEnd, Node):
            link = Link(self.selectedLinkStart, self.selectedLinkEnd)
            self.selectedLinkStart.links.append(link)
            self.selectedLinkEnd.links.append(link)
            self.E.append(link)
            self.drawLink(link)
            self.sendLinksBack()
            self.canvas.itemconfig(self.selectedLinkStart.p, tags="node",
                                   fill="cyan")
        self.selectedLinkStart = None
        self.selectedLinkEnd = None

    def clicked(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        self.selectedNode = self.getClosestNode(x, y)

    def dragging(self, event):
        node = self.selectedNode
        if node:
            node.setXY(event.x, event.y)
            self.canvas.coords(node.p, int(node.x-5), int(node.y-5),
                               int(node.x+5), int(node.y+5))
            for link in node.getLinks():
                s = link.getStartNode()
                e = link.getEndNode()
                self.canvas.coords(link.l, s.x, s.y, e.x, e.y)

    def released(self, event):
        self.selectedNode = None

    def render(self):
        self.canvas.create_rectangle(0, 0, 680, 500, fill="green")

        for point in self.V:
            self.drawNode(point)
        for line in self.E:
            self.drawLink(line)
        self.sendLinksBack()

    def drawNode(self, node):
        points = [node.x-5, node.y-5, node.x+5, node.y+5]
        node.p = self.canvas.create_oval(points, fill="cyan", tags="node")

    def drawLink(self, link):
        start = link.getStartNode()
        end = link.getEndNode()
        points = [start.x, start.y, end.x, end.y]
        link.l = self.canvas.create_line(points, tags="link")

    def sendLinksBack(self):
        self.canvas.tag_lower("link", "node")

    def getClosestNode(self, x, y):
        #Initial distance and value
        dist = math.sqrt((self.V[0].x-x)**2+(self.V[0].y-y)**2)
        closestNode = self.V[0]

        #Iterate over nodes and find closest
        for node in self.V:
            nodeDist = math.sqrt((node.x-x)**2+(node.y-y)**2)
            if nodeDist <= dist:
                closestNode = node
                dist = nodeDist
        return closestNode


def main():
    nodes = []
    edges = []
    for x in range(0, 500, 50):
        nodes.append(Node(0.5*x+x % 100, x+25))

    c = 0
    while (c < len(nodes)-1):
        edges.append(Link(nodes[c], nodes[c+1]))
        if c == 3:
            edges.append(Link(nodes[c], nodes[c+2]))
        c += 1

    window = NodeGrapher(nodes, edges)
    window.show()

if __name__ == "__main__":
    main()
