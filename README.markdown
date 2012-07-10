# Framecurve Nuke module

First of all, you will need our python script. [Download the .py](framecurve_nuke/raw/master/scripts/applyFramecurve.py)

Add it to your Nuke's `menu.py` script using import, like so:

	sys.path.append("/path/to/the/directory/where/framecurve_nuke/is/in")
	import framecurve_nuke

## Basic commands

This will create a Framecurve menu in your Nodes toolbar, and add a couple of commands to the Animation callback.

![Framecurve toolbar](framecurve_nuke/raw/master/images/nuke_fc_toolbar.png)

Select a node in Nuke, and pick **Load a framecurve from file and apply to selected node**
A dialog will pop out prompting you to select your framecurve file.

![Framecurve file selector](framecurve_nuke/raw/master/images/nuke_fc_selectfile.png)

After the file is chosen the module will create a knob called **framecurve** in your node, and populate it with
keyframes from the framecurve file.

![Framecurve knob with animation](framecurve_nuke/raw/master/images/nuke_fc_knob.png)

It will then walk all of your knobs in the node, and for each animated knob it will apply a timewarp expression which looks like this:

![Retiming expression](framecurve_nuke/raw/master/images/nuke_fc_expressions.png)

...and every animation in your node will become Framecurve-enabled. 

You can also copy-paste the framecurve animation into another node as desired.

If you only want to setup your node to handle the timewarp without loading any files, use **Add retime to the selected node.**

## Exporting animations

If you want to export a Framecurve file from an arbitrary knob, right-click on that knob and use the **Framecurve** menu.

![Knob menu](framecurve_nuke/raw/master/images/nuke_fc_anim_menu.png)

## The Python module

These scripts use the [framecurve_python](http://github.com/guerilla-di/framecurve_python) library by Ben Dickson.
That library is truly awesome and if you want to do anything sophisticated related to Framecurves we suggest you check it out.

## License

The scripts here are covered with [framecurve license](http://framecurve.org/scripts/#license).