__author__ = 'Abhi'

"""This paint program is based on the OSX yosemite theme and allows the user to draw using a variety of different brushes,
add images, uses stamps and filter their drawings. The program also allows you to have the ultimate mac experience even in a
windows environment."""

from pygame import *
from pygame import gfxdraw
from tkinter import *
from tkinter import filedialog as saveload
from random import *
from math import *
from Functions import *     #functions called from the program 
from Surfaces import *      #all of the images and surfaces used in the main
import os
import pygame.mixer

root = Tk() 
root.withdraw()

#---------------------------------SET SCREEN---------------------------------
init()
font.init()
clock = time.Clock()
setScreen(200,30)
screen = display.set_mode((1270,815))#, NOFRAME)#,FULLSCREEN) #1440 BY 815 is the mac resolution    #1270 by 815 is the school computer resolution
setup()
canvas = Rect(100,84,1080,650)
canvasDrawing = 'REBLIT'
bg_col = (255,255,255)
background = image.load('Resources/background_official.png').convert()  
screen.blit(background, (0,0))
draw.rect(screen, bg_col, canvas)   #draws canvas
#---------------------------------SET SCREEN---------------------------------

#---------------------------Fading Animation------------------------------
boot_screen = image.load('Resources/mac_os_x_yosemite.jpg')
setup_about = image.load('Resources/screenshot.png')
screen.blit(boot_screen, (0, 0))
main = False
mainy = 0
speed = 0
scroll = False
animation_counter = 0
#---------------------------Fading Animation------------------------------


#---------------------------------UNDO/REDO SETUP---------------------------------
undoList = [screen.subsurface(canvas).copy()]
redoList = []
copy = screen.subsurface(canvas).copy()
drawing = False
#---------------------------------UNDO/REDO SETUP---------------------------------

#-----------------------------------COLOUR WHEEL SETUP----------------------------------
collide = False
col_origin = (0,0)
colourWheel = 'INACTIVE'
Puck = 'SHOW'
done = True #variable used to make sure code in while loop isnt repeated (flag)
copyDrawing = screen.subsurface(canvas).copy()

primeCol = (0,0,0)
secCol = (0,0,255)
# By default, left mouse button colour is the drawing colour

drawCol = primeCol

primeHue = (0,0,0)  # When the program starts up, the default colour palette colour will be black
secHue = (0,0,255)  # The default secondary colour will be blue

primeID = (900, 237)     # Default position of main colour identifier
secID = (900, 237)       # Default position of secondary colour identifier

hue = 0
rectColSpectrum = Rect(1004, 460, 43, 228)
rectColPalette = Rect(1050, 493, 228, 228)

old_secCol = secCol
old_primeCol = primeCol

shadePaletteCollide = Surface((1270,815), SRCALPHA)
shadePaletteCollide.blit(col_images['shadePaletteCollide'], col_surfaces['shadePalette'])
#-----------------------------------COLOUR WHEEL SETUP----------------------------------

#--------------------------------STAMPS SETUP--------------------------------
sidePanel = False
sidePanelRect = Rect(1030,0,252,815)
stamp_origin = (0,0)
copyDrawing_stamps = screen.subsurface(Rect(1020,0,250,815)).copy()
copyDrawing_stamps2 = screen.subsurface(canvas).copy()
stamps_counter = 1270
reblit_SidePanel = True
#--------------------------------STAMPS SETUP--------------------------------

#--------------------------------POLYGON SETUP--------------------------------
polygon_origin = (0,0)
oldpolygon_origin = (0,0)
points = []
#--------------------------------POLYGON SETUP--------------------------------

#---------------------------------UPDATING VALUES---------------------------------
mx,my = 16,672  #random values assigned just to declare them before the while loop
cmx, cmy = mx-100,my-84
oldmx, oldmy = 0,0
mouseStat = 'DOWN'
lastClick = 'LEFT'
old_lastClick = lastClick
origin_lagoon = (0,0)
brush_size = 0
stamp_resize = 1
threshold = 100
stack = []
#---------------------------------UPDATING VALUES---------------------------------

#---------------------------------TEXT-------------------------------
startText = False
text = ""
typing = False
rectDrawn = False
WHpoints = (0,0)
ENDpoints = (0,0)
blity = 0
defaultFont = font.SysFont('Arial', 10)
text_origin = (0,0)
text_size = 14
size = (0,0)
#---------------------------------TEXT-------------------------------

#---------------------------------FILTERS-------------------------------
filter_origin = (0,0)
filters_counter = 1270
#---------------------------------FILTERS-------------------------------

#---------------------------------MUSIC-------------------------------
play = True
pause = False
counting = 0
pos = 0

playOveride = False
currentSong = Songs[0]
currentSong2 = Songs[1]
#---------------------------------MUSIC-------------------------------

#---------------------------------INITIALIZATION---------------------------------
lagoon(screen, canvas, background, drawCol)
colourPuck(screen, 1127, 78, lastClick, primeCol, secCol, puckLarge, puckSmall)

for group in groups:
    screen.blit(lagoonUP[group], blit_locations[group])

reblit_BgCanvasLagoon = True
reblit_Canvas_stamps = False
goAhead = False
copies = 0
highlight_stamp = True
copy_once = False
loadCustImg = False
CustImg = ''
AddImg_resize = 1
CustImg_blitOnce = False
copyDrawing_Edit = screen.subsurface(canvas).copy()
scroll = screen.subsurface(Rect(1043,753,184,15)).copy()
#---------------------------------INITIALIZATION---------------------------------

#---------------------------Fading Animation------------------------------
third_counter = 0

while third_counter != 2:
    for i in event.get():
        if i.type == QUIT:
            quit()
    screen.blit(boot_screen, (0, 0))
    third_counter += 1

while animation_counter < 40:
    for i in event.get():
        if i.type == QUIT:
            quit()

    setup_about.set_alpha(animation_counter % 255)  #image that should have the alpha value to blend in
    screen.blit(setup_about, (0, 0))     #this code fades and blends an image into another

    animation_counter += 0.5    #speed of fade out  # 7 = school computer   # 10 = mac
    time.wait(1)
    display.flip()
#---------------------------Fading Animation------------------------------

#---------------------------------BOTTOM BAR SETUP---------------------------------
WHpoints = (0,0)    # stores the default length and width of a shape
XYsurf = screen.subsurface(Rect(874,794,88,18)).copy()
WHsurf = screen.subsurface(Rect(874,794,100,20)).copy()
FPSsurf = screen.subsurface(Rect(21,795,33,13)).copy()
CanvasXYsurf = screen.subsurface(Rect(1175,794,89,14)).copy()
#---------------------------------BOTTOM BAR SETUP---------------------------------

