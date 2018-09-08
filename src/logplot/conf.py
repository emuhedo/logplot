from collections import namedtuple

import yaml


General = namedtuple("General", ["log_open_cmd"])
General.__new__.__defaults__ = (None,) * len(General._fields)

ConfEntry = namedtuple("ConfEntry", ["identifier", "priority", "label"])
ConfEntry.__new__.__defaults__ = (None,)  # label is optional

SpecialConfEntry = namedtuple("SpecialConfEntry", ["identifier", "label", "regex"])
SpecialConfEntry.__new__.__defaults__ = (None,) * len(SpecialConfEntry._fields)

Conf = namedtuple("Conf", ["general", "entries", "special_entries"])


def _loag_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)


def read(default_path, user_path):
    default = _loag_yaml(default_path)
    user = _loag_yaml(user_path)
    # General settings from default and then override by user defined
    general = default.get("general", {})
    general.update(user.get("general", {}))
    general = General(**general)
    # Log entry specific settings only from user
    basics = [ConfEntry(**e) for e in user["entries"]]
    specials = [SpecialConfEntry(**e) for e in user.get("special-entries", [])]
    return Conf(general, basics, specials)
