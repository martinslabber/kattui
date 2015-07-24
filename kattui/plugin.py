import os
import imp
import glob
import json


PLUGIN_PATH = '/usr/local/lib/kattui'


def allowed_to_run_on_this_node(mod, node_conf):
    """
    """
    allowed = True
    plugin_allow_rule = getattr(mod, 'KATTUI_ALLOW', {})
    plugin_deny_rule = getattr(mod, 'KATTUI_DENY', {})

    # Validate the ALLOW rules
    if plugin_allow_rule:
        for key, options in plugin_allow_rule.items():
            this = node_conf.get(key)
            if this:
                if this not in options:
                    return ('not allowed {} {} because is not in {}'.
                            format(key, this, options))
            else:
                return ('no key {}'.format(key))

    # Validate the DENY rules
    if plugin_deny_rule:
        for key, options in plugin_deny_rule.items():
            this = node_conf.get(key)
            if this:
                if this in options:
                    return ('deny {} {} because it is in {}'.
                            format(key, this, options))
            else:
                return ('no key {}'.format(key))
    return allowed


def add_method_to_class(src_module, module_name, function_name, dst_class):
    """Take a function from a module and make it a method on a class. The
    function must have a self to work properly.

    Parameters
    ----------
    src_module: python module
        The module that has the needed function
    function_name: str
        The name of the function to link.
    dst_class: class
        The class (not an instance) the function will be linked to.
    """
    func = getattr(src_module, function_name, None)
    if not func:
        return
    if hasattr(dst_class, function_name):
        return
    setattr(dst_class, function_name + '_' + module_name, func)


def load_plugins(app, node_conf):
    """Load plugins for kat tui and attach them to the app.

    A Plugin is a python file in the PLUGIN_PATH that has
    a variable KATTUI set to True. Functions from the package that fatch the
    filename is linked into the CMD class. Its hard to explain read the code.

    Parameters
    ----------
    app: Class
        A class we will extend with plugins.
    """

    # Loop through all python files in the PLUGIN_PATH
    for filename in glob.glob1(PLUGIN_PATH, '*.py'):
        mod_name = filename.split(".", 1)[0]
        mod = imp.load_source(mod_name, os.path.join(PLUGIN_PATH, filename))
        if getattr(mod, 'KATTUI', False):
            # Use only files that has KATTUI set to True
            if allowed_to_run_on_this_node(mod, node_conf) is True:
                add_method_to_class(mod, mod_name, 'do', app)
                add_method_to_class(mod, mod_name, 'help', app)

    return app()


def load_node_conf():

    node_conf = {}
    if os.path.isfile('/var/kat/node.conf'):
        with open('/var/kat/node.conf') as fh:
            node_conf = json.loads(fh.read())
    return node_conf


def connect_plugin(line):
    node_conf = load_node_conf()
    if not node_conf:
        print("Could not load node.conf")
    else:
        print("Value of node.conf:")
        for key, value in node_conf.items():
            print("\t{}: {}".format(key, value))

    print('')
    for filename in glob.glob1(PLUGIN_PATH, '*.py'):
        mod_name = filename.split(".", 1)[0]
        mod = imp.load_source(mod_name, os.path.join(PLUGIN_PATH, filename))
        kattui_enabled = getattr(mod, 'KATTUI', False)
        if kattui_enabled:
            print("File {} as module {}:".format(filename, mod_name))
            # Use only files that has KATTUI set to True
            allowed = allowed_to_run_on_this_node(mod, node_conf)
            if allowed is True:
                method = 'do_' + mod_name
                if hasattr(mod, 'do'):
                    print("\t. Can load: {}".format(method))
                else:
                    print("\t! Can not load: {}".format(method))
                method = 'help_' + mod_name
                if hasattr(mod, 'help'):
                    print("\t. Can load: {}".format(method))
            else:
                print("\tCannot load: {}".format(allowed))
        else:
            print("File {} as module {} has no KATTUI or KATTUI is set "
                  "to false".format(filename, mod_name))
