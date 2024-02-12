# STYLE ***************************************************************************
# content = assignment
#
# date    = 2022-01-07
# email   = contact@alexanderrichtertd.com
#************************************************************************************

# original: logging.init.py

def findCaller(self):
    """
    Find the stack frame of the caller so that we can note the source
    file name, line number and function name.
    """

    # ***********************************************************************************
    # VARIABLES
    # ***********************************************************************************
    frame = currentframe()
    
    # ***********************************************************************************
    # ERROR HANDLING
    # ***********************************************************************************
    
    #On some versions of IronPython, currentframe() returns None if
    #IronPython isn't run with -X:Frames.
    if frame is not None:
        frame = f.f_back

    rv = "(unknown file)", 0, "(unknown function)"


    # ***********************************************************************************
    # MAIN FUNCTIONALITY
    # ***********************************************************************************
    
    while hasattr(frame, "f_code"):

        # Grabs file name ***********************************************************
        co = frame.f_code
        filename = os.path.normcase(co.co_filename)

        # Checks if file name is same as source file **********************************
        if filename == _srcfile:
            frame = frame.f_back
            continue

        # returns file name *********************************************************
        rv = (co.co_filename, f.f_lineno, co.co_name)
        break

    return rv