while True:
    for e in event.get():
        if e.type == QUIT:
            quit()
        if e.type == MOUSEBUTTONDOWN:
            col_origin = e.pos
            polygon_origin = e.pos   #starting positions for shapes, text, etc.
            text_origin = e.pos
            move_origin = e.pos

            if e.button != 4 and e.button != 5: #this is because when the user scrolls pygame counts it as 'MOUSEBUTTONDOWN'
                stamp_origin = e.pos
                filter_origin = e.pos
                copyDrawing = screen.subsurface(canvas).copy()

            #finds the brush size based on the scroll
            if e.button == 4:
                if groups2['Stamps']:
                    if stamp_resize > 0.2:   stamp_resize -= 0.1
                elif loadCustImg:
                    if AddImg_resize > 0.2:   AddImg_resize -= 0.1
                elif Tools['Text']:
                    if text_size > 6:   text_size -= 1
                else:
                    if brush_size >= 1: brush_size -=1
            elif e.button == 5:
                if groups2['Stamps']:
                    if stamp_resize < 2.5:   stamp_resize += 0.1
                elif Tools['Text']:
                    if text_size < 72:   text_size += 1
                elif loadCustImg:
                    if AddImg_resize < 2.5:   AddImg_resize += 0.1
                else:
                    if brush_size < threshold: brush_size +=1

            if circleCollidepoint(93,798,mx,my,18) and len(undoList) > 1:
                recent = undoList.pop()
                time.delay(10)
                screen.blit(undoList[-1], canvas)
                redoList.append(recent)

            if circleCollidepoint(131,798,mx,my,16) and len(redoList) > 0:
                recent = redoList.pop()
                time.delay(10)
                screen.blit(recent, canvas)
                undoList.append(recent)

            if DockBasics['iTunes']:
                if circleCollidepoint(393,777,mx,my,7) and e.type == MOUSEBUTTONDOWN and pause:
                    pause = False
                    play = True
                    #pause = False
                    #screen.blit(image.load('Resources/iTunes/Play.png'), (300,760))
                elif circleCollidepoint(393,777,mx,my,7) and e.type == MOUSEBUTTONDOWN and play:
                    play = False
                    pause = True
                if Rect(346,771,21,15).collidepoint((mx,my)) and e.type == MOUSEBUTTONDOWN:
                    if pos > 0:
                        pos -= 1
                if Rect(422,771,21,15).collidepoint((mx,my)) and e.type == MOUSEBUTTONDOWN:
                    if pos < len(Songs)-1:
                        pos += 1

            if groups['Edit'] and group_surfaces['Edit'].collidepoint((move_origin)):
                OK = False
                copyDrawing_Edit = screen.subsurface(canvas).copy()

                    
        if e.type == MOUSEBUTTONUP:
            move_endpoint = e.pos
            if e.button != 4 and e.button != 5: #so that undo doesnt take a pic when the unfilled rectangle thickness is being adjusted
                if canvas.collidepoint((mx,my)) and colourWheel == 'INACTIVE':
                    copy = screen.subsurface(canvas).copy()
                if drawing:      #checks if any of the paint program tools are being used
                    drawing = False
                    redoList = []   #so that redo only works if it is clicked right after undo
                    undoList.append(copy)

        if Tools['Text']:
            if e.type == KEYDOWN:
                typing = True
                if e.key == K_BACKSPACE:
                    if len(text) > 0:
                        text = text[:-1]
                    if e.key == K_KP_ENTER or e.key == K_RETURN:
                        typing = False
                elif e.key == K_KP_ENTER or e.key == K_RETURN:
                    typing = False
                elif e.key < 256:
                    defaultFont = font.SysFont('Arial', text_size)
                    size = defaultFont.size(text) 
                    if 100 < (mx+size[0]) < 1180 and 84 < (my+size[1]) < 734:
                        text += e.unicode
            if e.type == MOUSEBUTTONDOWN and e.button != 4 and e.button != 5: # and mx == text_origin[0] and my == text_origin[1]:
                typing = False

            if typing == False:
                text = ""
            if typing:
                if canvas.collidepoint((mx,my)):
                    if 128 < (my+size[1]) < 770:
                        screen.blit(copyDrawing, (100,84))
                        makeText(screen, text, text_size, drawCol, (255,255,255), mx, my-text_size)

    mx, my = mouse.get_pos()
    cmx, cmy = mouse.get_pos()[0]-100,mouse.get_pos()[1]-84
    mb = mouse.get_pressed()

    if mb[0] == 1 or mb[2] == 1:  mouseStat = 'DOWN' 
    else:   mouseStat = 'UP' 
    if mb[0] == 1:  lastClick = 'LEFT'
    elif mb[2] == 1:    lastClick = 'RIGHT'

    drawCol = primeCol if lastClick == 'LEFT' else secCol

    if canvas.collidepoint((mx,my)) == False or mouseStat == 'UP' or Puck == 'HIDE' or group_surfaces2['Colour'].collidepoint((mx,my)): #or done2:# and mouseStat == 'UP':
        lagoon(screen, canvas, background, drawCol)
        reblit_BgCanvasLagoon = True
    else:
        reblit_BgCanvasLagoon = False

    for surf in group_surfaces:                                 #groups are the different icons on the lagoon
        if mouseStat == 'DOWN':                                 #checks if the mouse has been clicked
            if group_surfaces[surf].collidepoint((mx,my)):
                origin_lagoon = e.pos                           #saves the mouse coordinates if it was in one of the regions of the groups
                for group in groups:
                    groups[group] = False                       #sets all of the groups to their regular icons
                groups[surf] = True                             #sets the group that has been hovered over or clicked on as a highlighted icon
            else:
                groups[surf] = False                            #sets all of the groups to their original appearance if the icons aren't used
        if group_surfaces[surf].collidepoint(origin_lagoon):    #sets the group that has been clicked on or hovered over even if
            for group in groups:                                #the mouse coordinates are out of region as long as it has been clicked once
                groups[group] = False
            groups[surf] = True


    for group in groups:
        if reblit_BgCanvasLagoon:
            if groups[group] == True: #and group != 'Colour' and group != 'Stamps' and group != 'Filters': 
                if mouseStat == 'DOWN' and group_surfaces[group].collidepoint((mx,my)):
                    screen.blit(lagoonPRESSED[group], blit_locations[group])
                else:
                    screen.blit(lagoonOVER[group], blit_locations[group])
            elif group_surfaces[group].collidepoint((mx,my)):
                screen.blit(lagoonOVER[group], blit_locations[group])
                screen.blit(macDock[group], (-4,44))
            else:                                                           #icon of the group
                screen.blit(lagoonUP[group], blit_locations[group])


    for group in groups2:
        if reblit_BgCanvasLagoon or collide or group_surfaces2['Colour'].collidepoint((mx,my)):
            if mouseStat == 'DOWN' and group_surfaces2[group].collidepoint((mx,my)):
                screen.blit(lagoonPRESSED2[group], blit_locations2[group])
            elif group_surfaces2[group].collidepoint((mx,my)):
                screen.blit(lagoonOVER2[group], blit_locations2[group])
            else:                                                           #icon of the group
                screen.blit(lagoonUP2[group], blit_locations2[group])

    if groups['Tools']:
        screen.blit(macDock['Tools'], (-4,44))
    if groups['Brushes']:
        screen.blit(macDock['Brushes'], (-4,44))
    if groups['Shapes']:
        screen.blit(macDock['Shapes'], (-4,44))
    if groups['Edit']:
        screen.blit(macDock['Edit'], (-4,44))   

