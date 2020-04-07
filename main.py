#!/usr/bin/env python3

import json
import pkgutil
import importlib


def json_save(filepath, dat):
    with open(filepath, 'w') as f:
        json.dump(dat, f)


def json_load(filepath):
    dat = {}
    with open(filepath) as f:
        dat = json.load(f)
    return dat


def load_configure():
    cfg = 'coderband.cfg'
    return json_load(cfg)


def init_ui():
    print("TODO: Init UI!!!")


def init_cmd():
    print("TODO: Init CMD!!!")


def init_web():
    print("TODO: Init WEB!!!")


def get_options():
    print("TODO: get options!!!")


def process(cfg, cls):
    obj = cls(cfg)
    # step 6: analysis
    obj.analysis()
    obj.composer()


def output():
    pass


def load_modules(modspath, modsmap):
    pkgs = pkgutil.walk_packages(path=[modspath])
    for pkg in pkgs:
        spec = importlib.util.spec_from_file_location(pkg.name, \
                                                      "{}/{}.py".format(pkg.module_finder.path, pkg.name))
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        m.register_module(modsmap)


if __name__ == "__main__":
    styles = {}
    instruments = {}
    # step 1: load components
    load_modules('styles', styles)
    load_modules('instruments', instruments)
    # step 2: get options from command line
    get_options()
    # step 3: startup user interface
    init_ui()
    init_cmd()
    init_web()
    # step 4: load default configure file
    cfg = load_configure()
    cls = styles.get(cfg['style'])
    if not cls:
        print("Unkown style {}!!!".format(cfg['style']))
        raise SystemExit
    # step 5: process settings
    process(cfg, cls)
    # step 6: converter
    output()
