

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
((23,35),[(12,5),(13,5)]),((35,34),[(12,3),(13,3)]),((34,48),[(12,1),(13,1)]),
#south vertical hallway
((26,36),[(12,13),(13,13)]),((36,37),[(12,15),(13,15)]),((37,57),[(12,17),(13,17)]),
#west horizontal hallway
((72,38),[(1,9)]),((38,39),[(4,9)]),((39,40),[(6,9)]),((40,32),[(8,9)]),
#east horizontal hallway
((29,41),[(17,9)]),((41,42),[(19,9)]),((42,43),[(21,9)]),((43,65),[(24,9)]),
#north horizontal hallway
((44,45),[(4,0)]),((45,46),[(6,0)]),((46,47),[(9,0)]),((47,48),[(11,0)]),((48,49),[(14,0)]),((49,50),[(16,0)]),((50,51),[(19,0)]),((51,52),[(21,0)]),
#south horizontal hallway
((53,54),[(4,18)]),((54,55),[(6,18)]),((55,56),[(9,18)]),((56,57),[(11,18)]),((57,58),[(14,18)]),((58,59),[(17,18)]),((59,60),[(19,18)]),((60,61),[(21,18)]),
#east vertical hallway
((62,63),[(25,4)]),((63,64),[(25,6)]),((64,65),[(25,8)]),((65,66),[(25,10)]),((66,67),[(25,12)]),((67,68),[(25,14)]),
#west vertical hallway
((69,70),[(0,4)]),((70,71),[(0,6)]),((71,72),[(0,8)]),((72,73),[(0,10)]),((73,74),[(0,12)]),((74,75),[(0,14)]),
#inner corners
((31,22),[(9,6)]),((24,28),[(16,6)]),((30,27),[(16,12)]),((25,33),[(9,12)]),
#outer corners
((69,44),[(0,0)]),((52,62),[(25,0)]),((68,61),[(25,18)]),((53,75),[(0,18)]),
]

doorConnectors = [
#bottomleft intern doors
((11,12),[(2,13),(2,14)]),((12,15),[(4,16),(5,16)]),#((15,16),[(,),(,)]),((11,15),[(,),(,)]),((13,15),[(,),(,)]),((14,15),[(,),(,)]),((14,13),[(,),(,)]),((13,11),[(,),(,)]),
#bottomleft extern doors
#((,),[]),((,),[]),((,),[]),((,),[]),((,),[]),
#bottomright intern doors
#((,),[]),((,),[]),((,),[]),((,),[]),((,),[]),
#bottomright extern doors
#((,),[]),((,),[]),((,),[]),((,),[]),((,),[]),
#topright intern doors
#((,),[]),((,),[]),((,),[]),((,),[]),((,),[]),
#topright extern doors
#((,),[]),((,),[]),((,),[]),((,),[]),((,),[]),
#topleft intern doors
#((,),[]),((,),[]),((,),[]),((,),[]),((,),[]),
#topleft extern doors
#((,),[]),((,),[]),((,),[]),((,),[]),((,),[]),
]