#----------------------------------------------COLOUR WHEEL------------------------------------------------
    if Puck == 'SHOW':
        copyDrawing_col = screen.subsurface(canvas).copy()

    if group_surfaces2['Colour'].collidepoint((col_origin[0], col_origin[1])) or circleCollidepoint(1142,89,col_origin[0],col_origin[1],65):
        collide = True
        
    if groups2['Stamps'] == False and groups2['Filters'] == False:
        if circleCollidepoint(1127,78,col_origin[0],col_origin[1],37) or circleCollidepoint(1176,82,col_origin[0],col_origin[1],27) or collide == True:
            Puck = 'HIDE'
            colourWheel = 'ACTIVE'
            done = False    # variable to blit all of the necessary things for setup

            if lastClick == 'LEFT': hue = primeHue
            elif lastClick == 'RIGHT':  hue = secHue

            screen.blit(col_images['colPalette'], col_surfaces['colPalette'])
            draw.circle(screen, drawCol, (1142,89), 61)
            gfxdraw.aacircle(screen, 1142, 89, 61, drawCol)
            gfxdraw.aacircle(screen, 1141, 88, 61, drawCol)

            screen.blit(col_images['hue'], col_surfaces['hue'])
            draw.polygon(screen, hue, col_surfaces['polygon'])
            screen.blit(col_images['shadePalette'], col_surfaces['shadePalette'])
           
            if lastClick == 'LEFT': draw.circle(screen, (0,0,0), primeID, 5, 1)
            elif lastClick == 'RIGHT':  draw.circle(screen, (0,0,0), secID, 5, 1)

            dist = hypot(mx-1142, my-89)

            if mouseStat == 'DOWN':
                if 38 <= dist <= 57:
                    screen.blit(col_images['hue'], col_surfaces['hue'])
                    draw.polygon(screen, hue, col_surfaces['polygon'])
                    screen.blit(col_images['shadePalette'], col_surfaces['shadePalette'])

                    if mb[0] == 1:
                        primeHue = screen.get_at((mx, my))      # gets the colour
                        primeCol = screen.get_at(primeID)       # gets the shade of that colour
                        draw.circle(screen, (0,0,0), primeID, 5, 1)  # draws a circle to show the point where that colour is selected

                    elif mb[2] == 1:
                        secHue = screen.get_at((mx, my))
                        secCol = screen.get_at(secID)
                        draw.circle(screen, (0,0,0), secID, 5, 1)

                elif shadePaletteCollide.get_at((mx,my)) == (0,0,0):  #<collidepointDiamond>:   #how would you find collidepoint for a diamond ##########circleCollidepoint(1142,89,mx,my,38) and
                    screen.blit(col_images['hue'], col_surfaces['hue'])
                    draw.polygon(screen, hue, col_surfaces['polygon'])
                    screen.blit(col_images['shadePalette'], col_surfaces['shadePalette'])

                    if mb[0] == 1:
                        primeID = (mx,my)      # gets the colour
                        primeCol = screen.get_at(primeID)       # gets the shade of that colour
                        draw.circle(screen, (0,0,0), primeID, 5, 1)  # draws a circle to show the point where that colour is selected

                    elif mb[2] == 1:
                        secID = (mx,my)
                        secCol = screen.get_at(secID)
                        draw.circle(screen, (0,0,0), secID, 5, 1)
    
    if group_surfaces2['Colour'].collidepoint((col_origin[0], col_origin[1])) == False:
        if circleCollidepoint(1127,78,mx,my,37) == False or circleCollidepoint(1176,82,mx,my,27) == False:
            col_origin = (0,0)
    

	#--------------------------------LAGOOON ICONS-------------------------------------------   
    if circleCollidepoint(1142,89,mx,my,65) == False and done == False and group_surfaces2['Colour'].collidepoint((col_origin[0],col_origin[1])) == False:
        if canvas.collidepoint((mx,my)) == False or mouseStat == 'UP':
            screen.blit(background, (0,0))
            
        screen.blit(copyDrawing_col, (100,84))
            
        lagoon(screen, canvas, background, drawCol)

        for group in groups:
            if reblit_BgCanvasLagoon:
                if groups[group] == True: #and group != 'Colour' and group != 'Stamps' and group != 'Filters': 
                    if mouseStat == 'DOWN' and group_surfaces[group].collidepoint((mx,my)):
                        screen.blit(lagoonPRESSED[group], blit_locations[group])
                    else:
                        screen.blit(lagoonOVER[group], blit_locations[group])
                elif group_surfaces[group].collidepoint((mx,my)):
                    screen.blit(lagoonOVER[group], blit_locations[group])
                    screen.blit(macDock[group], (-4,44))
                else:                                                           #icon of the group
                    screen.blit(lagoonUP[group], blit_locations[group])

            if group != 'Edit' and groups[group] != True:
                OK = True

        for group in groups2:
            if reblit_BgCanvasLagoon or collide or group_surfaces2['Colour'].collidepoint((mx,my)):
                if mouseStat == 'DOWN' and group_surfaces2[group].collidepoint((mx,my)):
                    screen.blit(lagoonPRESSED2[group], blit_locations2[group])
                elif group_surfaces2[group].collidepoint((mx,my)):
                    screen.blit(lagoonOVER2[group], blit_locations2[group])
                else:                                                           #icon of the group
                    screen.blit(lagoonUP2[group], blit_locations2[group])
        
        if DockBasics['iTunes']:
            if circleCollidepoint(18,731,mx,my,11):
                screen.blit(image.load('Resources/ModeID/CurrentTool_over.png'), (-2,711))
                screen.blit(ModeID_DockBasics['iTunes'], (-6,708))
            else:
                screen.blit(ModeID_DockBasics['iTunes'], (-6,708))

        if groups['Tools']:
            for app in Tools:
                if Tools[app]:
                    if circleCollidepoint(18,731,mx,my,11):
                        screen.blit(image.load('Resources/ModeID/CurrentTool_over.png'), (-2,711))
                        screen.blit(ModeID_Tools[app], (-6,708))
                    else:
                        screen.blit(ModeID_Tools[app], (-6,708))

        elif groups['Brushes']:
            for app in Brushes:
                if Brushes[app]:
                    if circleCollidepoint(18,731,mx,my,11):
                        screen.blit(image.load('Resources/ModeID/CurrentTool_over.png'), (-2,711))
                        screen.blit(ModeID_Brushes[app], (-6,708))
                    else:
                        screen.blit(ModeID_Brushes[app], (-6,708))

        elif groups['Shapes']:
            for app in Shapes:
                if app == 'Filled' or app == 'Snap':    pass
                elif Shapes[app]:
                    if circleCollidepoint(18,731,mx,my,11):
                        screen.blit(image.load('Resources/ModeID/CurrentTool_over.png'), (-2,711))
                        screen.blit(ModeID_Shapes[app], (-6,708))
                    else:
                        screen.blit(ModeID_Shapes[app], (-6,708))

        elif groups['Edit']:
            for app in Edit:
                if Edit[app]:
                    if circleCollidepoint(18,731,mx,my,11):
                        screen.blit(image.load('Resources/ModeID/CurrentTool_over.png'), (-2,711))
                        screen.blit(ModeID_Edit[app], (-6,708))
                    else:
                        screen.blit(ModeID_Edit[app], (-6,708))

        if circleCollidepoint(18,760,mx,my,7):
            screen.blit(image.load('Resources/ModeID/CurrentColour_over.png'), (-2,740))
            draw.circle(screen, drawCol, (18,760),7)
        else:
            screen.blit(image.load('Resources/ModeID/CurrentColour.png'), (-2,740))
            draw.circle(screen, drawCol, (18,760),7)

        if len(undoList) > 1:
            screen.blit(image.load('Resources/LagoonIcons/Undo.png'), (76,780))
            if circleCollidepoint(93,798,mx,my,18):
                screen.blit(image.load('Resources/LagoonIcons/Undo_over.png'), (76,780))
            elif circleCollidepoint(93,798,mx,my,18) and mouseStat == 'DOWN':
                screen.blit(image.load('Resources/LagoonIcons/Undo_pressed.png'), (76,780))
        else:
            screen.blit(image.load('Resources/LagoonIcons/Undo_dim.png'), (76,780))

        if len(redoList) > 0:
            screen.blit(image.load('Resources/LagoonIcons/Redo.png'), (110,780))
            if circleCollidepoint(131,798,mx,my,16):
                screen.blit(image.load('Resources/LagoonIcons/Redo_over.png'), (110,780))
            elif circleCollidepoint(131,798,mx,my,16) and mouseStat == 'DOWN':
                screen.blit(image.load('Resources/LagoonIcons/Redo_pressed.png'), (110,780))
        else:
            screen.blit(image.load('Resources/LagoonIcons/Redo_dim.png'), (110,780))
        
        colourPuck(screen, 1127, 78, lastClick, primeCol, secCol, puckLarge, puckSmall)
        
        colourWheel = 'INACTIVE'
        collide = False
        done = True

    if secCol != old_secCol or primeCol != old_primeCol or lastClick != old_lastClick or canvasDrawing == 'REBLIT':  # glitch in python which gives the puck images a
        if colourWheel == 'INACTIVE':
            if canvas.collidepoint((mx,my)) == False or mouseStat == 'UP':
                colourPuck(screen, 1127, 78, lastClick, primeCol, secCol, puckLarge, puckSmall)                               # dark black border every time they are blitted in the event loop
            Puck = 'SHOW'   # variable to make sure that when the canvas is copied the puck is showing as opposed to the colour palette
    
    if group_surfaces2['Colour'].collidepoint((col_origin[0],col_origin[1])) or circleCollidepoint(1142,89,mx,my,65) and Puck == 'HIDE':
        if DockBasics['iTunes']:
            if circleCollidepoint(18,731,mx,my,11):
                screen.blit(image.load('Resources/ModeID/CurrentTool_over.png'), (-2,711))
                screen.blit(ModeID_DockBasics['iTunes'], (-6,708))
            else:
                screen.blit(ModeID_DockBasics['iTunes'], (-6,708))

        if groups['Tools']:
            for app in Tools:
                if Tools[app]:
                    if circleCollidepoint(18,731,mx,my,11):
                        screen.blit(image.load('Resources/ModeID/CurrentTool_over.png'), (-2,711))
                        screen.blit(ModeID_Tools[app], (-6,708))
                    else:
                        screen.blit(ModeID_Tools[app], (-6,708))

        elif groups['Brushes']:
            for app in Brushes:
                if Brushes[app]:
                    if circleCollidepoint(18,731,mx,my,11):
                        screen.blit(image.load('Resources/ModeID/CurrentTool_over.png'), (-2,711))
                        screen.blit(ModeID_Brushes[app], (-6,708))
                    else:
                        screen.blit(ModeID_Brushes[app], (-6,708))

        elif groups['Shapes']:
            for app in Shapes:
                if app == 'Filled' or app == 'Snap':    pass
                elif Shapes[app]:
                    if circleCollidepoint(18,731,mx,my,11):
                        screen.blit(image.load('Resources/ModeID/CurrentTool_over.png'), (-2,711))
                        screen.blit(ModeID_Shapes[app], (-6,708))
                    else:
                        screen.blit(ModeID_Shapes[app], (-6,708))

        elif groups['Edit']:
            for app in Edit:
                if Edit[app]:
                    if circleCollidepoint(18,731,mx,my,11):
                        screen.blit(image.load('Resources/ModeID/CurrentTool_over.png'), (-2,711))
                        screen.blit(ModeID_Edit[app], (-6,708))
                    else:
                        screen.blit(ModeID_Edit[app], (-6,708))

        if circleCollidepoint(18,760,mx,my,7):
            screen.blit(image.load('Resources/ModeID/CurrentColour_over.png'), (-2,740))
            draw.circle(screen, drawCol, (18,760),7)
        else:
            screen.blit(image.load('Resources/ModeID/CurrentColour.png'), (-2,740))
            draw.circle(screen, drawCol, (18,760),7)

        if len(undoList) > 1:
            screen.blit(image.load('Resources/LagoonIcons/Undo.png'), (76,780))
            if circleCollidepoint(93,798,mx,my,18):
                screen.blit(image.load('Resources/LagoonIcons/Undo_over.png'), (76,780))
            elif circleCollidepoint(93,798,mx,my,18) and mouseStat == 'DOWN':
                screen.blit(image.load('Resources/LagoonIcons/Undo_pressed.png'), (76,780))
        else:
            screen.blit(image.load('Resources/LagoonIcons/Undo_dim.png'), (76,780))

        if len(redoList) > 0:
            screen.blit(image.load('Resources/LagoonIcons/Redo.png'), (110,780))
            if circleCollidepoint(131,798,mx,my,16):
                screen.blit(image.load('Resources/LagoonIcons/Redo_over.png'), (110,780))
            elif circleCollidepoint(131,798,mx,my,16) and mouseStat == 'DOWN':
                screen.blit(image.load('Resources/LagoonIcons/Redo_pressed.png'), (110,780))
        else:
            screen.blit(image.load('Resources/LagoonIcons/Redo_dim.png'), (110,780))

#----------------------------------------------COLOUR WHEEL------------------------------------------------

