# framecurve in nuke python
# for more info, see http://framecurve.org
# Framecurve scripts are subject to MIT license
# http://framecurve.org/scripts/#license

from __future__ import with_statement
import nuke, nukescripts, os, re
import framecurve

# On the current node, add a userknob for the framecurve
def add_framecurve(onNode):
    if "framecurve" in onNode.knobs():
        return
    
    framecurveKnob = nuke.Double_Knob("framecurve",  "timewarp frame")
    framecurveKnob.setTooltip( "This contains the retiming framecurve animation")
    onNode.addKnob(framecurveKnob)
    onNode["framecurve"].setAnimated()
    onNode["framecurve"].setValueAt(1.0, 1)
    apply_timewarps_to_knobs(onNode)
    onNode["label"].setValue("TW to [value framecurve]")
    
# TODO: We want our retime knob to appear in a separate tab
def organize_retime_tab(onNode):
    pass
    
# This fails on Nuke < 6.3 but there ain't much we can do
def make_keyframes_linear(knob):
    for curve in knob.animations():
        for key in curve.keys():
            key.interpolation = nuke.LINEAR

def animate_framecurve_from_file(fc_path, to_node):
    with open(fc_path) as fc_file:
        # Validate the framecurve first
        curve = framecurve.parse(fc_file)
        load_curve_into_knob(curve, to_node["framecurve"])

def apply_timewarps_to_knobs(inNode):
    """
    Walks all the knobs in the passed node and changes them to be retimed
    with the framecurve value
    """
    for knob_name in inNode.knobs():
        if knob_name == "framecurve":
            pass
        else:
            k = inNode.knob(knob_name)
            if k.visible() and k.isAnimated():
                # Apply the magic framecurve expr!
                k.setExpression("curve(framecurve(frame))")

def apply_framecurve(toNode, framecurve_path):
    if not "framecurve" in toNode.knobs():
        add_framecurve(toNode)
        organize_retime_tab(toNode)
    # Apply the file at path
    animate_framecurve_from_file(framecurve_path, toNode)

def grab_file():
    return nuke.getFilename("Select the framecurve file", "*.framecurve.txt", default="/", favorites="", type="", multiple=False)

def apply_framecurve_from_selected_files_to_selected_nodes():
    # Load the animation
    framecurve_path = grab_file()
    selected = filter(lambda n: n.Class() != "Viewer" and n.name() != "VIEWER_INPUT", nuke.selectedNodes())
    for n in selected:
        apply_framecurve(n, framecurve_path)

def load_curve_into_knob(framecurve, knob):
    """
    Load a passed framecurve.Curve object into the passed Knob object, resetting
    all the animations
    """
    knob.clearAnimated()
    knob.setAnimated()
    for correlation in framecurve.frames():
        knob.setValueAt(correlation.value, correlation.at) #, index=1, view=1)
    make_keyframes_linear(knob)
    
def load_framecurve_into_focused_knob():
    """
    Can be used as a callback on an animated knob in the Animation menu. It will replace
    the animation in the currently selected knob's curve with a curve loaded from Framecurve
    """
    # Load the framecurve into tuples
    framecurve_path = grab_file()
    if framecurve_path == None:
        return
    
    with open(framecurve_path) as fc_file:
        curve = framecurve.parse(fc_file)
        knob_names = nuke.animations() # Returns the animations names under this knob
        for knob_name_with_suffix in knob_names:
            # Since the names are like "translate.x" what we gotta do is to chop off the suffix
            knob_name = knob_name_with_suffix.split(".")[0]
            # so that we can get at the knob object and do...
            k = nuke.thisNode()[knob_name]
            load_curve_into_knob(curve, k)

def all_script_frames():
    from_f = nuke.root()["first_frame"].getValue()
    to_f = nuke.root()["last_frame"].getValue()
    return xrange(int(from_f), int(to_f) + 1)

def export_framecurve_from_this_knob():
    fc_path = nuke.getFilename("Name the framecurve file to write to", "*.framecurve.txt", default="shot.framecurve.txt", favorites="", type="", multiple=False)
    fc = framecurve.Curve()
    
    curve_name_with_suffix = nuke.animations()[0]
    knob_name = curve_name_with_suffix.split(".")[0]
    this_knob = nuke.thisNode()[knob_name]
    with open(fc_path, "w") as fc_file:
        for curve in nuke.animations():
            for frame in all_script_frames():
                fc.append(framecurve.FrameCorrelation(at=frame, value=this_knob.getValueAt(frame)))
            framecurve.serialize(fc_file, fc)
                  
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

mydir = os.path.dirname(os.path.abspath(__file__))

if nuke.GUI:
    tb = nuke.toolbar("Nodes").addMenu('Framecurve', icon = os.path.join(mydir, "images", "icon.png"))
    
    tb.addCommand('Load a framecurve from file and apply to selected node', apply_framecurve_from_selected_files_to_selected_nodes)
    tb.addCommand('Add retime to the selected node', lambda: add_framecurve(nuke.selectedNode()))
    
    anim = nuke.menu("Animation").addMenu("Framecurve")
    anim.addCommand("Load into this knob", func_shorthand(load_framecurve_into_focused_knob))
    anim.addCommand("Export from this knob", func_shorthand(export_framecurve_from_this_knob))
    