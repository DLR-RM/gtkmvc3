In this example, we show how UIManager can be used with multiple
(sub)views. Each view has its own ActionGroups and Actions, and each
controller handles the associated view's signals.

Features:
- subviews, each containing its actions and action groups
- ui manager
- accelerators
- custom toolitem and action

At top level, there is the application, split into tree sub parts
(Part1, Part2 and Part3). There is also a further part to handle menu
and tool bars (Bars)

The Application level constructs the sub parts. The BarsView and
BarsCtrl know all subparts, which make possible to connect them when
creating menu and toolbar with the internal UIManager.

A part from this, all the other parts are independent each other.

Most of the UI stuff is in GtkBuilder files.

Part1 has simply a couple of button actions to control the content of
a buffer. Accelerator F12.

Part2 is much more interesting, as it features a SpinButton
controlling a counter value into the model through an adapter.  This
is very interesting also because the same counter value is controlled
also by a custom Action featuring a SpinButton in the toolbar.

The code for creating custom action is inspired to project Gramps,
which you can see here:
http://gramps.sourcearchive.com/documentation/3.3.1-1/valueaction_8py_source.html

Part3 is simply a ProgressBar moving when corresponding ToggleButton
is switched on. Accelerator CTRL+r

Application has Quit item. Accelerator CTRL+Q.


To run it:
$> pwd
(...)examples/uimanager/subviews

$> python2 main.py