#----------------------------------------------APP ICONS------------------------------------------------
    
    if mouseStat == 'DOWN' and colourWheel == 'INACTIVE':

        if DockBasics_surfs['iPaintPro'].collidepoint((mx,my)):
            for app in DockBasics:   #every basic application in the dock
                DockBasics[app] = False
            DockBasics['iPaintPro'] = True

        elif DockBasics_surfs['iTunes'].collidepoint((mx,my)):
            for app in DockBasics:   #every basic application in the dock
                DockBasics[app] = False
            DockBasics['iTunes'] = True

        elif DockBasics_surfs['Open'].collidepoint((mx,my)):
            drawTransCircle(screen, (255,255,255,125), 5, 463, 2)
            time.delay(100)
            DockBasics['Open'] = True

        elif DockBasics_surfs['Save'].collidepoint((mx,my)):
            drawTransCircle(screen, (255,255,255,125), 5, 499, 2)
            time.delay(100)
            DockBasics['Save'] = True

        elif DockBasics_surfs['AddImg'].collidepoint((mx,my)):
            copyDrawing = screen.subsurface(canvas).copy()
            drawTransCircle(screen, (255,255,255,125), 5, 536, 2)
            time.delay(100)
            DockBasics['AddImg'] = True

        elif DockBasics_surfs['Clear'].collidepoint((mx,my)):
            drawing = True
            DockBasics['Clear'] = True


        if groups['Tools']:
            if canvas.collidepoint((mx,my)):
                drawing = True

            if Tools_surfs['Pencil'].collidepoint((mx,my)):
                for app in Tools:
                    Tools[app] = False
                Tools['Pencil'] = True


            elif Tools_surfs['Eraser'].collidepoint((mx,my)):
                for app in Tools:
                    Tools[app] = False
                Tools['Eraser'] = True

            elif Tools_surfs['Text'].collidepoint((mx,my)):
                for app in Tools:
                    Tools[app] = False
                Tools['Text'] = True

            elif Tools_surfs['Fill'].collidepoint((mx,my)):
                for app in Tools:
                    Tools[app] = False
                Tools['Fill'] = True

            elif Tools_surfs['GradientFill'].collidepoint((mx,my)):
                for app in Tools:
                    Tools[app] = False
                Tools['GradientFill'] = True

            elif Tools_surfs['Crop'].collidepoint((mx,my)):
                for app in Tools:
                    Tools[app] = False
                Tools['Crop'] = True


        if groups['Brushes']:
            if canvas.collidepoint((mx,my)):
                drawing = True

            if Brushes_surfs['Airbrush'].collidepoint((mx,my)):
                for app in Brushes:
                    Brushes[app] = False
                Brushes['Airbrush'] = True

            elif Brushes_surfs['SprayCan'].collidepoint((mx,my)):
                for app in Brushes:
                    Brushes[app] = False
                Brushes['SprayCan'] = True

            elif Brushes_surfs['BallpointPen'].collidepoint((mx,my)):
                for app in Brushes:
                    Brushes[app] = False
                Brushes['BallpointPen'] = True

            elif Brushes_surfs['Marker'].collidepoint((mx,my)):
                for app in Brushes:
                    Brushes[app] = False
                Brushes['Marker'] = True

            elif Brushes_surfs['PaintBrush'].collidepoint((mx,my)):
                for app in Brushes:
                    Brushes[app] = False
                Brushes['PaintBrush'] = True

            elif Brushes_surfs['Pencil'].collidepoint((mx,my)):
                for app in Brushes:
                    Brushes[app] = False
                Brushes['Pencil'] = True


        if groups['Shapes']:
            if canvas.collidepoint((mx,my)):
                drawing = True

            if Shapes_surfs['Snap'].collidepoint((mx,my)) and oldmx != mx and oldmy != my:
                time.delay(100)
                if Shapes['Snap'] == False:
                    Shapes['Snap'] = True
                else:
                    Shapes['Snap'] = False

            if Shapes_surfs['Filled'].collidepoint((mx,my)) and oldmx != mx and oldmy != my:
                time.delay(100)
                if Shapes['Filled'] == False:
                    Shapes['Filled'] = True
                else:
                    Shapes['Filled'] = False

            if Shapes_surfs['Line'].collidepoint((mx,my)):
                for app in Shapes:
                    if app == 'Filled' or app == 'Snap':    pass
                    else:
                        Shapes[app] = False
                Shapes['Line'] = True  #have to account for pressing snap and filled later

            elif Shapes_surfs['Ellipse'].collidepoint((mx,my)):
                for app in Shapes:
                    if app == 'Filled' or app == 'Snap':    pass
                    else:
                        Shapes[app] = False
                Shapes['Ellipse'] = True  #have to account for pressing snap and filled later

            elif Shapes_surfs['Rect'].collidepoint((mx,my)):
                for app in Shapes:
                    if app == 'Filled' or app == 'Snap':    pass
                    else:
                        Shapes[app] = False
                Shapes['Rect'] = True  #have to account for pressing snap and filled later

            elif Shapes_surfs['Polygon'].collidepoint((mx,my)):
                drawing = True
                for app in Shapes:
                    if app == 'Filled' or app == 'Snap':    pass
                    else:
                        Shapes[app] = False
                Shapes['Polygon'] = True  #have to account for pressing snap and filled later     # neeed to add code for polygon tool


        if groups['Edit']:

            if canvas.collidepoint((mx,my)):
                drawing = True

            if Edit_surfs['Move'].collidepoint((mx,my)):
                for app in Edit:
                    Edit[app] = False
                Edit['Move'] = True  #have to account for pressing snap and filled later

            elif Edit_surfs['Crop'].collidepoint((mx,my)):
                for app in Edit:
                    Edit[app] = False
                Edit['Crop'] = True  #have to account for pressing snap and filled later

            elif Edit_surfs['Copy'].collidepoint((mx,my)):
                for app in Edit:
                    Edit[app] = False
                Edit['Copy'] = True  #have to account for pressing snap and filled later

            elif Edit_surfs['Paste'].collidepoint((mx,my)):
                for app in Edit:
                    Edit[app] = False
                Edit['Paste'] = True  #have to account for pressing snap and filled later

            elif Edit_surfs['Cut'].collidepoint((mx,my)):
                for app in Edit:
                    Edit[app] = False
                Edit['Cut'] = True  #have to account for pressing snap and filled later

            elif Edit_surfs['View'].collidepoint((mx,my)):
                for app in Edit:
                    Edit[app] = False
                Edit['View'] = True  #have to account for pressing snap and filled later

#----------------------------------------------APP ICONS------------------------------------------------
        
