# framecurve in nuke python
# for more info, see http://framecurve.org
# Framecurve scripts are subject to MIT license
# http://framecurve.org/scripts/#license

# Unfortunately we CANNOT specify a function callback as something that goes into the Animation menu, we have
# to do it with a function path as a string. This should be filed as a Nuke bug.
# Therefore, we resort to this workaround:
# https://gist.github.com/3010826/8a312c42ff1c343b54450feb6c4c8d169ef3afc7
import inspect
def func_shorthand(symbol):
    """
    Returns the fully qualified function call with it's module so that it can be used in Nuke's menus,
    even if your function is nested 6 levels deep in a module
    func_shorthand(do_this) #=> "some.module.another.do_this()"
    """
    my_module = inspect.getmodule(symbol).__name__
    return '.'.join([my_module, symbol.__name__]) + '()'

# Store the framecurve paths in a separate dir
import fcnuke
mydir = os.path.dirname(os.path.abspath(fcnuke.__file__))

if nuke.GUI:
    tb = nuke.toolbar("Nodes").addMenu('Framecurve', icon = os.path.join(mydir, "images", "icon.png"))
    
    tb.addCommand('Load a framecurve from file and apply to selected node', fcnuke.apply_framecurve_from_selected_files_to_selected_nodes)
    tb.addCommand('Add retime to the selected node', lambda: fcnuke.add_framecurve(nuke.selectedNode()))
    
    anim = nuke.menu("Animation").addMenu("Framecurve")
    anim.addCommand("Load into this knob", func_shorthand(fcnuke.load_framecurve_into_focused_knob))
    anim.addCommand("Export from this knob", func_shorthand(fcnuke.export_framecurve_from_this_knob))
    