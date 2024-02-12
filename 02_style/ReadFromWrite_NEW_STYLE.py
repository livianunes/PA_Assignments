#********************************************************************
# content = Creates a read node from a custom write node for Nuke.
#
# how to = readFromWrite()
# dependencies = nuke
#
# author = Livia Nunes
#********************************************************************

import colorsys

import nuke


def readFromWrite():

    """ This function creates a read node from a custom write node.
    It sets a backdrop for it with custom colors depending on the preset used on the custom write node
    and the name corresponding for that type of preset.
    It also sets the correct frame range and colorspace.
    """    


    # *******************************************************************************
    # VARIABLES
    # *******************************************************************************

    GROUP = nuke.thisGroup()
    NTN = nuke.thisNode()
    PRESET_KNOB = NTN.knob('presets')

    #get write node inside group
    GROUP.begin()
    WRITE_NODE = nuke.toNode('_Write')
    GROUP.end()

    #get information from write node
    PATH = WRITE_NODE.knob('file').value()
    COLORSPACE = WRITE_NODE.knob('colorspace').value()

    
    #frame range
    firstFrame = nuke.root().firstFrame()
    lastFrame = nuke.root().lastFrame()

    #movs or images without padding

    if PATH.find('%04d') == -1:
        firstFrame = 1
        lastFrame = 1
        no_padding = True
    else:
        no_padding = False

    # *******************************************************************************
    # CREATE THE READ NODE
    # *******************************************************************************
        
    read = nuke.createNode('Read')

    # Configures read node

    if no_padding == True":
        read.knob('frame').setValue('1001')


    read['file'].setValue(PATH)
    read['colorspace'].setValue(COLORSPACE)
    read['first'].setValue(firstFrame)
    read['last'].setValue(lastFrame)
    read['origfirst'].setValue(firstFrame)
    read['origlast'].setValue(lastFrame)
    read['on_error'].setValue(1)

    # *******************************************************************************
    # Copies read node from inside group and extracts it to outside the group
    # *******************************************************************************

    nuke.nodeCopy('%clipboard%')
    nuke.nodeDelete()

    nuke.root().begin()
    NTN.knob('selected').setValue(True)

    #sets proper position in relationship to write node
    xpos = NTN.xpos()
    ypos = NTN.ypos()
    Read_Node = nuke.nodePaste('%clipboard%')
    Read_Node.setXpos(xpos)
    Read_Node.setYpos(ypos + 250)


    # ***********************************************************************************
    # Sets backdrop bounds according to write node preset
    # ***********************************************************************************
    
    #selects Read Node
    Read_Node = Read_Node.knob('name').value()
    Read_Node = nuke.toNode(Read_Node)
    Read_Node.knob('selected').setValue(True)

    #creates backdrop
    selNodes = nuke.selectedNodes()
    backdrop = nuke.createNode("BackdropNode", inpanel=False)

    # Calculate bounds for the backdrop node.
    bdX = min([node.xpos() for node in selNodes])
    bdY = min([node.ypos() for node in selNodes])
    bdW = max([node.xpos() + node.screenWidth() for node in selNodes]) - bdX
    bdH = max([node.ypos() + node.screenHeight() for node in selNodes]) - bdY

    # Expand the bounds to leave a little border. Elements are offsets for left, top, right and bottom edges respectively
    if (PRESET_KNOB.value() == "Final_Render_EXR" or 
        PRESET_KNOB.value() == "Final_Render_EXR_Multichannel" or 
        PRESET_KNOB.value() == "Dailies" or 
        PRESET_KNOB.value() == "Web" or 
        PRESET_KNOB.value() == "Export_to_DMP" or 
        PRESET_KNOB.value() == "Mask" or 
        PRESET_KNOB.value() == "Jpeg"):
        left, top, right, bottom = (-100, -150, 100, 150)
    else:
        left, top, right, bottom = (-300, -160, 90, 130)

    bdX += left
    bdY += top
    bdW += (right - left)
    bdH += (bottom - top)

    backdrop = nuke.createNode("BackdropNode", inpanel=False)
    backdrop["xpos"].setValue(bdX)
    backdrop["bdwidth"].setValue(bdW)
    backdrop["ypos"].setValue(bdY)
    backdrop["bdheight"].setValue(bdH)

    #Gets backdrop name
    backdrop = backdrop.knob('name').value()


    # *******************************************************************************
    # Sets backdrop colors according to write node preset
    # *******************************************************************************

    # Backdrop preset colors
    colorPresets = {
        'Web': colorsys.hsv_to_rgb(0, 0.455, 0.165),
        'Dailies': colorsys.hsv_to_rgb(0, 0.455, 0.165),
        'Keying': colorsys.hsv_to_rgb(0.42, 0.31, 0.278),
        'Denoise': colorsys.hsv_to_rgb(0.37, 0.475, 0.2),
        'Cleanup': colorsys.hsv_to_rgb(0.145, 0.31, 0.278),
        'DMP_to_EXR': colorsys.hsv_to_rgb(0.72, 0.31, 0.278),
        '3D_Pass_Merge': colorsys.hsv_to_rgb(0.57, 0.31, 0.278),
        'Final_Render_EXR': colorsys.hsv_to_rgb(0, 0.31, 0.278),
        'Final_Render_EXR_Multichannel': colorsys.hsv_to_rgb(0, 0.31, 0.278),
      }

    #gets preset name values
    if PRESET_KNOB.value() == "Custom":
        customtag = NTN.knob('customtag').value()
        Preset_Name = NTN.knob('customName').value()
    else:
        customtag = ""
        Preset_Name = PRESET_KNOB.value()

    # Gets color from dictionary and converts to hex colour for Nuke
    presetColor = colorPresets.get(Preset_Name, colorsys.hsv_to_rgb(0.72, 0.0, 0.278))
    r = presetColor[0]
    g = presetColor[1]
    b = presetColor[2]
    hexColour = int('%02x%02x%02x%02x' % (r*255,g*255,b*255,1), 16)

    # *******************************************************************************
    # SET VALUES TO BACKDROP NODE
    # *******************************************************************************
    nuke.toNode(backdrop)['tile_color'].setValue(hexColour)
    nuke.toNode(backdrop)['label'].setValue(Preset_Name+"\n"+customtag)
    nuke.toNode(backdrop)['note_font_size'].setValue(40)
    nuke.toNode(backdrop)['note_font_color'].setValue(0)


    nuke.root().end()


    

# ***********************************************************************************
# EXECUTE
# ***********************************************************************************
readFromWrite()
