# STYLE ***************************************************************************
# content = assignment (Python Advanced)
#
# date    = 2022-01-07
# email   = contact@alexanderrichtertd.com
#**********************************************************************************


def set_color(ctrlList=None, color=None):

    
    color_dict = {
        1: 4,
        2: 13,
        3: 25,
        4: 17,
        5: 17,
        6: 15,
        7: 6,
        8: 16
    }

    for ctrlName in ctrlList:

        try:
            mc.setAttr(ctrlName + 'Shape.overrideEnabled', 1)
        except:
            print("Could not set shape color override")

        try:
            mc.setAttr(ctrlName + 'Shape.overrideColor', color_dict.get(color, 0))

        except:
            print("Could not set color")
    


# EXAMPLE
# set_color(['circle','circle1'], 8)