

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
nbHallways = 54

rooms = [
#big room
{"coordinates":(10,7,6,5),"color":(168,148,135)},
#topleft rooms
{"coordinates":(1,1,4,3),"color":(174,120,87)},
{"coordinates":(5,1,4,3),"color":(166,82,74)},
{"coordinates":(1,4,4,5),"color":(118,118,123)},
{"coordinates":(5,4,4,5),"color":(162,189,83)},
{"coordinates":(9,1,3,5),"color":(149,188,192)},
#topright rooms
{"coordinates":(14,1,3,5),"color":(166,61,40)},
{"coordinates":(17,1,4,4),"color":(179,185,203)},
{"coordinates":(21,1,4,4),"color":(210,172,107)},
{"coordinates":(17,5,4,4),"color":(194,143,64)},
{"coordinates":(21,5,4,4),"color":(205,210,109)},
#bottomleft rooms
{"coordinates":(1,10,4,4),"color":(225,210,127)},
{"coordinates":(1,14,4,4),"color":(160,159,191)},
{"coordinates":(5,10,2,3),"color":(192,222,232)},
{"coordinates":(7,10,2,3),"color":(124,158,150)},
{"coordinates":(5,13,4,5),"color":(188,116,103)},
{"coordinates":(9,13,3,5),"color":(180,158,102)},
#bottomright rooms
{"coordinates":(17,10,4,4),"color":(168,172,209)},
{"coordinates":(21,10,4,4),"color":(210,189,100)},
{"coordinates":(18,14,3,4),"color":(185,141,96)},
{"coordinates":(21,14,4,4),"color":(124,184,105)},
{"coordinates":(14,13,4,5) ,"color":(172,126,118)},
#must be last to be drawn properly
]

hallways = [
#north central hallway
(10.5,6.5),(13,6.5),(15.5,6.5),
#south central hallway
(10.5,12.5),(13,12.5),(15.5,12.5),
#east central hallway
(16.5,7.5),(16.5,9.5),(16.5,11.5),
#west central hallway
(9.5,7.5),(9.5,9.5),(9.5,11.5),
#north vertical hallway
(13,2.5),(13,4.5),
#south vertical hallway
(13,14.5),(13,16.5),
#west horizontal hallway
(3,9.5),(5.5,9.5),(7.5,9.5),
#east horizontal hallway
(18.5,9.5),(20.5,9.5),(23,9.5),
#north horizontal hallway
(3,0.5),(5.5,0.5),(8,0.5),(10.5,0.5),(13,0.5),(15.5,0.5),(18,0.5),(20.5,0.5),(23,0.5),
#south horizontal hallway
(3,18.5),(5.5,18.5),(8,18.5),(10.5,18.5),(13,18.5),(16,18.5),(18.5 ,18.5),(20.5,18.5),(23,18.5),
#east vertical hallway
(25.5,3),(25.5,5.5),(25.5,7.5),(25.5,9.5),(25.5,11.5),(25.5,13.5),(25.5,16),
#west vertical hallway
(0.5,2.5),(0.5,5.5),(0.5,7.5),(0.5,9.5),(0.5,11.5),(0.5,13.5),(0.5,16),
]

rockConnectors = [
#north central hallway
((22,23),[(11, 6)]),((23,24),[(14,6)]),
#south central hallway
((25,26),[(11,12)]),((26,27),[(14,12)]),
#east central hallway
((28,29),[(16,8)]),((29,30),[(16,10)]),
#west central hallway
((31,32),[(9,8)]),((32,33),[(9,10)]),
#north vertical hallway
((23,35),[(12,5),(13,5)]),((34,35),[(12,3),(13,3)]),((35,48),[(12,1),(13,1)]),
#south vertical hallway
((26,36),[(12,13),(13,13)]),((36,37),[(12,15),(13,15)]),((37,57),[(12,17),(13,17)]),
#west horizontal hallway
#((,),[]),((,),[]),((,),[]),
#east horizontal hallway
#((,),[]),((,),[]),((,),[]),
#north horizontal hallway
#((,),[]),((,),[]),((,),[]),
#south horizontal hallway
#((,),[]),((,),[]),((,),[]),
#east vertical hallway
#((,),[]),((,),[]),((,),[]),
#west vertical hallway
#((,),[]),((,),[]),((,),[]),
]

doorConnectors = [

]