#----------------------------------------------FUNCTIONALITY------------------------------------------------
        
        if DockBasics['Clear']:
            drawTransCircle(screen, (255,255,255,125), 5, 597, 2)
            clearCanvas(screen, canvas)
            DockBasics['Clear'] = False


        if DockBasics['Open']:
            drawTransCircle(screen, (255,255,255,125), 5, 463, 2)
            fileName = saveload.askopenfilename()
            try:
                screen.blit(image.load(fileName), canvas)
                DockBasics['Open'] = False
            except:
                DockBasics['Open'] = False


        if DockBasics['AddImg']:
            drawTransCircle(screen, (255,255,255,125), 5, 536, 2)
            fileName = saveload.askopenfilename()
            CustImg = fileName
            if len(CustImg) > 0:
                loadCustImg = True
            DockBasics['AddImg'] = False                


        if canvas.collidepoint((mx,my)) or canvas.collidepoint((mx,my))==False:
            if DockBasics['iPaintPro']:
                drawTransCircle(screen, (255,255,255,125), 5, 140, 2)
                #code goes here to show details (about dialog box)
                pass

            if groups['Tools']:
                if Tools['Pencil']:
                    drawTransCircle(screen, (255,255,255,125), 5, 198, 2)
                    threshold = 10
                    if brush_size > threshold: brush_size = threshold
                    drawPencil(screen, canvas, drawCol, oldmx, oldmy, mx, my, brush_size)

                elif Tools['Eraser']:
                    drawTransCircle(screen, (255,255,255,125), 5, 233, 2)
                    threshold = 75
                    if brush_size > threshold: brush_size = threshold
                    drawPencil(screen, canvas, bg_col, oldmx, oldmy, mx, my, brush_size)

                elif Tools['Text']:
                    drawTransCircle(screen, (255,255,255,125), 5, 267, 2)               

                elif Tools['Fill']:
                    drawTransCircle(screen, (255,255,255,125), 5, 299, 2)
                    ScanLineStack_floodFill(screen, canvas, stack, mx, my, drawCol)

                elif Tools['GradientFill']:
                    drawTransCircle(screen, (255,255,255,125), 5, 338, 2)
                    GradfloodFill(screen, canvas, stack, mx, my, cmx, cmy, primeCol, secCol)

                elif Tools['Crop']:
                    drawTransCircle(screen, (255,255,255,125), 5, 375, 2)
                    

            if groups['Brushes']:
                if Brushes['Airbrush']:
                    drawTransCircle(screen, (255,255,255,125), 5, 199, 2)
                    threshold = 65
                    if brush_size > threshold: brush_size = threshold
                    drawAirspray(screen, canvas, drawCol, oldmx, oldmy, mx, my, brush_size)

                elif Brushes['SprayCan']:
                    drawTransCircle(screen, (255,255,255,125), 5, 236, 2)
                    threshold = 50
                    if brush_size > threshold: brush_size = threshold
                    drawSprayCan(screen, canvas, drawCol, oldmx, oldmy, mx, my, 150, brush_size)

                elif Brushes['BallpointPen']:
                    drawTransCircle(screen, (255,255,255,125), 5, 270, 2)
                    drawPencil(screen, canvas, drawCol, oldmx, oldmy, mx, my, 1)

                elif Brushes['Marker']:
                    drawTransCircle(screen, (255,255,255,125), 5, 305, 2)
                    threshold = 50
                    if brush_size > threshold: brush_size = threshold
                    drawMarker(screen, canvas, drawCol, oldmx, oldmy, mx, my, brush_size)

                elif Brushes['PaintBrush']:
                    drawTransCircle(screen, (255,255,255,125), 5, 305, 2)
                    threshold = 55
                    if brush_size > threshold: brush_size = threshold
                    drawTransCircle(screen, (255,255,255,125), 5, 340, 2)
                    drawPaintBrush(screen, canvas, drawCol, oldmx, oldmy, mx, my, brush_size)

                elif Brushes['Pencil']:
                    drawTransCircle(screen, (255,255,255,125), 5, 374, 2)
                    threshold = 10
                    if brush_size > threshold: brush_size = threshold
                    drawPencil(screen, canvas, drawCol, oldmx, oldmy, mx, my, brush_size)

            if groups['Shapes']:
                if Shapes['Line']:
                    drawTransCircle(screen, (255,255,255,125), 5, 199, 2)
                    threshold = 70
                    if brush_size > threshold: brush_size = threshold
                    if e.type == MOUSEBUTTONDOWN:
                        origin = e.pos
                        WHpoints = origin
                        copyDrawing = screen.subsurface(canvas).copy()
                    if Shapes['Snap']:
                        if mouse.get_pos() != origin:
                            drawSnapLine(screen, canvas, copyDrawing, drawCol, origin, mx, my, brush_size)
                    else:
                        if mouse.get_pos() != origin:
                            drawFilledLine(screen, canvas, copyDrawing, drawCol, origin, mx, my, brush_size)

                elif Shapes['Ellipse']:
                    drawTransCircle(screen, (255,255,255,125), 5, 281, 2)
                    threshold = 100
                    if brush_size > threshold: brush_size = threshold
                    if e.type == MOUSEBUTTONDOWN:
                        origin = e.pos
                        WHpoints = origin
                        copyDrawing = screen.subsurface(canvas).copy()
                    if Shapes['Filled'] == False:
                        if mouse.get_pos() != origin:
                            drawUnfilledEllipse(screen, canvas, copyDrawing, drawCol, origin, mx, my, brush_size)
                    else:
                        if mouse.get_pos() != origin:
                            drawFilledEllipse(screen, canvas, copyDrawing, drawCol, origin, mx, my)

                elif Shapes['Rect']:
                    drawTransCircle(screen, (255,255,255,125), 5, 308, 2)
                    threshold = 100
                    if brush_size > threshold: brush_size = threshold
                    if e.type == MOUSEBUTTONDOWN:

                        origin = e.pos
                        WHpoints = origin
                        copyDrawing = screen.subsurface(canvas).copy()
                    if Shapes['Filled'] == False:
                        if mouse.get_pos() != origin:
                            drawUnfilledRectangle(screen, canvas, copyDrawing, drawCol, origin, mx, my, brush_size)
                    else:
                        if mouse.get_pos() != origin:
                            drawFilledRectangle(screen, canvas, copyDrawing, drawCol, origin, mx, my)

                elif Shapes['Polygon']:
                    drawTransCircle(screen, (255,255,255,125), 5, 340, 2)
                    threshold = 100
                    if brush_size > threshold: brush_size = threshold
                    if e.type == MOUSEBUTTONDOWN:
                        origin = e.pos
                        WHpoints = origin
                        copyDrawing = screen.subsurface(canvas).copy()
                    if Shapes['Filled'] == False and canvas.collidepoint((mx,my)):
                        drawUnfilledPolygon(screen, canvas, copyDrawing, primeCol, points, polygon_origin, oldpolygon_origin, mx, my, mb)
                        if mb[2] == 1:  points = []
                    else:
                        if canvas.collidepoint((mx,my)):
                            drawFilledPolygon(screen, canvas, copyDrawing, primeCol, points, polygon_origin, oldpolygon_origin, mx, my, mb)
                            if mb[2] == 1:  points = []

            if groups['Edit']:
                if OK == False:
                    screen.blit(license, (100,84))

                    if OKsurf.collidepoint((mx,my)):    
                        OK = True
                        screen.blit(copyDrawing_Edit, (100,84))
                    if MoreInfoSurf.collidepoint((mx,my)):  
                        MoreInfo = True
                        screen.blit(copyDrawing_Edit, (100,84))

                if Edit['Move']:
                    drawTransCircle(screen, (255,255,255,125), 5, 201, 2)
                    pass

                elif Edit['Crop']:
                    drawTransCircle(screen, (255,255,255,125), 5, 233, 2)
                    #code goes here for crop (same as crop before)
                    pass

                elif Edit['Copy']:
                    drawTransCircle(screen, (255,255,255,125), 5, 270, 2)
                    #code goes here for copy
                    pass

                elif Edit['Paste']:
                    drawTransCircle(screen, (255,255,255,125), 5, 305, 2)
                    #code goes here for paste
                    pass

                elif Edit['Cut']:
                    drawTransCircle(screen, (255,255,255,125), 5, 338, 2)
                    #code goes here for cut
                    pass

                elif Edit['View']:
                    drawTransCircle(screen, (255,255,255,125), 5, 372, 2)
                    #code goes here for view
                    pass
#----------------------------------------------FUNCTIONALITY------------------------------------------------


#----------------------------------------------TEXT LABELS------------------------------------------------

    if DockBasics_surfs['Finder'].collidepoint((mx,my)):
        screen.blit(image.load('Resources/Text/Finder.png'), (49,60))

    elif DockBasics_surfs['Launch'].collidepoint((mx,my)):
        screen.blit(image.load('Resources/Text/Launch.png'), (49,90))

    elif DockBasics_surfs['iPaintPro'].collidepoint((mx,my)):
        screen.blit(image.load('Resources/Text/About.png'), (49,132))

    elif DockBasics_surfs['iTunes'].collidepoint((mx,my)):
        screen.blit(image.load('Resources/Text/iTunes.png'), (49,424))

    elif DockBasics_surfs['Open'].collidepoint((mx,my)):
        screen.blit(image.load('Resources/Text/Open.png'), (49,457))

    elif DockBasics_surfs['Save'].collidepoint((mx,my)):
        screen.blit(image.load('Resources/Text/Save.png'), (49,490))

    elif DockBasics_surfs['AddImg'].collidepoint((mx,my)):
        screen.blit(image.load('Resources/Text/AddImg.png'), (49,527))

    elif DockBasics_surfs['Clear'].collidepoint((mx,my)):
        screen.blit(image.load('Resources/Text/Clear.png'), (49,586))


    if groups['Tools']:
        if Tools_surfs['Pencil'].collidepoint((mx,my)):
            screen.blit(image.load('Resources/Text/Pencil.png'), (49,190))

        elif Tools_surfs['Eraser'].collidepoint((mx,my)):
            screen.blit(image.load('Resources/Text/Eraser.png'), (49,226))

        elif Tools_surfs['Text'].collidepoint((mx,my)):
            screen.blit(image.load('Resources/Text/Text.png'), (49,262))

        elif Tools_surfs['Fill'].collidepoint((mx,my)):
            screen.blit(image.load('Resources/Text/Fill.png'), (49,294))

        elif Tools_surfs['GradientFill'].collidepoint((mx,my)):
            screen.blit(image.load('Resources/Text/GradFill.png'), (49,330))

        elif Tools_surfs['Crop'].collidepoint((mx,my)):
            screen.blit(image.load('Resources/Text/Crop.png'), (49,367))

    if groups['Brushes']:
        if Brushes_surfs['Airbrush'].collidepoint((mx,my)):
            screen.blit(image.load('Resources/Text/Airbrush.png'), (49,190))

        elif Brushes_surfs['SprayCan'].collidepoint((mx,my)):
            screen.blit(image.load('Resources/Text/SprayCan.png'), (49,226))

        elif Brushes_surfs['BallpointPen'].collidepoint((mx,my)):
            screen.blit(image.load('Resources/Text/Pen.png'), (49,262))

        elif Brushes_surfs['Marker'].collidepoint((mx,my)):
            screen.blit(image.load('Resources/Text/Marker.png'), (49,294))

        elif Brushes_surfs['PaintBrush'].collidepoint((mx,my)):
            screen.blit(image.load('Resources/Text/PaintBrush.png'), (49,330))

        elif Brushes_surfs['Pencil'].collidepoint((mx,my)):
            screen.blit(image.load('Resources/Text/Pencil.png'), (49,364))

    if groups['Shapes']:
        if Shapes_surfs['Line'].collidepoint((mx,my)):
            screen.blit(image.load('Resources/Text/Line.png'), (49,190))

        elif Shapes_surfs['Ellipse'].collidepoint((mx,my)):
            screen.blit(image.load('Resources/Text/Ellipse.png'), (49,268))

        elif Shapes_surfs['Rect'].collidepoint((mx,my)):
            screen.blit(image.load('Resources/Text/Rect.png'), (49,298))

        elif Shapes_surfs['Polygon'].collidepoint((mx,my)):
            screen.blit(image.load('Resources/Text/Polygon.png'), (49,328))

