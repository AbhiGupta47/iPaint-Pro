from pygame import *
from random import *
from math import *
from Functions import *
import numpy
from scipy import ndimage
import os

font.init()



def setScreen(defaultx, defaulty):
    os.environ['SDL_VIDEO_WINDOW_POS'] = str(defaultx)+','+str(defaulty)    #sets screen to default position on startup
    
def setup():
    icon = image.load('Resources/App_Icon.png').convert_alpha()   
    display.set_icon(icon)             #Gives the program an app icon
    display.set_caption('iPaint Pro')  #Gives the program a header name

def myRound(x, base=5):                         #x+1 if you want 5 to round up instead of down
    return int(base * round(float(x)/base))   #rounds value up or down based on the given argument

def circleCollidepoint(cx, cy, mx, my, radius): #checks collision with a cirlce using distance fotmula
    dist = hypot(mx-cx, my-cy)                  #from mouse position
    if dist <= radius:  return True
    else:   return False

def drawTransCircle(surface, colour, location_x, location_y, size):  #draws a transparent circle
    circ = Surface((size*2,size*2), SRCALPHA)
    draw.circle(circ, colour, (size,size), size)
    surface.blit(circ, (location_x, location_y))


def makeText(surface, text, text_size, color, background_color, x, y, fontselection = 'Arial'):
    defaultFont = font.SysFont(fontselection, text_size)    #font used for text
    textSurf = defaultFont.render(text, True, color)  #renders text and blits it onto a surface
    surface.blit(textSurf,(x,y))


def infoBar(surface, XY, ShapeSize, CanvasSize, FPS):
    surface.blit(XY, (840,791))             #blits all of the images at the bottom bar
    surface.blit(ShapeSize, (986,791))      #that display the corresponding information
    surface.blit(CanvasSize, (1136,787))
    surface.blit(FPS, (1,789))

def displayXY(surface, XYsurf, canvas, text_size, text_colour, background_colour, mx, my, location_x, location_y):
    X = mx-100  #position x on canvas
    Y = my-84   #position y on canvas
    if canvas.collidepoint((mx,my)):
        surface.blit(XYsurf, (location_x, location_y))  #blits a cover each time new x,y coordinates are written on the screen
        makeText(surface, str(X)+", "+str(Y)+" px", text_size, text_colour, (255,255,255), location_x, location_y)  #writes mouse pos on canvas

def displayWH(surface, WHsurf, canvas, text_size, text_colour, background_colour, WHpoints, mx, my, location_x, location_y, type = 'Shapes'):
    if type == 'Shapes':          #if current tool is shapes,
        startW = WHpoints[0]-100  #takes in the mouse pos when mouse is clicked on canvas
        startH = WHpoints[1]-84
        endW = mx-100             #current mouse pos to where the shape is being drawn to
        endH = my-84
        W = abs(endW-startW)
        H = abs(endH-startH)
        if W == 0:  W = 1       #if width and length of shape is (0,0), changes is to (1,1)
        if H == 0: H = 1
        if canvas.collidepoint((mx,my)):    #if current mouse pos is on the canvas
            surface.blit(WHsurf, (location_x, location_y))   #renders and blits text (Width and length of shape)
            makeText(surface, str(W)+" x "+str(H)+" px", text_size, text_colour, (255,255,255), location_x, location_y)

    elif type == 'Text':    #blits the size of the text box in which you are typing at the bottom 
        if canvas.collidepoint((mx,my)):
            surface.blit(WHsurf, (location_x, location_y))   
            makeText(surface, str(WHpoints[0])+" x "+str(WHpoints[1])+" px", text_size, text_colour, (255,255,255), location_x, location_y)

def displayCanvasXY(surface, CanvasXYsurf, canvas, text_size, text_colour, background_colour, location_x, location_y):
    X = canvas[2]   #x dimension of canvas
    Y = canvas[3]   #y dimension
    surface.blit(CanvasXYsurf, (location_x, location_y))   #renders and blits the dimensions of the canvas
    makeText(surface, str(X)+" x "+str(Y)+" px", text_size, text_colour, (255,255,255), location_x, location_y)


def displayFPS(surface, FPSsurf, fps, text_size, text_colour, background_colour, location_x, location_y):
    surface.blit(FPSsurf, (location_x, location_y))     #takes in the current FPS and blits it to the bottom left corner of the screen
    makeText(surface, fps, text_size, text_colour, None, location_x, location_y)


def stampSize(stamp, resize):                          
   #resizez stamp when user scrolls                                                
   img = transform.scale(stamp,(int(stamp.get_width()*resize),int(stamp.get_height()*resize)))
   #takes the stamp that the user has selected, gets the height and width, and multiplies it with a value depending on how much the user has scrolled
   return img

