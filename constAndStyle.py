

#style constants
butInCol = (215,174,129) #inside color of buttons
butOutCol = (170,115,90) #outside color of buttons
butPresInCol = (190,144,109) #inside color of pressed buttons
butPresOutCol = (170,115,90) #out color of pressed buttons


#game constants
mapLength = 26
mapWidth = 19
itemNames = ["Door","Rock"] #known items
nbRooms = 22

rooms = [
#big room
{"coordinates":(10,7,6,5),"color":(168,148,135),"center":(13,9.5)},
#topleft rooms
{"coordinates":(1,1,4,3),"color":(174,120,87),"center":(3,2.5)},
{"coordinates":(5,1,4,3),"color":(166,82,74),"center":(7,2.5)},
{"coordinates":(1,4,4,5),"color":(118,118,123),"center":(None,None)},
{"coordinates":(5,4,4,5),"color":(162,189,83),"center":(None,None)},
{"coordinates":(9,1,3,5),"color":(149,188,192),"center":(None,None)},
#bottomleft rooms
{"coordinates":(1,10,4,4),"color":(225,210,127),"center":(None,None)},
{"coordinates":(1,14,4,4),"color":(160,159,191),"center":(None,None)},
{"coordinates":(5,10,2,3),"color":(192,222,232),"center":(None,None)},
{"coordinates":(7,10,2,3),"color":(124,158,150),"center":(None,None)},
{"coordinates":(5,13,4,5),"color":(188,116,103),"center":(None,None)},
{"coordinates":(9,13,3,5),"color":(180,158,102),"center":(None,None)},
#topright rooms
{"coordinates":(14,1,3,5),"color":(166,61,40),"center":(None,None)},
{"coordinates":(17,1,4,4),"color":(179,185,203),"center":(None,None)},
{"coordinates":(21,1,4,4),"color":(210,172,107),"center":(None,None)},
{"coordinates":(17,5,4,4),"color":(194,143,64),"center":(None,None)},
{"coordinates":(21,5,4,4),"color":(205,210,109),"center":(None,None)},
#bottomright rooms
{"coordinates":(17,10,4,4),"color":(168,172,209),"center":(None,None)},
{"coordinates":(21,10,4,4),"color":(210,189,100),"center":(None,None)},
{"coordinates":(18,14,3,4),"color":(185,141,96),"center":(None,None)},
{"coordinates":(21,14,4,4),"color":(124,184,105),"center":(None,None)},
{"coordinates":(14,13,4,5) ,"color":(172,126,118),"center":(None,None)},
#must be last to be drawn properly
]
