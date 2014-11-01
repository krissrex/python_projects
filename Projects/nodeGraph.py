# -*- coding: utf-8 -*-
"""
Created on Wed Aug 27 22:23:08 2014

@author: kristian
"""

import tkinter
from sys import argv


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


class Node(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.links = []


class NodeGrapher(object):
    def __init__(self, V=[], E=[]):
        self.V = self.getValidElementsList(V, Node)
        self.E = self.getValidElementsList(E, Link)
        self.selectedLinkStart = None
        self.selectedLinkEnd = None
        self.selectedNode = None
        self._initGUI()

    def show(self):
        tkinter.mainloop()

    def getValidElementsList(self, elementList, className):
        return [element for element in elementList if isinstance(element, className)]

    def _initGUI(self):
        self.main = tkinter.Tk()
        self.main.title("Node Grapher")
        self.main.bind("<Button-1>", self._clicked)
        self.main.bind("<B1-Motion>", self._dragging)
        self.main.bind("<ButtonRelease-1>", self._released)
        self.main.bind("<Delete>", self._delete_all)

        # For adding nodes
        self.main.bind("<Control-Button-1>", self._ctrlClicked)

        # Add a canvas to draw points and lines
        self.canvas = tkinter.Canvas(self.main, width=680, height=500)
        # For rightclicking a node
        self.canvas.tag_bind("node", "<Button-3>", self._nodeRightClicked)
        self.canvas.tag_bind("node", "<Control-Button-3>", self._nodeCtrlRightClicked)
        self.canvas.pack()

        # Draw nodes
        self._render()

    def _ctrlClicked(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        node = Node(x, y)
        self.V.append(node)
        self._drawNode(node)

    def _nodeRightClicked(self, event):
        x, y = self._canvas_coords(event)
        node = self._getClosestNode(x, y)

        # Select the node and color its point, if one has not been selected already
        if not self.selectedLinkStart:
            self.selectedLinkStart = node
            self.canvas.itemconfig(node.p, tags=("node", "selected"), fill="red")
        else:
            # If the same node was selected twice, reset it.
            # Otherwise, the node was the end node.
            if node == self.selectedLinkStart:
                self.canvas.itemconfig(self.selectedLinkStart.p, tags="node", fill="cyan")
                self.selectedLinkStart = None
            else:
                self.selectedLinkEnd = node
                self._connectNodes()

    def _nodeCtrlRightClicked(self, event):
        x, y = self._canvas_coords(event)
        node = self._getClosestNode(x, y)

        if not self.selectedLinkStart:
            self.selectedLinkStart = node
            self.canvas.itemconfig(node.p, tags=("node", "selected"), fill="red")
        else:
            # Use [:] to make a copy of the list, to avoid breaking iteration
            for link in self.selectedLinkStart.links[:]:
                if node == link.end or node == link.start:
                    try:
                        link.end.links.remove(link)
                    except Exception:
                        pass
                    try:
                        link.start.links.remove(link)
                    except Exception:
                        pass
                    try:
                        self.E.remove(link)
                    except Exception:
                        pass
                    self.canvas.delete(link.l)


                

    def _delete_all(self, event):
        """Delete all lines and links. If there are none, delete all nodes and points."""
        if self.E:
            self.E = []
            self.canvas.delete("link")
        elif self.V:
            self.V = []
            self.canvas.delete("node")

    def _canvas_coords(self, event):
        return (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))

    def _connectNodes(self):
        """Link the nodes assigned as selected in the NodeGrapher and draw them."""
        if isinstance(self.selectedLinkStart, Node) \
                and isinstance(self.selectedLinkEnd, Node):
            # Create a Link with the two selected nodes
            link = Link(self.selectedLinkStart, self.selectedLinkEnd)
            self.selectedLinkStart.links.append(link)
            self.selectedLinkEnd.links.append(link)
            self.E.append(link)
            self._drawLink(link)
            self._sendLinksBack()
            self.canvas.itemconfig(self.selectedLinkStart.p, tags="node",
                                   fill="cyan")
        # Clear the selection.
        self.selectedLinkStart = None
        self.selectedLinkEnd = None

    def _clicked(self, event):
        x, y = self._canvas_coords(event)
        self.selectedNode = self._getClosestNode(x, y)

    def _dragging(self, event):
        node = self.selectedNode
        if node:
            node.x = event.x
            node.y = event.y
            # update the drawn point with id in node.p and radius 5
            self.canvas.coords(node.p, int(node.x-5), int(node.y-5),
                               int(node.x+5), int(node.y+5))
            for link in node.links:
                s = link.start
                e = link.end
                # update the drawn line with id in link.l
                # and start in s.x, s.y and end e.x, e.y
                self.canvas.coords(link.l, s.x, s.y, e.x, e.y)

    def _released(self, event):
        self.selectedNode = None

    def _render(self):
        self.canvas.create_rectangle(0, 0, 680, 500, fill="green")

        for point in self.V:
            self._drawNode(point)
        for line in self.E:
            self._drawLink(line)
        self._sendLinksBack()

    def _drawNode(self, node):
        points = [node.x-5, node.y-5, node.x+5, node.y+5]
        node.p = self.canvas.create_oval(points, fill="cyan", tags="node")

    def _drawLink(self, link):
        start = link.start
        end = link.end
        points = [start.x, start.y, end.x, end.y]
        # Create a line in the canvas and assign its id to link.l
        link.l = self.canvas.create_line(points, tags="link")

    def _sendLinksBack(self):
        """Sends all lines in the canvas innwards so they are behind the points."""
        # Lower all elements with tag 'link' below those with tag 'node'
        try:
            self.canvas.tag_lower("link", "node")
        except:
            print("Failed to send back lines. Perhaps there are none?")

    def _getClosestNode(self, x, y):
        if not self.V:
            # No nodes in the list of vertices.
            return

        def distance_squared(node):
            # No need to find the square root, as it is just comparison.
            return (node.x - x)**2 + (node.y - y)**2

        # Initial distance and value
        dist = distance_squared(self.V[0])
        closest_node = self.V[0]

        #Iterate over nodes and find closest
        for node in self.V:
            current_dist = distance_squared(node)
            if current_dist <= dist:
                closest_node = node
                dist = current_dist
        return closest_node


def main(args):

    nodes = []
    edges = []
    if "debug" in args:
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
    main(argv)