def stampPos(stamp, mx, my):                 
   #ensures that the mouse is always in the center of the stamp no matter what size   
   pos = int(mx-(stamp.get_width()/2)),int(my-(stamp.get_height()/2))
   #gets the height and width of the image and to find the middle, the height and width is divided by 2 before being subtracted by the original mouse position
   return pos    

def stampsSetupDOWN(surface, StampsMask, copyDrawing_stamps2, canvas, stamp, stamp_resize, mx, my, lastClick, primeCol, secCol, puckLarge, puckSmall):
    surface.blit(StampsMask, (1020,0))  #blits a cover to prevent the sidePanel from being shown on the canvas after it is disabled
    surface.blit(copyDrawing_stamps2, canvas)   #blits the canvas that was copied prior to activating the sidePanel
    stamp = stampSize(stamp, stamp_resize)  #calls the function stampSize so that the user can adjust the size of the selected stamp
    surface.set_clip(canvas)
    surface.blit(stamp, stampPos(stamp, mx, my))    #blits the surface back on to the canvas, ensuring the stamp is in the middle of the mouse position
    surface.set_clip(None)
    colourPuck(surface, 1127, 78, lastClick, primeCol, secCol, puckLarge, puckSmall)  #blits the colourPuck on the topright corner of the screen back so that it doesnt get
                                                                                      #covered by the other layers that are being blitted

def stampsSetupUP(surface, StampsMask, copyDrawing_stamps, copyDrawing_stamps2, canvas, stamp, stamp_resize, mx, my, lastClick, primeCol, secCol, puckLarge, puckSmall):
    surface.blit(StampsMask, (1020,0))         #this function is the same as the one above but is used to clarify the code when called in main.py
    surface.blit(copyDrawing_stamps2, canvas)
    stamp = stampSize(stamp, stamp_resize)
    surface.set_clip(canvas)
    surface.blit(stamp, stampPos(stamp, mx, my))
    surface.set_clip(None)
    colourPuck(surface, 1127, 78, lastClick, primeCol, secCol, puckLarge, puckSmall)


def lagoon(surface, canvas, background, primeCol):
    Lagoon_Bg = transform.scale(image.load('Resources/LagoonBackground.png'), (250,200))   #blits the arc seen at the bottom left of the screen
    copyDrawing = surface.subsurface(canvas).copy() #copies the canvas and stores it
    surface.blit(background, (0,0))     #blits the entire screen's background
    surface.blit(copyDrawing, (100,84)) #followed by the canvas and then
    surface.blit(Lagoon_Bg, (0,615))    #the lagoon or arc (just the background, no icons)


def colourPuck(surface, x, y, lastClick, primeCol, secCol, puckLarge, puckSmall):
    if lastClick == 'RIGHT':
        draw.circle(surface, primeCol, (x,y), 37)   #draws a circle inside the circle area of the puck with the leftclick colour
        surface.blit(puckLarge, (1080,30))    # blit the large puck on top of coloured circles
        draw.circle(surface, secCol, (x+49,y+4), 27)
        surface.blit(puckSmall, (1140,45))    # blit the small puck on top of coloured circles
    elif lastClick == 'LEFT':
        draw.circle(surface, secCol, (x+49,y+4), 27) #draws a circle inside the circle area of the puck with the rightclick colour
        surface.blit(puckSmall, (1140,45))    # blit the small puck on top of coloured circles
        draw.circle(surface, primeCol, (x,y), 37)
        surface.blit(puckLarge, (1080,30))    # blit the large puck on top of coloured circle     


def drawPencil(surface, canvas, colour, oldmx, oldmy, mx, my, size):
    dist = hypot(mx-oldmx, my-oldmy) #gets distance between the current mouse pos and the last mouse pos 
    dist = max(1, int(dist))         #prevents division by zero error
    if size == 0:   size += 1        #changes the brush size to certain defaults and makes sure that the user is drawing something 
    if size == 2:   size += 1        #rather than the brush being invisble (0 thickness)
    if size == 1:
        surface.set_clip(canvas)
        draw.aaline(surface, colour, (oldmx, oldmy), (mx, my), size)    #draws on the canvas
        surface.set_clip(None)
    else:
        for i in range(dist):
            sx = i*(mx-oldmx)//dist #the distance from the original position 
            sy = i*(my-oldmy)//dist #the distance from the original position
            surface.set_clip(canvas)
            draw.circle(surface, colour, (oldmx+sx, oldmy+sy), size-1)  #draws at every pixel
            surface.set_clip(None)

