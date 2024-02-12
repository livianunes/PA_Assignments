import nuke

def readFromWrite():


    #variables
    ntn = nuke.thisNode()
    g = nuke.thisGroup()
    g.begin()
    writeNode = nuke.toNode('_Write')
    g.end()
    path = writeNode.knob('file').value()
    colorspace = writeNode.knob('colorspace').value()
    rootPath = nuke.root()

    #frame range
    first = nuke.root().firstFrame()
    last = nuke.root().lastFrame()



    #get connected nodes
    try:
        connectedTo = ntn.dependent()
        connectedTo = connectedTo[0].name()
        connectedTo = nuke.toNode(connectedTo)
    except:
        pass

    #CREATE THE READ NODE
    read = nuke.createNode('Read')

    #movs or images without padding
    if path.find('%04d') == -1:

        first = 1
        last = 1
        read.knob('frame').setValue('1001')


    read['file'].setValue(path)
    read['colorspace'].setValue(colorspace)
    read['first'].setValue(first)
    read['last'].setValue(last)
    read['origfirst'].setValue(first)
    read['origlast'].setValue(last)
    read['on_error'].setValue(1)


    nuke.nodeCopy('%clipboard%')
    nuke.nodeDelete()

    rootPath.begin()
    ntn.knob('selected').setValue(True)
    xpos = ntn.xpos()
    ypos = ntn.ypos()
    pastedRead = nuke.nodePaste('%clipboard%')
    pastedRead.setXpos(xpos)
    pastedRead.setYpos(ypos + 250)

    presetK = ntn.knob('presets')
        
    pastedReadName = pastedRead.knob('name').value()
    pastedReadName = nuke.toNode(pastedReadName)
    pastedReadName.knob('selected').setValue(True)

    #create backdrop


    selNodes = nuke.selectedNodes()
    if not selNodes:
        n = nuke.createNode("BackdropNode", inpanel=False)
        return

    # Calculate bounds for the backdrop node.
    bdX = min([node.xpos() for node in selNodes])
    bdY = min([node.ypos() for node in selNodes])
    bdW = max([node.xpos() + node.screenWidth() for node in selNodes]) - bdX
    bdH = max([node.ypos() + node.screenHeight() for node in selNodes]) - bdY

    # Expand the bounds to leave a little border. Elements are offsets for left, top, right and bottom edges respectively

    if presetK.value() == "Final_Render_EXR" or presetK.value() == "Final_Render_EXR_Multichannel" or presetK.value() == "Dailies" or presetK.value() == "Web" or presetK.value() == "Export_to_DMP" or presetK.value() == "Mask" or presetK.value() == "Jpeg":
        left, top, right, bottom = (-100, -150, 100, 150)
    else:
        left, top, right, bottom = (-300, -160, 90, 130)
    bdX += left
    bdY += top
    bdW += (right - left)
    bdH += (bottom - top)

    n = nuke.createNode("BackdropNode", inpanel=False)
    n["xpos"].setValue(bdX)
    n["bdwidth"].setValue(bdW)
    n["ypos"].setValue(bdY)
    n["bdheight"].setValue(bdH)

    backdrop = n.knob('name').value()

    import colorsys

    # Backdrop presets
    ColorDMP = colorsys.hsv_to_rgb(0.72, 0.31, 0.278)
    ColorDenoise = colorsys.hsv_to_rgb(0.37, 0.475, 0.2)
    ColorOthers = colorsys.hsv_to_rgb(0.72, 0.0, 0.278)
    ColorCleanUp = colorsys.hsv_to_rgb(0.145, 0.31, 0.278)
    ColorKeying = colorsys.hsv_to_rgb(0.42, 0.31, 0.278)
    ColorRender = colorsys.hsv_to_rgb(0, 0.31, 0.278)
    ColorCG = colorsys.hsv_to_rgb(0.57, 0.31, 0.278)
    ColorWeb = colorsys.hsv_to_rgb(0, 0.455, 0.165)



    if presetK.value() == "3D_Pass_Merge":
        presetColor = ColorCG

    elif presetK.value() == "Cleanup":
        presetColor = ColorCleanUp

    elif presetK.value() == "Denoise":
        presetColor = ColorDenoise


    elif presetK.value() == "DMP_to_EXR":
        presetColor = ColorDMP


    elif presetK.value() == "Keying":
        presetColor = ColorKeying


    elif presetK.value() == "Final_Render_EXR" or presetK.value() == "Final_Render_EXR_Multichannel":
        presetColor = ColorRender


    elif presetK.value() == "Web":
        presetColor = ColorWeb


    elif presetK.value() == "Dailies":
        presetColor = ColorWeb

    else:
        presetColor = ColorOthers

    Presettype = presetK.value()

    customtag = ntn.knob('customtag').value()

    if presetK.value() == "Custom":
        Presettype = ntn.knob('customName').value()
    else:
        pass


    # Float R, G, and B values for the color you're after
    r = presetColor[0]
    g = presetColor[1]
    b = presetColor[2]
    hexColour = int('%02x%02x%02x%02x' % (r*255,g*255,b*255,1), 16)

    nuke.toNode(backdrop)['tile_color'].setValue(hexColour)
    nuke.toNode(backdrop)['label'].setValue(Presettype+"\n"+customtag)
    nuke.toNode(backdrop)['note_font_size'].setValue(40)
    nuke.toNode(backdrop)['note_font_color'].setValue(0)


    rootPath.end()

readFromWrite()
