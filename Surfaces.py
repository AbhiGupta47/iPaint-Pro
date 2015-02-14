from pygame import *
from Functions import *
#-----------------------------LAGOON IMAGES and SURFACES--------------------------------
Lagoon_Bg = transform.scale(image.load('Resources/LagoonBackground.png'), (250,200))


lagoonUP = {
    'Tools' : image.load('Resources/LagoonIcons/Tools.png'), 
    'Brushes' : image.load('Resources/LagoonIcons/Brushes.png'),
    'Shapes' : transform.scale(image.load('Resources/LagoonIcons/Shapes.png'), (31,35)),
    'Edit' : image.load('Resources/LagoonIcons/Edit.png')
    }

lagoonUP2 = {
    'Colour' : image.load('Resources/LagoonIcons/RGB.png'),
    'Stamps' : image.load('Resources/LagoonIcons/Stamps.png'),
    'Filters' : transform.scale(image.load('Resources/LagoonIcons/Filters.png'), (36,32))
}

lagoonPRESSED = {
    'Tools' : image.load('Resources/LagoonIcons/Tools_pressed.png'),
    'Brushes' : image.load('Resources/LagoonIcons/Brushes_pressed.png'),
    'Shapes' : transform.scale(image.load('Resources/LagoonIcons/HighlightedShapes.png'), (31,35)),
    'Edit' : image.load('Resources/LagoonIcons/Edit_pressed.png')
    }

lagoonPRESSED2 = {
    'Colour' : image.load('Resources/LagoonIcons/RGB_pressed.png'),
    'Stamps' : image.load('Resources/LagoonIcons/Stamps_pressed.png'),
    'Filters' : transform.scale(image.load('Resources/LagoonIcons/Filters_pressed.png'), (36,32))
}

lagoonOVER = {
    'Tools' : image.load('Resources/LagoonIcons/Tools_over.png'),
    'Brushes' : image.load('Resources/LagoonIcons/Brushes_over.png'),
    'Shapes' : transform.scale(image.load('Resources/LagoonIcons/HighlightedShapes.png'), (31,35)),
    'Edit' : image.load('Resources/LagoonIcons/Edit_over.png')
    }

lagoonOVER2 = {
    'Colour' : image.load('Resources/LagoonIcons/RGB_over.png'),
    'Stamps' : image.load('Resources/LagoonIcons/Stamps_over.png'),
    'Filters' : transform.scale(image.load('Resources/LagoonIcons/Filters_over.png'), (36,32))
}

blit_locations = {
    'Tools' : (-12,655),
    'Brushes' : (20,661),
    'Shapes' : (69,672),
    'Edit' : (156,776)
    }

blit_locations2 = {
    'Colour' : (92,692),
    'Stamps' : (122,717), ###
    'Filters' : (150,754),
}

group_surfaces = {
    'Tools' : Rect(-12,655,28,32),
    'Brushes' : Rect(20,661,29,33),
    'Shapes' : Rect(69,672,26,26),
    'Edit' : Rect(156,776,31,35)
    }

groups = {
    'Tools' : True,
    'Brushes' : False,
    'Shapes' : False,
    'Edit' : False
    }

group_surfaces2 = {
    'Colour' : Rect(92,692,31,35),
    'Stamps' : Rect(122,717,31,35),
    'Filters' : Rect(150,754,40,38)   
}

groups2 = {
    'Colour' : False,
    'Stamps' : False,
    'Filters' : False
}

#-----------------------------MAC DOCK IMAGES and SURFACES--------------------------------


macDock = {
    'Tools' : image.load('Resources/MacDock_Tools.png'),
    'Brushes' : image.load('Resources/MacDock_Brushes.png'),
    'Shapes' : image.load('Resources/MacDock_Shapes.png'),
    'Edit' : image.load('Resources/MacDock_Edit.png')
    }

DockBasics = {
    'Finder' : False,
    'Launch' : False,
    'iPaintPro' : False,
    'iTunes' : False,
    'Open' : False,
    'Save' : False,
    'AddImg' : False,
    'Clear' : False,
}

DockBasics_surfs = {
    'Finder' : Rect(14,55,28,24),
    'Launch' : Rect(14,92,30,24),
    'iPaintPro' : Rect(18,124,22,32),
    'iTunes' : Rect(13,416,29,29),
    'Open' : Rect(13,450,30,26),
    'Save' : Rect(13,484,30,30),
    'AddImg' : Rect(13,521,30,31),
    'Clear' : Rect(13,583,27,29),
}

Tools = {
    'Pencil' : True,
    'Eraser' : False,
    'Text' : False,
    'Fill' : False,
    'GradientFill' : False,
    'Crop' : False,
}

