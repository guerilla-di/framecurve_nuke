# Framecurve Nuke module

First of all, you will need our python script. [Download the .py](framecurve_nuke/raw/master/scripts/applyFramecurve.py)

Select a node in Nuke, execute the script function **apply_framecurve_from_file()**
A dialog will pop out prompting you to select your framecurve file.

![Framecurve file selector](framecurve_nuke/raw/master/images/nuke_fc_selectfile.png)

After the file is chosen the module will create a knob called **framecurve** in your node, and populate it with
keyframes from the framecurve file.

![Framecurve knob with animation](framecurve_nuke/raw/master/images/nuke_fc_knob.png)

It will then walk all of your knobs in the node, and for each animated knob it will apply a timewarp expression which looks like this:

![Retiming expression](framecurve_nuke/raw/master/images/nuke_fc_expressions.png)

...and every animation in your node will become Framecurve-enabled. 
You can also copy-paste the framecurve animation into another node as desired.

## License

The scripts here are covered with [framecurve license](http://framecurve.org/scripts/#license).