#----------------------------------------------TEXT LABELS------------------------------------------------
 
    if reblit_BgCanvasLagoon:
        infoBar(screen, XY, ShapeSize, CanvasSize, FPS)   #blits all of the images at the bottom bar
        displayCanvasXY(screen, CanvasXYsurf, canvas, 14, (255,255,255), (255,255,255), 1172, 794)
    
    if oldmx != mx and oldmy != my or reblit_BgCanvasLagoon:
        displayXY(screen, XYsurf, canvas, 14, (255,255,255), (255,255,255), mx, my, 872, 794)

    displayFPS(screen, FPSsurf, str(round(clock.get_fps(),2)), 12, (255,255,255), (255,255,255), 23,795)
    

    if groups['Shapes'] or Tools['Text']:#Shapes['Rect'] or Shapes['Ellipse'] or Shapes['Line']:#tools['FilledRectangle'] or tools['UnfilledRectangle'] or tools['FilledEllipse'] or tools['UnfilledEllipse'] or tools['FilledLine'] or tools['SnapLine']:
        if mouseStat == 'DOWN' or typing or text_size != old_text_size: 
            if groups['Shapes']:
                displayWH(screen, WHsurf, canvas, 14, (255,255,255), (255,255,255), WHpoints, mx, my, 1017, 794, 'Shapes')
            elif Tools['Text']:
                displayWH(screen, WHsurf, canvas, 14, (255,255,255), (255,255,255), size, mx, my, 1017, 794, 'Text')
                                                                                            #this is the code for the W,H points to be displayed
            if mx == oldmx and my == oldmy:
                WHsurfNEW = screen.subsurface(Rect(1017,794,100,20)).copy()

        elif mouseStat == 'UP' and canvas.collidepoint((mx,my)) or Shapes_surfs['Rect'].collidepoint((mx,my)) or Shapes_surfs['Ellipse'].collidepoint((mx,my)) or Shapes_surfs['Line'].collidepoint((mx,my)):#tool_surfaces['FilledRectangle'].collidepoint((mx,my)) or tool_surfaces['UnfilledRectangle'].collidepoint((mx,my)) or tool_surfaces['FilledEllipse'].collidepoint((mx,my)) or tool_surfaces['UnfilledEllipse'].collidepoint((mx,my)) or tool_surfaces['FilledLine'].collidepoint((mx,my)) or tool_surfaces['SnapLine'].collidepoint((mx,my)):
            screen.blit(WHsurfNEW, (1017, 794))
            screen.blit(WHsurfNEW, (1017,794))

            
#----------------------------------------------ANIMATIONS------------------------------------------------

    if groups['Shapes']:
        if Shapes_surfs['Snap'].collidepoint((mx,my)) and mouseStat == 'DOWN':
            snapON_surf = Rect(1,221,14,24)
            snapOFF_surf = Rect(34,221,13,24)

            if mouseStat == 'DOWN' and Shapes['Snap']:
                screen.blit(ToggleShapes['SnapOnBg'], (1,221))
            elif mouseStat == 'DOWN' and Shapes['Snap'] == False:
                screen.blit(ToggleShapes['SnapOffBg'], (1,221))             #this code controls the animations for the SNAP and FILLED icons under the Shapes group

            draw.circle(screen, (255,255,255), (mx,233), 10)

            if snapON_surf.collidepoint((mx,my)):
                Shapes['Snap'] = True
            elif snapOFF_surf.collidepoint((mx,my)):
                Shapes['Snap'] = False

        if Shapes_surfs['Snap'].collidepoint((mx,my)) == False or mouseStat == 'UP':
            screen.blit(ToggleShapes['SnapOn'], (1,221)) if Shapes['Snap'] else screen.blit(ToggleShapes['SnapOff'], (1,221))

        if Shapes_surfs['Filled'].collidepoint((mx,my)) and mouseStat == 'DOWN':# and oldmx != mx and oldmy != my:
            FilledOn_surf = Rect(1,364,14,24)
            FilledOff_surf = Rect(34,364,13,24)

            if mouseStat == 'DOWN' and Shapes['Filled']:
                screen.blit(ToggleShapes['FilledOnBg'], (1,364))
            elif mouseStat == 'DOWN' and Shapes['Filled'] == False:
                screen.blit(ToggleShapes['FilledOffBg'], (1,364))

            draw.circle(screen, (255,255,255), (mx,376), 10)

            if FilledOn_surf.collidepoint((mx,my)):
                Shapes['Filled'] = True
            elif FilledOff_surf.collidepoint((mx,my)):
                Shapes['Filled'] = False

        if Shapes_surfs['Filled'].collidepoint((mx,my)) == False or mouseStat == 'UP':
            screen.blit(ToggleShapes['FilledOn'], (1,364)) if Shapes['Filled'] else screen.blit(ToggleShapes['FilledOff'], (1,364))

#----------------------------------------------ANIMATIONS------------------------------------------------

#----------------------------------------------BRUSH SIZE SCROLLER------------------------------------------------

    percent = brush_size/threshold
    screen.blit(scroll, (1043,753))
    draw.circle(screen, (255,255,255), (int(percent*172+1049), 762), 6)

#----------------------------------------------BRUSH SIZE SCROLLER------------------------------------------------