def drawSprayCan(surface, canvas, colour, oldmx, oldmy, mx, my, speed, size):
    dist = hypot(mx-oldmx, my-oldmy)
    dist = max(1, int(dist))
    if size < 8:   size = 8   #sets the minimum brush size to 8
    for p in range(dist):
        for i in range(speed):     #range controls speed
            if size > 100:
                sprayx = randint(mx-size, mx+size)     #variable value controls size
                sprayy = randint(my-size, my+size)
            elif size <= 100:
                sprayx = randint(mx-100, mx+100)       #variable value controls size
                sprayy = randint(my-100, my+100)       #if its less than a 100, to see the effect it needs to 100 
            sx=p*(oldmx-mx)//dist
            sy=p*(oldmy-my)//dist
            if hypot(mx-sprayx, my-sprayy) < size:   #variable value must be the same as above
                surface.set_clip(canvas)
                draw.circle(surface, colour, (sprayx+sx, sprayy+sy), int(0.9))  #draws at every position with a bunch of small circles
                surface.set_clip(None)

def drawPencil_Block(surface, canvas, colour, oldmx, oldmy, mx, my, size):
    if size == 0:   size += 1
    if size == 1:
        surface.set_clip(canvas)
        draw.aaline(surface, colour, (oldmx, oldmy), (mx, my), size)
        surface.set_clip(None)
    else:
        dist = hypot(mx-oldmx, my-oldmy)
        dist = max(1, int(dist))
        for i in range(dist):
            sx = i*(mx-oldmx)//dist #the distance from the original position
            sy = i*(my-oldmy)//dist #the distance from the original position
            surface.set_clip(canvas)
            aacircle(surface, (oldmx+sx)-(size-0.5), (oldmy+sy)-(size-0.5), size, colour)  #draws an antialiased border of the brush as well as fills it with a circle to make it more smooth
            draw.circle(surface, colour, (oldmx+sx, oldmy+sy), size-1)
            surface.set_clip(None)

def drawPencil_3Drender(surface, canvas, colour, oldmx, oldmy, mx, my, size):
    if size == 0:   size += 1
    if size == 1:
        surface.set_clip(canvas)
        draw.aaline(surface, colour, (oldmx, oldmy), (mx, my), size)
        surface.set_clip(None)
    else:
        dist = hypot(mx-oldmx, my-oldmy)
        dist = max(1, int(dist))
        for i in range(dist):
            sx = i*(mx-oldmx)//dist #the distance from the original position
            sy = i*(my-oldmy)//dist #the distance from the original position
            surface.set_clip(canvas)
            aacircle(surface, (oldmx+sx)-(size-0.5), (oldmy+sy)-(size-0.5), size, colour)  #draws an antialiased border of the brush as well as fills it with a circle to make it more smooth
            surface.set_clip(None)

