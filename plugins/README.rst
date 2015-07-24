
How To write a plugin
=====================

Functions
---------

A plugin must have a function named `do`.
The do function must take 2 parameters: The class instance (self) and command line input as a string.

The do function must return nothing.  (PS: Return True is a Quit at present.)

Help
----

The doc string of the do function will be used as the help message for the plugin.
If a function named help exist in the plugin that will be called to print the help.

The help function must print the help and return nothing.

Autocomplete
------------

Not yet implemented. 

Rules
-----

KATTUI = True                                                                                                                        
KATTUI_DENY = {'site': ['karoo', 'vkaroo']}                                                                                          
KATTUI_ALLOW = {'nodetype': ['head']}                                                                                                

Where
-----

Copy your plugin into `/usr/local/lib/kattui`

Debug
-----

Call `kat` with the `plugin` argument to see details of the various plugins.

::
    kat plugin
