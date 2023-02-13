


class Vertex():
    def __init__(self,id,edges,degree):
        self.id = id
        self.edges = edges
        self.degree = degree



class Edge():
    def __init__(self,id,start,end):
        self.id = id
        self.start = start
        self.end = end

    def print(self):
        print("Edge "+str(self.id)+", from V"+str(self.start.id)+" to V"+str(self.end.id))



class Area(Vertex):
    def __init__(self,id,edges,degree,type,center):
        super().__init__(id,edges,degree)
        self.type = type



class Connector(Edge):
    def __init__(self,id,start,end,type,squares):
        super().__init__(id,start,end)
        self.type = type

        if type == "Rock":
            self.open = True
            self.square = squares[0]
        elif type == "Door":
            self.open = False
            self.frontSquare = squares[0]
            self.backSquare = squares[1]

    def flip(self):
        self.open = not self.open



class Graph():
    def __init__(self,vertices,edges,nbVertices,nbEdges):
        self.vertices = vertices
        self.edges = edges
        self.nbVertices = nbVertices
        self.nbEdges = nbEdges

    def print(self):
        print(self.nbVertices,"Vertices",self.nbEdges,"Edges")
        for edge in self.edges:
            edge.print()