#---------------------------------------------------------------STAMPS---------------------------------------------------------------------
    if group_surfaces2['Stamps'].collidepoint(stamp_origin) and copies <= 1: #or DockBasics['Save']:
        copyDrawing_stamps = screen.subsurface(Rect(1020,0,250,815)).copy()
        copyDrawing_stamps2 = screen.subsurface(canvas).copy() #not neccesary just copies the canvas
        goAhead = True
        copies += 1

    if group_surfaces2['Stamps'].collidepoint(stamp_origin) and goAhead:
        groups2['Stamps'] = True
    elif groups2['Stamps'] and sidePanelRect.collidepoint(stamp_origin):
        groups2['Stamps'] = True
    else:
        groups2['Stamps'] = False
        stamps_counter = 1270

    if groups2['Stamps']:
        reblit_Canvas_stamps = True
        if stamps_counter > 1030 and stamps_counter != 1030: stamps_counter -= 25
        screen.blit(transform.scale(StampsSidePanel, (252, 815)), (stamps_counter,0))


        if Stamps_surfs['Apple'].collidepoint((mx,my)) or Stamps_surfs['Apple'].collidepoint(stamp_origin) and mouseStat == 'DOWN' and highlight_stamp:
            screen.blit(StampsSP['Apple'], (1020,6))
        if Stamps_surfs['AndroidWorker'].collidepoint((mx,my)) or Stamps_surfs['AndroidWorker'].collidepoint(stamp_origin) and mouseStat == 'DOWN' and highlight_stamp:
            screen.blit(StampsSP['AndroidWorker'], (1020,11.5))
        if Stamps_surfs['MacHDD'].collidepoint((mx,my)) or Stamps_surfs['MacHDD'].collidepoint(stamp_origin) and mouseStat == 'DOWN' and highlight_stamp:
            screen.blit(StampsSP['MacHDD'], (1020,16.5))
        if Stamps_surfs['Xcode'].collidepoint((mx,my)) or Stamps_surfs['Xcode'].collidepoint(stamp_origin) and mouseStat == 'DOWN' and highlight_stamp:
            screen.blit(StampsSP['Xcode'], (1020,19.5))
        if Stamps_surfs['iCloudDrive'].collidepoint((mx,my)) or Stamps_surfs['iCloudDrive'].collidepoint(stamp_origin) and mouseStat == 'DOWN' and highlight_stamp:
            screen.blit(StampsSP['iCloudDrive'], (1020,24.5))
        if Stamps_surfs['iPhone6+'].collidepoint((mx,my)) or Stamps_surfs['iPhone6+'].collidepoint(stamp_origin) and mouseStat == 'DOWN' and highlight_stamp:
            screen.blit(StampsSP['iPhone6+'], (1020,29.5))


        if Stamps_surfs['Apple'].collidepoint(stamp_origin): 
            if mouseStat == 'DOWN':
                stampsSetupDOWN(screen, StampsMask, copyDrawing_stamps2, canvas, Stamps['Apple'], stamp_resize, mx, my, lastClick, primeCol, secCol, puckLarge, puckSmall)
                copy_once = True
                highlight_stamp = False
            elif mouseStat == 'UP' and copy_once:
                stampsSetupUP(screen, StampsMask, copyDrawing_stamps, copyDrawing_stamps2, canvas, Stamps['Apple'], stamp_resize, mx, my, lastClick, primeCol, secCol, puckLarge, puckSmall)
                copyDrawing_stamps = screen.subsurface(Rect(1020,0,250,815)).copy()
                copyDrawing_stamps2 = screen.subsurface(canvas).copy()
                copy_once = False
                highlight_stamp = False
        if Stamps_surfs['AndroidWorker'].collidepoint(stamp_origin): 
            if mouseStat == 'DOWN':
                stampsSetupDOWN(screen, StampsMask, copyDrawing_stamps2, canvas, Stamps['AndroidWorker'], stamp_resize, mx, my, lastClick, primeCol, secCol, puckLarge, puckSmall)
                copy_once = True
                highlight_stamp = False
            elif mouseStat == 'UP' and copy_once:
                stampsSetupUP(screen, StampsMask, copyDrawing_stamps, copyDrawing_stamps2, canvas, Stamps['AndroidWorker'], stamp_resize, mx, my, lastClick, primeCol, secCol, puckLarge, puckSmall)
                copyDrawing_stamps = screen.subsurface(Rect(1020,0,250,815)).copy()
                copyDrawing_stamps2 = screen.subsurface(canvas).copy()
                copy_once = False
                highlight_stamp = False
        if Stamps_surfs['MacHDD'].collidepoint(stamp_origin): 
            if mouseStat == 'DOWN':
                stampsSetupDOWN(screen, StampsMask, copyDrawing_stamps2, canvas, Stamps['MacHDD'], stamp_resize, mx, my, lastClick, primeCol, secCol, puckLarge, puckSmall)
                copy_once = True
                highlight_stamp = False
            elif mouseStat == 'UP' and copy_once:
                stampsSetupUP(screen, StampsMask, copyDrawing_stamps, copyDrawing_stamps2, canvas, Stamps['MacHDD'], stamp_resize, mx, my, lastClick, primeCol, secCol, puckLarge, puckSmall)
                copyDrawing_stamps = screen.subsurface(Rect(1020,0,250,815)).copy()
                copyDrawing_stamps2 = screen.subsurface(canvas).copy()
                copy_once = False
                highlight_stamp = False
        if Stamps_surfs['Xcode'].collidepoint(stamp_origin): 
            if mouseStat == 'DOWN':
                stampsSetupDOWN(screen, StampsMask, copyDrawing_stamps2, canvas, Stamps['Xcode'], stamp_resize, mx, my, lastClick, primeCol, secCol, puckLarge, puckSmall)
                copy_once = True
                highlight_stamp = False
            elif mouseStat == 'UP' and copy_once:
                stampsSetupUP(screen, StampsMask, copyDrawing_stamps, copyDrawing_stamps2, canvas, Stamps['Xcode'], stamp_resize, mx, my, lastClick, primeCol, secCol, puckLarge, puckSmall)
                copyDrawing_stamps = screen.subsurface(Rect(1020,0,250,815)).copy()
                copyDrawing_stamps2 = screen.subsurface(canvas).copy()
                copy_once = False
                highlight_stamp = False
        if Stamps_surfs['iCloudDrive'].collidepoint(stamp_origin): 
            if mouseStat == 'DOWN':
                stampsSetupDOWN(screen, StampsMask, copyDrawing_stamps2, canvas, Stamps['iCloudDrive'], stamp_resize, mx, my, lastClick, primeCol, secCol, puckLarge, puckSmall)
                copy_once = True
                highlight_stamp = False
            elif mouseStat == 'UP' and copy_once:
                stampsSetupUP(screen, StampsMask, copyDrawing_stamps, copyDrawing_stamps2, canvas, Stamps['iCloudDrive'], stamp_resize, mx, my, lastClick, primeCol, secCol, puckLarge, puckSmall)
                copyDrawing_stamps = screen.subsurface(Rect(1020,0,250,815)).copy()
                copyDrawing_stamps2 = screen.subsurface(canvas).copy()
                copy_once = False
                highlight_stamp = False
        if Stamps_surfs['iPhone6+'].collidepoint(stamp_origin): 
            if mouseStat == 'DOWN':
                stampsSetupDOWN(screen, StampsMask, copyDrawing_stamps2, canvas, Stamps['iPhone6+'], stamp_resize, mx, my, lastClick, primeCol, secCol, puckLarge, puckSmall)
                copy_once = True
                highlight_stamp = False
            elif mouseStat == 'UP' and copy_once:
                stampsSetupUP(screen, StampsMask, copyDrawing_stamps, copyDrawing_stamps2, canvas, Stamps['iPhone6+'], stamp_resize, mx, my, lastClick, primeCol, secCol, puckLarge, puckSmall)
                copyDrawing_stamps = screen.subsurface(Rect(1020,0,250,815)).copy()
                copyDrawing_stamps2 = screen.subsurface(canvas).copy()
                copy_once = False
                highlight_stamp = False
    
#-----------------------------------------------------------------------STAMPS-----------------------------------------------------------------------

#-------------------------------------------------------FILTERS-------------------------------------------------------
    
    if group_surfaces2['Filters'].collidepoint(filter_origin) and copies <= 1: #or DockBasics['Save']:
        copyDrawing_stamps = screen.subsurface(Rect(1020,0,250,815)).copy()
        copyDrawing_stamps2 = screen.subsurface(canvas).copy() #not neccesary just copies the canvas
        goAhead = True
        copies += 1
        
    if group_surfaces2['Filters'].collidepoint(filter_origin) and goAhead:
        groups2['Stamps'] = False
        groups2['Filters'] = True
    elif groups2['Filters'] and sidePanelRect.collidepoint(filter_origin):
        groups2['Filters'] = True
    else:
        groups2['Filters'] = False
        filters_counter = 1270

    if groups2['Filters']:
        if key.get_pressed()[K_LSHIFT]:
            screen.blit(transform.scale(FiltersSidePanel2, (252, 815)), (1020, 0))

            if Filters_surfs['Blur'].collidepoint((mx,my)) and mouseStat == 'DOWN':
                Filters['Blur'] = True
                groups2['Filters'] = False
            else: Filters['Blur'] = False
        
            if Filters_surfs['Sharpen'].collidepoint((mx,my)) and mouseStat == 'DOWN':
                Filters['Sharpen'] = True
                groups2['Filters'] = False
            else: Filters['Sharpen'] = False

            if Filters_surfs['SharpenCol'].collidepoint((mx,my)) and mouseStat == 'DOWN':
                Filters['SharpenCol'] = True
                groups2['Filters'] = False
            else: Filters['SharpenCol'] = False

            if Filters_surfs['Sobel'].collidepoint((mx,my)) and mouseStat == 'DOWN':
                Filters['Sobel'] = True
                groups2['Filters'] = False
            else: Filters['Sobel'] = False

        else:
            reblit_Canvas_stamps = True
            if filters_counter > 1030 and filters_counter != 1030: filters_counter -= 25
            screen.blit(transform.scale(FiltersSidePanel, (252, 815)), (filters_counter,0))

            if Filters_surfs['GrayScale'].collidepoint((mx,my)) and mouseStat == 'DOWN':
                Filters['GrayScale'] = True
                groups2['Filters'] = False
            else: Filters['GrayScale'] = False

            if Filters_surfs['Sepia'].collidepoint((mx,my)) and mouseStat == 'DOWN':
                Filters['Sepia'] = True
                groups2['Filters'] = False
            else: Filters['Sepia'] = False

            if Filters_surfs['Invert'].collidepoint((mx,my)) and mouseStat == 'DOWN':
                Filters['Invert'] = True
                groups2['Filters'] = False
            else: Filters['Invert'] = False

            if Filters_surfs['Pixelate'].collidepoint((mx,my)) and mouseStat == 'DOWN':
                Filters['Pixelate'] = True
                groups2['Filters'] = False
            else: Filters['Pixelate'] = False

            if Filters_surfs['Tint'].collidepoint((mx,my)) and mouseStat == 'DOWN':
                Filters['Tint'] = True
                groups2['Filters'] = False
            else: Filters['Tint'] = False

    if groups2['Stamps'] == False and groups2['Filters'] == False and reblit_Canvas_stamps or DockBasics['Save']:
        screen.blit(copyDrawing_stamps, (1020,0))
        copies = 0
        reblit_Canvas_stamps = False
        reblit_SidePanel = True

    if groups2['Filters'] == False:
        if Filters['GrayScale']:
            grayScale(screen)
            Filters['GrayScale'] = False
        elif Filters['Sepia']:
            sepia(screen)
            Filters['Sepia'] = False
        elif Filters['Invert']:
            invert(screen)
            Filters['Invert'] = False
        elif Filters['Pixelate']:
            pixelate(screen)
            Filters['Pixelate'] = False
        elif Filters['Tint']:
            tint(screen, canvas, drawCol)
            Filters['Tint'] = False
        elif Filters['Blur']:
            screen.blit(gaussianBlur(screen, canvas), (100,84))
            Filters['Blur'] = False
        elif Filters['Sharpen']:
            screen.blit(sharpen(screen, canvas), (100,84))
            Filters['Sharpen'] = False
        elif Filters['SharpenCol']:
            screen.blit(sharpenCol(screen, canvas), (100,84))
            Filters['SharpenCol'] = False
        elif Filters['Sobel']:
            screen.blit(sobel(screen, canvas), (100,84))
            Filters['Sobel'] = False


    if DockBasics['Save']:
        drawTransCircle(screen, (255,255,255,125), 5, 499, 2)
        copyDrawing = screen.subsurface(canvas).copy()
        savename = saveload.asksaveasfilename() 
        image.save(copyDrawing, savename + '.png')
        DockBasics['Save'] = False

    if loadCustImg:
        if mouseStat == 'DOWN':
            try:
                screen.blit(copyDrawing, canvas)
                stamp = stampSize(image.load(CustImg), AddImg_resize)
                screen.set_clip(canvas)
                screen.blit(stamp, stampPos(stamp, mx, my))
                screen.set_clip(None)
                if e.type == MOUSEMOTION:   CustImg_blitOnce = True
            except:
                loadCustImg = False
        if mouseStat == 'UP' and CustImg_blitOnce:
            try:
                screen.blit(copyDrawing, canvas)
                stamp = stampSize(image.load(CustImg), AddImg_resize)
                screen.set_clip(canvas)
                screen.blit(stamp, stampPos(stamp, mx, my))
                screen.set_clip(None)
                CustImg_blitOnce = False
                loadCustImg = False
            except:
                loadCustImg = False

