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
    print("Init UI!!!")


def process(cfg, cls):
    obj = cls(cfg)
    obj.analysis()
    obj.composer()


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
    cfg = load_configure()
    load_modules('styles', styles)
    load_modules('instruments', instruments)
    init_ui()
    cls = styles.get(cfg['style'])
    if not cls:
        print("Unkown style {}!!!".format(cfg['style']))
        raise SystemExit
    process(cfg, cls)
