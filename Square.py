


class Square():
    def __init__(self,x:int,y:int):
        self.x = x
        self.y = y

    @classmethod
    def fromDict(cls,dict):
        return cls(dict["x"],dict["y"])

    def equal(self,otherSquare):
        if self.x == otherSquare.x and self.y == otherSquare.y:
            return True
        else:
            return False

    def toJSON(self):
        return {"x":self.x,"y":self.y}