#----------------------------------------------MUSIC------------------------------------------------

    if DockBasics['iTunes']:
        drawTransCircle(screen, (255,255,255,125), 5, 430, 2)
        if reblit_BgCanvasLagoon == True:
            screen.blit(image.load('Resources/iTunes/BestDayofMyLife.png'), (230,760))

        if play and Rect(230,760,335,45).collidepoint((mx,my)):
            if reblit_BgCanvasLagoon == True:
                screen.blit(image.load('Resources/iTunes/Pause.png'), (300,760))
        if pause and Rect(230,760,335,45).collidepoint((mx,my)):
            if reblit_BgCanvasLagoon == True:
                screen.blit(image.load('Resources/iTunes/Play.png'), (300,760))

        if play:
            mixer.music.load(Songs[pos])
            mixer.music.play(loops=1000, start=0.0)
    
        if circleCollidepoint(241,769,mx,my,6) and mouseStat == 'DOWN':
            DockBasics['iTunes'] = False

#----------------------------------------------MUSIC------------------------------------------------

#----------------------------------------------CURRENT TOOL INDICATION------------------------------------------------

    if DockBasics['iPaintPro']:
        drawTransCircle(screen, (255,255,255,125), 5, 140, 2)
    elif DockBasics['iTunes']:
        drawTransCircle(screen, (255,255,255,125), 5, 430, 2)
    elif DockBasics['Open']:
        drawTransCircle(screen, (255,255,255,125), 5, 463, 2)
    elif DockBasics['Save']:
        drawTransCircle(screen, (255,255,255,125), 5, 499, 2)
    elif DockBasics['AddImg']:
        drawTransCircle(screen, (255,255,255,125), 5, 536, 2)

    if groups['Tools']:
        if Tools['Pencil']:
            drawTransCircle(screen, (255,255,255,125), 5, 198, 2)
        elif Tools['Eraser']:
             drawTransCircle(screen, (255,255,255,125), 5, 233, 2)
        elif Tools['Text']:
            drawTransCircle(screen, (255,255,255,125), 5, 267, 2)
        elif Tools['Fill']:
            drawTransCircle(screen, (255,255,255,125), 5, 299, 2)           #this code draws small translucent circles besides the active apps on the Mac Dock
        elif Tools['GradientFill']:
            drawTransCircle(screen, (255,255,255,125), 5, 338, 2)
        elif Tools['Crop']:
            drawTransCircle(screen, (255,255,255,125), 5, 375, 2)

    if groups['Brushes']:
        if Brushes['Airbrush']:
            drawTransCircle(screen, (255,255,255,125), 5, 199, 2)
        elif Brushes['SprayCan']:
            drawTransCircle(screen, (255,255,255,125), 5, 236, 2)
        elif Brushes['BallpointPen']:
            drawTransCircle(screen, (255,255,255,125), 5, 270, 2)
        elif Brushes['Marker']:
            drawTransCircle(screen, (255,255,255,125), 5, 305, 2)
        elif Brushes['PaintBrush']:
            drawTransCircle(screen, (255,255,255,125), 5, 340, 2)
        elif Brushes['Pencil']:
            drawTransCircle(screen, (255,255,255,125), 5, 374, 2)

    if groups['Shapes']:
        if Shapes['Line']:
            drawTransCircle(screen, (255,255,255,125), 5, 199, 2)
        elif Shapes['Ellipse']:
            drawTransCircle(screen, (255,255,255,125), 5, 281, 2)
        elif Shapes['Rect']:
            drawTransCircle(screen, (255,255,255,125), 5, 308, 2)
        elif Shapes['Polygon']:
            drawTransCircle(screen, (255,255,255,125), 5, 340, 2)

    if groups['Edit']:
        if Edit['Move']:
            drawTransCircle(screen, (255,255,255,125), 5, 201, 2)
        elif Edit['Crop']:
            drawTransCircle(screen, (255,255,255,125), 5, 233, 2)
        elif Edit['Copy']:
            drawTransCircle(screen, (255,255,255,125), 5, 270, 2)
        elif Edit['Paste']:
            drawTransCircle(screen, (255,255,255,125), 5, 305, 2)
        elif Edit['Cut']:
            drawTransCircle(screen, (255,255,255,125), 5, 338, 2)
        elif Edit['View']:
            drawTransCircle(screen, (255,255,255,125), 5, 372, 2)


    if canvas.collidepoint((mx,my)) == False or mouseStat == 'UP':
        
        if DockBasics['iTunes']:
            if circleCollidepoint(18,731,mx,my,11):
                screen.blit(image.load('Resources/ModeID/CurrentTool_over.png'), (-2,711))
                screen.blit(ModeID_DockBasics['iTunes'], (-6,708))
            else:
                screen.blit(ModeID_DockBasics['iTunes'], (-6,708))

        if groups['Tools']:
            for app in Tools:
                if Tools[app]:
                    if circleCollidepoint(18,731,mx,my,11):
                        screen.blit(image.load('Resources/ModeID/CurrentTool_over.png'), (-2,711))
                        screen.blit(ModeID_Tools[app], (-6,708))
                    else:
                        screen.blit(ModeID_Tools[app], (-6,708))

        elif groups['Brushes']:
            for app in Brushes:
                if Brushes[app]:
                    if circleCollidepoint(18,731,mx,my,11):
                        screen.blit(image.load('Resources/ModeID/CurrentTool_over.png'), (-2,711))
                        screen.blit(ModeID_Brushes[app], (-6,708))
                    else:
                        screen.blit(ModeID_Brushes[app], (-6,708))

        elif groups['Shapes']:
            for app in Shapes:
                if app == 'Filled' or app == 'Snap':    pass
                elif Shapes[app]:
                    if circleCollidepoint(18,731,mx,my,11):
                        screen.blit(image.load('Resources/ModeID/CurrentTool_over.png'), (-2,711))
                        screen.blit(ModeID_Shapes[app], (-6,708))
                    else:
                        screen.blit(ModeID_Shapes[app], (-6,708))

        elif groups['Edit']:
            for app in Edit:
                if Edit[app]:
                    if circleCollidepoint(18,731,mx,my,11):
                        screen.blit(image.load('Resources/ModeID/CurrentTool_over.png'), (-2,711))
                        screen.blit(ModeID_Edit[app], (-6,708))
                    else:
                        screen.blit(ModeID_Edit[app], (-6,708))

        if circleCollidepoint(18,760,mx,my,7):
            screen.blit(image.load('Resources/ModeID/CurrentColour_over.png'), (-2,740))	#current colour indication
            draw.circle(screen, drawCol, (18,760),7)
        else:
            screen.blit(image.load('Resources/ModeID/CurrentColour.png'), (-2,740))
            draw.circle(screen, drawCol, (18,760),7)

#----------------------------------------------CURRENT TOOL INDICATION------------------------------------------------

#----------------------------------------------UNDO/REDO------------------------------------------------

        if len(undoList) > 1:
            screen.blit(image.load('Resources/LagoonIcons/Undo.png'), (76,780))
            if circleCollidepoint(93,798,mx,my,18):
                screen.blit(image.load('Resources/LagoonIcons/Undo_over.png'), (76,780))
            elif circleCollidepoint(93,798,mx,my,18) and mouseStat == 'DOWN':
                screen.blit(image.load('Resources/LagoonIcons/Undo_pressed.png'), (76,780))
        else:
            screen.blit(image.load('Resources/LagoonIcons/Undo_dim.png'), (76,780))

        if len(redoList) > 0:
            screen.blit(image.load('Resources/LagoonIcons/Redo.png'), (110,780))
            if circleCollidepoint(131,798,mx,my,16):
                screen.blit(image.load('Resources/LagoonIcons/Redo_over.png'), (110,780))
            elif circleCollidepoint(131,798,mx,my,16) and mouseStat == 'DOWN':
                screen.blit(image.load('Resources/LagoonIcons/Redo_pressed.png'), (110,780))
        else:
            screen.blit(image.load('Resources/LagoonIcons/Redo_dim.png'), (110,780))

#----------------------------------------------UNDO/REDO------------------------------------------------

    oldmx, oldmy = mx, my
    old_text_size = text_size
    oldpolygon_origin = polygon_origin
    old_primeCol, old_secCol = primeCol, secCol
    old_lastClick = lastClick
    counting += 1

    display.flip()
    clock.tick()
quit()