Tools_surfs = {
    'Pencil' : Rect(13,184,30,29),
    'Eraser' : Rect(13,220,30,29),
    'Text' : Rect(13,255,30,26),
    'Fill' : Rect(13,284,30,33),
    'GradientFill' : Rect(13,324,30,29),
    'Crop' : Rect(13,358,30,33),
}

Brushes = {
    'Airbrush' : False,
    'SprayCan' : False,
    'BallpointPen' : False,
    'Marker' : False,
    'PaintBrush' : False,
    'Pencil' : True,
}

Brushes_surfs = {
    'Airbrush' : Rect(13,183,30,33),
    'SprayCan' : Rect(13,220,30,32),
    'BallpointPen' : Rect(13,254,30,32),
    'Marker' : Rect(13,289,30,32),
    'PaintBrush' : Rect(13,324,30,32),
    'Pencil' : Rect(13,358,30,32),
}

Shapes = {
    'Line' : False,
    'FilledLine' : False,
    'SnapLine' : False,
    'Ellipse' : False,
    'FilledEllipse' : False,
    'UnfilledEllipse' : False,
    'Circle' : False,
    'Rect' : True,
    'FilledRect' : False,
    'UnfilledRect' : False,
    'Polygon' : False,
    'FilledPolygon' : False,
    'UnfiiledPolygon' : False,
    'Snap' : False,
    'Filled' : True
}

Shapes_surfs = {
    'Line' : Rect(13,184,30,30),
    'Ellipse' : Rect(13,264,30,35),
    'Rect' : Rect(13,295,28,26),
    'Polygon' : Rect(13,324,30,33),
    'Snap' : Rect(1,221,47,24),
    'Filled' : Rect(1,364,47,24)
}

ToggleShapes = {
    'SnapOnBg' : image.load('Resources/SnapOnBg.png'),
    'SnapOffBg' : image.load('Resources/SnapOffBg.png'),
    'SnapOn' : image.load('Resources/SnapOn.png'),
    'SnapOff' : image.load('Resources/SnapOff.png'),
    'FilledOnBg' : image.load('Resources/FilledOnBg.png'),
    'FilledOffBg' : image.load('Resources/FilledOffBg.png'),
    'FilledOn' : image.load('Resources/FilledOn.png'),
    'FilledOff' : image.load('Resources/FilledOff.png')
}

Edit = {
    'Move' : False,
    'Crop' : False,
    'Copy' : False,
    'Paste' : False,
    'Cut' : False,
    'View' : False
}

Edit_surfs = {
    'Move' : Rect(13,186,30,30),
    'Crop' : Rect(13,222,30,30),
    'Copy' : Rect(13,255,30,32),
    'Paste' : Rect(13,291,30,29),
    'Cut' : Rect(13,325,30,29),
    'View' : Rect(13,358,30,30)
}

ModeID_DockBasics = {
    'iTunes' :  image.load('Resources/ModeID/Cursor.png')
}

ModeID_Tools = {
    #'Cursor' : image.load('Resources/ModeID/Cursor.png'),
    'Pencil' : image.load('Resources/ModeID/Pencil.png'),
    'Eraser' : image.load('Resources/ModeID/Eraser.png'),
    'Text' : image.load('Resources/ModeID/Fill.png'),
    'Fill' : image.load('Resources/ModeID/Fill.png'),
    'GradientFill' : image.load('Resources/ModeID/Fill.png'),
    'Crop' : image.load('Resources/ModeID/Fill.png')
}

ModeID_Brushes = {
    'Airbrush' : image.load('Resources/ModeID/Airbrush.png'),
    'SprayCan' : image.load('Resources/ModeID/SprayCan.png'),
    'BallpointPen' : image.load('Resources/ModeID/BallpointPen.png'),
    'Marker' : image.load('Resources/ModeID/Marker.png'),
    'PaintBrush' : image.load('Resources/ModeID/PaintBrush.png'),
    'Pencil' : image.load('Resources/ModeID/Pencil.png'),
}

ModeID_Shapes = {
    'Line' : image.load('Resources/ModeID/Airbrush.png'),
    'Ellipse' : image.load('Resources/ModeID/SprayCan.png'),
    'Rect' : image.load('Resources/ModeID/BallpointPen.png'),
    'Polygon' : image.load('Resources/ModeID/PaintBrush.png'),
}

ModeID_Edit = {
    'Move' : image.load('Resources/ModeID/Airbrush.png'),
    'Crop' : image.load('Resources/ModeID/SprayCan.png'),
    'Copy' : image.load('Resources/ModeID/BallpointPen.png'),
    'Paste' : image.load('Resources/ModeID/Marker.png'),
    'Cut' : image.load('Resources/ModeID/PaintBrush.png'),
    'View' : image.load('Resources/ModeID/Pencil.png'),
}

#-----------------------------STAMPS--------------------------------

