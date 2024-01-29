In this repo is the development of a tool called Optimum Render, made to optimize local rendering in Nuke.
The tool builds upon a rough prototype where I offered the option to launch various render instances of a nuke. 
This allows better usage of the threads on light/medium weight scripts and can speed up rendering a lot.
But memory is always an issue with Nuke. On cases where the script is lightweight, you can launch many instances,
but each instance loads things into memory, so in a heavy comp, this will not be helpful and will make your system crash.
So I gave an option to manually adjust instance (and threads) number on a case by case basis.
While this allows optimization, it is a manual process and some may be confused with how to use this properly.

Building upon this idea, Optimum Render will have a proper UI, the rendering instances will be launched as background processes,
as to not open a bunch of terminal windows the compositor has to keep track of.

Upon first render, the first, middle and last frames will be rendered and logged. According to the memory used, the instance/thread
numbers will be adjusted for the rest of the render as to optimize it automatically.
On the following renders, log files of all frames will be analyzed to create a more robust approach to rendering lighter and heavier frames throughout the comp.
You will be able to toggle this off in case you made substantial changes to the script that will make the logs irrelevant.

Information on the renders will be properly displayed so the compositor knows what is going on.
Based upon frame render time the app will estimate how much this would have taken with only one instance normal nuke rendering,
and compare it with the final render time using Optimum Renderer.

This will all run without locking up the GUI, though the cache will be flushed before rendering, to free memory.
If the script is heavy, a warning will pop up advising the compositor to avoid working while rendering.