def drawMarker(surface, canvas, colour, oldmx, oldmy, mx, my, size, alphaVal = 5):
    if size == 0:   size += 5   #sets the default size to 2
    alphaCol = (colour[0], colour[1], colour[2], alphaVal) #alpha colour 
    markerSurf = Surface((size*2,size*2), SRCALPHA)
    if canvas.collidepoint((mx,my)):
        draw.ellipse(markerSurf, alphaCol, (size, 0, size, size//1.35)) #draws an ellipse in the center of the marker surface
        dist = hypot(mx-oldmx, my-oldmy)
        dist = max(1, int(dist))
        cx = (mx-oldmx)/dist
        cy = (my-oldmy)/dist
        for i in range(int(dist)):
            surface.set_clip(canvas)    #for each position, blits the marker surface which is rotated at 52 dgrees clockwise onto the screen
            surface.blit(transform.rotate(markerSurf,-52), (int((oldmx+i*cx)-size*2.15), int((oldmy+i*cy)-size*1.35)))#blit in the center by subracting size from x and y
            surface.set_clip(None)

def drawAirspray(surface, canvas, colour, oldmx, oldmy, mx, my, size, alphaVal = 2):
    if size == 0:   size += 10
    alphaCol = (colour[0], colour[1], colour[2], alphaVal)
    markerSurf = Surface((size*2,size*2), SRCALPHA)
    if mx != oldmx or my != oldmy:
        draw.circle(markerSurf, alphaCol, (size,size), size-1) #size,size = center of markersurface
        dist = hypot(mx-oldmx, my-oldmy)                       #performs the same operation as marker but before blitting the 
        cx = (mx-oldmx)/dist                                   #marker surface, it blurs the entire surface
        cy = (my-oldmy)/dist
        pixelSize = 8
        for x in range(size*2//pixelSize):      #blurring the surface by averaging the pixels' colours
            for y in range(size*2//pixelSize):
                Col = transform.average_color(markerSurf.subsurface((x*pixelSize),(y*pixelSize),pixelSize,pixelSize))
                draw.rect(markerSurf, Col, ((x*pixelSize),(y*pixelSize),pixelSize,pixelSize))
        for i in range(int(dist)):
            surface.set_clip(canvas)
            surface.blit(markerSurf, (int((oldmx+i*cx)-size), int((oldmy+i*cy)-size)))#blit in the center by subracting size from x and y
            surface.set_clip(None)

def drawPaintBrush(surface, canvas, colour, oldmx, oldmy, mx, my, size, alphaVal = 8):
    if size == 0:   size += 1
    alphaCol = (colour[0], colour[1], colour[2], alphaVal)
    markerSurf = Surface((size*2,size*2), SRCALPHA)
    if mx != oldmx or my != oldmy:
        draw.circle(markerSurf, alphaCol, (size,size), size-1) #performs similar operation as marker but with a higher alpha value
        dist = hypot(mx-oldmx, my-oldmy)
        cx = (mx-oldmx)/dist
        cy = (my-oldmy)/dist
        for i in range(int(dist)):
            surface.set_clip(canvas)
            surface.blit(markerSurf, (int((oldmx+i*cx)-size), int((oldmy+i*cy)-size)))#blit in the center by subracting size from x and y
            surface.set_clip(None)

def drawFilledLine(surface, canvas, copyDrawing, colour, origin, mx, my, size):
    if size == 0:   size += 1
    canvas_x, canvas_y = canvas.x, canvas.y
    surface.blit(copyDrawing, (canvas_x, canvas_y))
    dist = hypot(mx-origin[0], my-origin[1])
    dist = max(1, int(dist))
    if mx == origin[0] and my == origin[1]:
        surface.set_clip(canvas)
        draw.circle(surface, colour, (origin[0], origin[1]), size//2)
        surface.set_clip(None)
    else:
        for i in range(int(dist)):
            sx = i*(mx-origin[0])//dist
            sy = i*(my-origin[1])//dist
            surface.set_clip(canvas)
            draw.circle(surface, colour, (origin[0] + sx, origin[1] + sy), size//2)
            surface.set_clip(None)

def drawSnapLine(surface, canvas, copyDrawing, colour, origin, mx, my, size):
    if size == 0:   size += 1
    canvas_x, canvas_y = canvas.x, canvas.y
    surface.blit(copyDrawing, (canvas_x, canvas_y))
    if mx == origin[0] and my == origin[1]:
        surface.set_clip(canvas)
        draw.circle(surface, colour, (origin[0], origin[1]), size//2)
        surface.set_clip(None)
    else:
        dist = hypot(mx-origin[0], my-origin[1])
        dist = max(1, int(dist))
        distx = abs(mx-origin[0])
        distx = max(1, distx)
        disty = abs(my-origin[1])
        theta = degrees(atan(disty/distx))      #uses trig to find horizontal and vertical lines, then afterwards uses myRound function to round the coordinates of the endpoints
        for i in range(int(dist)):
            surface.set_clip(canvas)
            if theta < 11.25:   #for a horizontal line (0 degrees)
                sx = i*(mx-origin[0])//dist
                sy = i*(my-origin[1])//dist
                draw.circle(surface, colour, (origin[0] + sx, origin[1]), size//2)
            elif theta > 67.5:   #for a vertical line (90 degrees)
                sx = i*(mx-origin[0])//dist
                sy = i*(my-origin[1])//dist
                draw.circle(surface, colour, (origin[0], origin[1] + sy), size//2)
            else:
                mx = myRound(mx, 100)   #rounds mx, my to nearest hundred so that it can snap to nearest angle
                my = myRound(my, 100)
                sx = i*(mx-origin[0])//dist
                sy = i*(my-origin[1])//dist
                draw.circle(surface, colour, (origin[0] + sx, origin[1] + sy), size//2)
            surface.set_clip(None)

def drawFilledRectangle(surface, canvas, copyDrawing, colour, origin, mx, my):
    canvas_x, canvas_y = canvas.x, canvas.y
    surface.blit(copyDrawing, (canvas_x, canvas_y))
    width = mx-origin[0]
    length = my-origin[1]
    surface.set_clip(canvas)
    if key.get_pressed()[K_LSHIFT] or key.get_pressed()[K_RSHIFT]:
        Size = min(abs(width), abs(length))
        draw.rect(surface, colour, (origin[0], origin[1], Size if width > 1 else -Size, Size if length > 1 else -Size))
    else:
        draw.rect(surface, colour, (origin[0], origin[1], width, length))
    surface.set_clip(None)

def drawUnfilledRectangle(surface, canvas, copyDrawing, colour, origin, mx, my, size):
    if key.get_pressed()[K_LSHIFT] or key.get_pressed()[K_RSHIFT]:
        if size == 0:   size += 1
        canvas_x, canvas_y = canvas.x, canvas.y
        surface.blit(copyDrawing, (canvas_x, canvas_y))
        width = mx-origin[0]
        length = my-origin[1]
        surface.set_clip(canvas)
        Size = min(abs(width), abs(length))
        draw.rect(surface, colour, (origin[0], origin[1], Size if width > 1 else -Size, Size if length > 1 else -Size), size)
        surface.set_clip(None)
    else:
        if size == 0:   size += 1
        canvas_x, canvas_y = canvas.x, canvas.y
        surface.blit(copyDrawing, (canvas_x, canvas_y))
        if my >= origin[1]:                             #draws individual lines to form rectangle
            surface.set_clip(canvas)
            draw.line(surface, colour, (origin[0], origin[1]-1), (mx, origin[1]-1), size)    #-1 or +1 to origin
            draw.line(surface, colour, (origin[0], origin[1]-size/2), (origin[0], my+size/2), size)    #-1 or +1 to origin
            draw.line(surface, colour, (mx, origin[1]-size/2), (mx, my+size/2), size)    #-1 or +1 to origin
            draw.line(surface, colour, (mx, my), (origin[0], my), size)    #-1 or +1 to origin
            surface.set_clip(None)
        elif my < origin[1]:
            surface.set_clip(canvas)
            draw.line(surface, colour, (origin[0], origin[1]), (mx, origin[1]), size)    #-1 or +1 to origin
            draw.line(surface, colour, (origin[0], origin[1]+size/2), (origin[0], my-size/2), size)    #-1 or +1 to origin
            draw.line(surface, colour, (mx, origin[1]+size/2), (mx, my-size/2), size)    #-1 or +1 to origin
            draw.line(surface, colour, (mx, my-1), (origin[0], my-1), size)    #-1 or +1 to origin
            surface.set_clip(None)

def drawFilledEllipse(surface, canvas, copyDrawing, colour, origin, mx, my):
    canvas_x, canvas_y = canvas.x, canvas.y
    surface.blit(copyDrawing, (canvas_x, canvas_y))
    radx = abs(mx-origin[0])
    rady = abs(my-origin[1])
    if key.get_pressed()[K_LSHIFT] or key.get_pressed()[K_RSHIFT]:
        surface.set_clip(canvas)
        Size = round(hypot(mx-origin[0], my-origin[1]))
        draw.circle(surface, colour, (origin[0], origin[1]), Size)
        surface.set_clip(None)
    else:
        surface.set_clip(canvas)
        draw.ellipse(surface, colour, (min(mx, origin[0]), min(my, origin[1]), radx, rady))
        #gfxdraw.filled_ellipse(screen, min(mx, origin[0]), min(my, origin[1]), width, length, colour)
        surface.set_clip(None)    

def drawUnfilledEllipse(surface, canvas, copyDrawing, colour, origin, mx, my, size):
    canvas_x, canvas_y = canvas.x, canvas.y
    surface.blit(copyDrawing, (canvas_x, canvas_y))
    radx = abs(mx-origin[0])
    rady = abs(my-origin[1])
    surface.set_clip(canvas)
    draw.ellipse(surface, colour, (min(mx, origin[0]), min(my, origin[1]), radx, rady))
    #gfxdraw.filled_ellipse(screen, min(mx, origin[0]), min(my, origin[1]), width, length, colour)
    surface.set_clip(None)
    if size == 0: size += 1
    canvas_x, canvas_y = canvas.x, canvas.y
    surface.blit(copyDrawing, (canvas_x, canvas_y))
    radx = abs(mx-origin[0])
    rady = abs(my-origin[1])
    if size <= 2:
        surface.set_clip(canvas)
        draw.ellipse(surface, colour, (min(mx, origin[0]), min(my, origin[1]), radx, rady), size if 0 < size < min(radx, rady)//2 else 0)
        surface.set_clip(None)
    if size > 2:#radx >= 200 and rady >= 200 and size > 2:
        if mx < origin[0] or my < origin[1]:        #draws a bunch of ellipses at positions +1, -1 relative to mouse pos if endpoint is left from the start point
            surface.set_clip(canvas)
            for i in range(5):
                draw.ellipse(surface, colour, (min(mx+i, origin[0]-i), min(my+i, origin[1]-i), radx, rady), size if 0 < size < min(radx, rady)//2 else 0)
                draw.ellipse(surface, colour, (min(mx-i, origin[0]+i), min(my-i, origin[1]+i), radx, rady), size if 0 < size < min(radx, rady)//2 else 0)
                draw.ellipse(surface, colour, (min(mx-i, origin[0]-i), min(my+i, origin[1]+i), radx, rady), size if 0 < size < min(radx, rady)//2 else 0)
                draw.ellipse(surface, colour, (min(mx+i, origin[0]+i), min(my-i, origin[1]-i), radx, rady), size if 0 < size < min(radx, rady)//2 else 0)
            draw.ellipse(surface, colour, (min(mx+1, origin[0]-1), min(my+1, origin[1]-1), radx, rady), size if 0 < size < min(radx, rady)//2 else 0)
            draw.ellipse(surface, colour, (min(mx-1, origin[0]+1), min(my-1, origin[1]+1), radx, rady), size if 0 < size < min(radx, rady)//2 else 0)
            surface.set_clip(None)
        else:
            surface.set_clip(canvas)
            for i in range(5):
                draw.ellipse(surface, colour, (min(mx-i, origin[0]+i), min(my-i, origin[1]+i), radx, rady), size if 0 < size < min(radx, rady)//2 else 0)
                draw.ellipse(surface, colour, (min(mx+i, origin[0]-i), min(my+i, origin[1]-i), radx, rady), size if 0 < size < min(radx, rady)//2 else 0)
                draw.ellipse(surface, colour, (min(mx+i, origin[0]+i), min(my-i, origin[1]-i), radx, rady), size if 0 < size < min(radx, rady)//2 else 0)
                draw.ellipse(surface, colour, (min(mx-i, origin[0]-i), min(my+i, origin[1]+i), radx, rady), size if 0 < size < min(radx, rady)//2 else 0)
            draw.ellipse(surface, colour, (min(mx-1, origin[0]+1), min(my-1, origin[1]+1), radx, rady), size if 0 < size < min(radx, rady)//2 else 0)
            draw.ellipse(surface, colour, (min(mx+1, origin[0]-1), min(my+1, origin[1]-1), radx, rady), size if 0 < size < min(radx, rady)//2 else 0)
            surface.set_clip(None)

def drawFilledPolygon(surface, canvas, copyDrawing, colour, points, polygon_origin, oldpolygon_origin, mx, my, mb):
    if polygon_origin != oldpolygon_origin and mb[0] == 1:
        surface.set_at((mx,my), colour)
        points.append((mx,my))
    if len(points) > 1 and mb[0] == 1:
        draw.line(surface, colour, points[-2], points[-1], 1)
    if mb[2] == 1 and len(points) > 2:
        draw.polygon(surface, colour, points)

def drawUnfilledPolygon(surface, canvas, copyDrawing, colour, points, polygon_origin, oldpolygon_origin, mx, my, mb):
    if polygon_origin != oldpolygon_origin and mb[0] == 1:
        surface.set_at((mx,my), colour)
        points.append((mx,my))
    if len(points) > 1 and mb[0] == 1:
        draw.line(surface, colour, points[-2], points[-1], 1)
    if mb[2] == 1 and len(points) > 2:
        draw.polygon(surface, colour, points, 1)


def recursive_floodFill(surface, canvas, mx, my, fill_col):
    boundary_col=surface.get_at((mx,my))    #get the colour that is currently wanting to be changed
    if fill_col != boundary_col:    #base case. if the current fill colour isn't the same as the background you are filling.
        screen.set_at((mx,my), fill_col)
        if canvas.collidepoint((mx, my)):
            recursive_floodFill(surface, mx+1, my, fill_col)
            recursive_floodFill(surface, mx, my+1, fill_col)
            recursive_floodFill(surface, mx-1, my, fill_col)
            recursive_floodFill(surface, mx, my-1, fill_col)

def FourWayStack_floodFill(surface, canvas, stack, mx, my, fill_col):
    boundary_col=surface.get_at((mx,my))    #get the colour that is currently wanting to be changed
    if boundary_col != fill_col:            #if existing colour is different it gets the pixel at that location, changes it and looks at the pixels around it
        point=mouse.get_pos()          # until the pixels with the same exchange colour have all been changed
        stack.append(point)
        while len(stack)>0:
            mx,my = stack.pop()
            if surface.get_at((mx,my)) == boundary_col and canvas.collidepoint((mx,my)):
                surface.set_at((mx,my), fill_col)
                stack += ((mx,my+1), (mx+1,my), (mx,my-1), (mx-1,my))

def ScanLineStack_floodFill(surface, canvas, stack, mx, my, fill_col):
    boundary_col=surface.get_at((mx,my))    #get the colour that is currently wanting to be changed
    if boundary_col == fill_col:    return
    y1 = 0
    spanLeft = None
    spanRight = None
    if boundary_col != fill_col:       #if existing colour is different it gets the pixel at that location, changes it and looks at the pixels around it
        point=mouse.get_pos()          #until the pixels with the same exchange colour have all been changed
        stack.append(point)

        while len(stack)>0:
            mx,my = stack.pop()
            y1 = my    #y value is equal to my

            while canvas.collidepoint((mx,y1)) and surface.get_at((mx,y1)) == boundary_col: #if colour is == boundary col, keep moving up 
                y1 -= 1
            y1 += 1  #else keep moving down

            spanLeft = spanRight = False   #spanning both directions is False

            while canvas.collidepoint((mx, y1)) and surface.get_at((mx, y1)) == boundary_col:
                surface.set_at((mx, y1), fill_col)
                if spanLeft == False and canvas.collidepoint((mx, y1)) and surface.get_at((mx-1, y1)) == boundary_col:
                    stack += ((mx-1, y1),)
                    spanLeft = True 
                elif spanLeft and canvas.collidepoint((mx-1, y1)) and surface.get_at((mx-1, y1)) != boundary_col:
                    spanLeft = False

                if spanRight == False and canvas.collidepoint((mx+1, y1)) and surface.get_at((mx+1, y1)) == boundary_col:
                    stack += ((mx+1, y1),)
                elif spanRight and canvas.collidepoint((mx+1, y1)) and surface.get_at((mx+1, y1)) != boundary_col:
                    spanRight = True

                y1 += 1

def GradfloodFill(surface, canvas, stack, mx, my, cmx, cmy, primeCol, secCol):
    #Radial Gradient
    if key.get_pressed()[K_LSHIFT] or key.get_pressed()[K_RSHIFT]:
        boundary_col=surface.get_at((mx,my))    #get the colour that is currently wanting to be changed
        point=mouse.get_pos()          # until the pixels with the same exchange colour have all been changed
        stack.append(point)
        val = 1265
        while len(stack)>0:
            mx,my = stack.pop()
            if surface.get_at((mx,my)) == boundary_col and canvas.collidepoint((mx,my)):
                dist = hypot(mx-cmx, my-cmy)
                R = round(primeCol[0] * (dist/val) + secCol[0] * ((val-dist)/val))
                G = round(primeCol[1] * (dist/val) + secCol[1] * ((val-dist)/val))
                B = round(primeCol[2] * (dist/val) + secCol[2] * ((val-dist)/val))
                if R > 255: R = 255
                if R < 0:   R = 0
                if G > 255: G = 255
                if G < 0:   G = 0
                if B > 255: B = 255
                if B < 0:   B = 0
                fill_col = (R,G,B)
                surface.set_at((mx,my), fill_col)
                stack += ((mx,my+1), (mx+1,my), (mx,my-1), (mx-1,my))
    #Horizontal Gradient
    elif key.get_pressed()[K_LALT] or key.get_pressed()[K_RALT]:
        boundary_col=surface.get_at((mx,my))    #get the colour that is currently wanting to be changed
        point=mouse.get_pos()          # until the pixels with the same exchange colour have all been changed
        stack.append(point)
        while len(stack)>0:
            mx,my = stack.pop()
            if surface.get_at((mx,my)) == boundary_col and canvas.collidepoint((mx,my)):
                R = round(primeCol[0] * (mx/650) + secCol[0] * ((650-mx)/650))
                G = round(primeCol[1] * (mx/650) + secCol[1] * ((650-mx)/650))
                B = round(primeCol[2] * (mx/650) + secCol[2] * ((650-mx)/650))
                if R > 255: R = 255
                if R < 0:   R = 0
                if G > 255: G = 255
                if G < 0:   G = 0
                if B > 255: B = 255
                if B < 0:   B = 0
                fill_col = (R,G,B)
                surface.set_at((mx,my), fill_col)
                stack += ((mx,my+1), (mx+1,my), (mx,my-1), (mx-1,my))
    #Vertical Gradient
    else:
        boundary_col=surface.get_at((mx,my))    #get the colour that is currently wanting to be changed
        point=mouse.get_pos()          # until the pixels with the same exchange colour have all been changed
        stack.append(point)
        while len(stack)>0:
            mx,my = stack.pop()
            if surface.get_at((mx,my)) == boundary_col and canvas.collidepoint((mx,my)):
                R = round(primeCol[0] * (my/650) + secCol[0] * ((650-my)/650))
                G = round(primeCol[1] * (my/650) + secCol[1] * ((650-my)/650))
                B = round(primeCol[2] * (my/650) + secCol[2] * ((650-my)/650))
                if R > 255: R = 255
                if R < 0:   R = 0
                if G > 255: G = 255
                if G < 0:   G = 0
                if B > 255: B = 255
                if B < 0:   B = 0
                fill_col = (R,G,B)
                surface.set_at((mx,my), fill_col)
                stack += ((mx,my+1), (mx+1,my), (mx,my-1), (mx-1,my))




def moveCanvas(surface, canvas, mx, my):
    copyDrawing = screen.subsurface(canvas).copy()  #remembers the drawing on the canvas
    canvas_x, canvas_y = canvas.x, canvas.y
    offset_x = mx-canvas_x
    offset_y = my-canvas_y

    canvas.move_ip((offset_x,offset_y))
    initiate()  #setups the pygame window again to prevent two canvases in a single window
    surface.blit(copyDrawing, (mx,my))   #190, 165
    #drawSurfaces()  #draws all the tools again
    surface.blit(copyDrawing, (mx,my))

def clearCanvas(surface, canvas):
    draw.rect(surface, (255,255,255), canvas)


def grayScale(surface):
    for x in range(1080):
        for y in range(650):
            pixCol = surface.get_at((100+x, 84+y))
            avg = (pixCol[0]+pixCol[1]+pixCol[2])//3
            surface.set_at((100+x, 84+y), (avg, avg, avg))

def sepia(surface):
    for x in range(1080):
        for y in range(650):
            pixCol = surface.get_at((100+x, 84+y))

            outputRed = (pixCol[0]*.393 + pixCol[1]*.769 + pixCol[2]*.189)
            if outputRed > 255: outputRed = 255

            outputGreen = (pixCol[0]*.349 + pixCol[1]*.686 + pixCol[2]*.168)
            if outputGreen > 255: outputGreen = 255

            outputBlue = (pixCol[0]*.272 + pixCol[1]*.534 + pixCol[2]*.131)
            if outputBlue > 255: outputBlue = 255

            surface.set_at((100+x, 84+y), (outputRed, outputGreen, outputBlue))

def invert(surface):
    for x in range(1080):
        for y in range(650):
            pixCol = surface.get_at((100+x, 84+y))
            invertCol = (255-pixCol[0], 255-pixCol[1], 255-pixCol[2])
            surface.set_at((100+x, 84+y), invertCol)

def pixelate(surface, pixelSize = 5):
    for x in range(1080//pixelSize):
        for y in range(650//pixelSize):
            Col = transform.average_color(surface.subsurface(100+(x*pixelSize),84+(y*pixelSize),pixelSize,pixelSize))
            draw.rect(surface, Col, (100+(x*pixelSize),84+(y*pixelSize),pixelSize,pixelSize))
            #surface.set_at((100+(x*pixelSize), 84+(y*pixelSize)), Col)

def tint(surface, canvas, drawCol, alphaVal = 30):
    tintMask = surface.subsurface(canvas).copy()
    tintMask.fill(drawCol)
    tintMask.set_alpha(alphaVal)
    surface.blit(tintMask, (100,84))

def gaussianBlur(surface, canvas, sigma = 2):   #sigma is the intensity of the blur
    mask = surface.subsurface(canvas).copy()
    np_array = surfarray.array3d(mask)  #converts pygame surface to a numpy array
    result = ndimage.filters.gaussian_filter(np_array, (sigma, sigma, 0))   #filters the image using the builtin module for gaussian blur
    mask = surfarray.make_surface(result)   #converts the numpy array back into a pygame surface
    return mask

def sharpen(surface, canvas):   #sigma is the intensity of the blur
    mask = surface.subsurface(canvas).copy()
    np_array = surfarray.array3d(mask)  #converts pygame surface to a numpy array
    blurred1 = ndimage.filters.gaussian_filter(np_array, (3))   #filters the image using the builtin module for gaussian blur
    filter_blurred1 = ndimage.filters.gaussian_filter(blurred1, (1))   #filters the image using the builtin module for gaussian blur
    alpha = 20
    sharpened = blurred1 + alpha * (blurred1 - filter_blurred1)
    mask = surfarray.make_surface(sharpened)   #converts the numpy array back into a pygame surface
    return mask

def sharpenCol(surface, canvas):   #sigma is the intensity of the blur
    mask = surface.subsurface(canvas).copy()
    np_array = surfarray.array3d(mask)  #converts pygame surface to a numpy array
    blurred1 = ndimage.filters.gaussian_filter(np_array, (3, 3, 0))   #filters the image using the builtin module for gaussian blur
    filter_blurred1 = ndimage.filters.gaussian_filter(blurred1, (1, 1, 0))   #filters the image using the builtin module for gaussian blur
    alpha = 30
    sharpened = blurred1 + alpha * (blurred1 - filter_blurred1)
    mask = surfarray.make_surface(sharpened)   #converts the numpy array back into a pygame surface
    return mask

def sobel(surface, canvas):    #edge detection
    mask = surface.subsurface(canvas).copy()
    np_array = surfarray.array3d(mask)  #converts pygame surface to a numpy array
    result = ndimage.filters.sobel(np_array)   #filters the image using the builtin module for edge detection
    mask = surfarray.make_surface(result)   #converts the numpy array back into a pygame surface
    return mask