StampsMask = image.load('Resources/SidePanel/stamps_mask.png')

StampsSidePanel = image.load('Resources/SidePanel/Stamps_SidePanel.png')

Stamps = {
    'Apple' : image.load('Resources/Stamps/Apple.png'),
    'AndroidWorker' : image.load('Resources/Stamps/AndroidWorker.png'),
    'MacHDD' : image.load('Resources/Stamps/MacHDD.png'),
    'Xcode' : image.load('Resources/Stamps/Xcode.png'),
    'iCloudDrive' : image.load('Resources/Stamps/iCloudDrive.png'),
    'iPhone6+' : image.load('Resources/Stamps/iPhone6+.png')
}

StampsSP = {
    'Apple' : image.load('Resources/SidePanel/Stamps_Apple.png'),
    'AndroidWorker' : image.load('Resources/SidePanel/Stamps_AndroidWorker.png'),
    'MacHDD' : image.load('Resources/SidePanel/Stamps_MacHDD.png'),
    'Xcode' : image.load('Resources/SidePanel/Stamps_Xcode.png'),
    'iCloudDrive' : image.load('Resources/SidePanel/Stamps_iCloudDrive.png'),
    'iPhone6+' : image.load('Resources/SidePanel/Stamps_iPhone6+.png')
}

Stamps_surfs = {
    'Apple' : Rect(1021,61,249,125),
    'AndroidWorker' : Rect(1021,186,249,150),
    'MacHDD' : Rect(1021,336,249,125),
    'Xcode' : Rect(1021,436,249,125),
    'iCloudDrive' : Rect(1021,561,249,125),
    'iPhone6+' : Rect(1021,686,249,125)
}

#------------------------------FILTERS----------------------------------
FiltersSidePanel = image.load('Resources/SidePanel/Filters_SidePanel.png')
FiltersSidePanel2 = image.load('Resources/SidePanel/Filters_SidePanel2.png')

Filters_surfs = {
    'GrayScale' : Rect(1039,72,217,128),
    'Sepia' : Rect(1039,222,217,128),
    'Invert' : Rect(1039,372,217,128),
    'Pixelate' : Rect(1039,519,217,128),
    'Tint' : Rect(1039,669,217,128),
    'Blur' : Rect(1039,72,217,128),
    'Sharpen' : Rect(1039,222,217,128),
    'SharpenCol' : Rect(1039,372,217,128),
    'Sobel' : Rect(1039,519,217,128)
}

Filters = {
    'GrayScale' : False,
    'Sepia' : False,
    'Invert' : False,
    'Pixelate' : False,
    'Tint' : False,
    'Blur' : False,
    'Sharpen' : False,
    'SharpenCol' : False,
    'Sobel' : False
}


#------------------------------FILTERS----------------------------------

#------------------------------COLOUR WHEEL----------------------------------

puckLarge = image.load("Resources/colourPucknoShadow.png")
puckSmall = transform.scale(image.load("Resources/colourPucknoShadow.png"), (70,70))

col_images = {
    'colPalette' : image.load('Resources/colourPalette.png'),
    'shadePalette' : image.load("Resources/colourPaletteDiamond.png"),
    'shadePaletteCollide' : image.load('Resources/colourPaletteDiamond_collide.png'),
    'hue' : image.load("Resources/colourPaletteHue.png")
}

col_surfaces = {
    'colPalette' : (1067,2),
    'shadePalette' : Rect(1068,2.85,69,89),
    'hue' : (1067,2),
    'polygon' : ((1142.75,56), (1174,88.5), (1142.75,121), (1110,88.5))
}

#------------------------------EDIT LICENSE----------------------------------
license = image.load('Resources/Edit_License.png')

OK = False
MoreInfo = False

OKsurf = Rect(751,368,77,20)
MoreInfoSurf = Rect(623,368,113,18)


#------------------------------INFO BAR----------------------------------

XY = transform.scale(image.load('Resources/XY.png'), (20,20))
ShapeSize = transform.scale(image.load('Resources/ShapeSize.png'), (20,20))
CanvasSize = transform.scale(image.load('Resources/CanvasSize.png'), (30,28))
#FPS = transform.scale(image.load('Resources/FPS.png'), (22,24))
FPS = image.load('Resources/FPS.png')

#------------------------------SONGS----------------------------------

Songs = ['Resources/iTunes/Songs/BestDayofMyLife.mp3', 'Resources/iTunes/Songs/Radioactive.mp3', 'Resources/iTunes/Songs/Sidewinder.mp3', 'Resources/iTunes/Songs/test.mp3', 
'Resources/iTunes/Songs/Mars.mp3', 'Resources/iTunes/Songs/TooClose.mp3', 'Resources/iTunes/Songs/ButterfliesandHurricanes.mp3']

