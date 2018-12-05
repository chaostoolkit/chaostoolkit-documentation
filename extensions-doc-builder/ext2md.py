# -*- coding: utf-8 -*-
import importlib
import inspect
import json
from operator import itemgetter
import pkgutil
from typing import Any, Dict, List

from chaoslib.discovery.discover import portable_type_name
from jinja2 import Template
from yapf.yapflib.yapf_api import FormatCode
import yaml

__version__ = '0.1.0'


def get_activity_default_value(arg_type: str) -> str:
    default = None

    if arg_type == "boolean":
        default = True
    elif arg_type == "integer":
        default = 0
    elif arg_type == "float":
        default = 0.0
    elif arg_type == "string":
        default = ""
    elif arg_type == "byte":
        default = b""
    elif arg_type in ("set", "list", "tuple"):
        default = []
    elif arg_type == "mapping":
        default = {}
    elif arg_type == "object":
        default = None

    return default




def import_extension(extension: Dict[str, str]) -> Dict[str, Any]:
    pkg = importlib.import_module(extension["name"])

    try:
        readme = pkgutil.get_data(
            extension["name"], "../README.md").decode('utf-8')
        _, readme = readme.split("\n", 1)
    except FileNotFoundError as x:
        print("Failed to find README in {}: {}".format(
            extension["name"], str(x)))
        readme = "N/A"

    meta = {
        "ext": {
            "name": extension["name"],
            "version": pkg.__version__,
            "repo_url": extension["repo"]
        },
        "readme": readme,
        "activities": {}
    }

    controls = {
        "enabled": False,
        "experiment": {
            "before": False,
            "after": False
        },
        "hypothesis": {
            "before": False,
            "after": False
        },
        "method": {
            "before": False,
            "after": False
        },
        "rollback": {
            "before": False,
            "after": False
        },
        "activity": {
            "before": False,
            "after": False
        }
    }
    meta["controls"] = controls

    walker = pkgutil.walk_packages(
        pkg.__path__, pkg.__name__ + ".")
    for (module_loader, mod_name, ispkg) in walker:
        if mod_name.endswith(".types"):
            continue

        if ispkg:
            continue

        mod = importlib.import_module(mod_name)
        exported = getattr(mod, "__all__", [])
        if not exported:
            continue

        is_control_module = False
        for func_name in exported[:]:
            if func_name in ["configure_control", "cleanup_control"]:
                is_control_module = True
                controls["enabled"] = True
                exported.remove(func_name)
                continue

            if func_name.startswith(("after_", "before_")):
                is_control_module = True
                controls["enabled"] = True
                exported.remove(func_name)
                point, level, _ = func_name.split("_")
                controls[level][point] = True

        if is_control_module:

            controls["as_json"] = json.dumps({
                "name": pkg.__name__,
                "provider": {
                    "type": "python",
                    "module": mod_name
                }
            }, indent=2)
            controls["as_yaml"] = yaml.dump({
                "name": pkg.__name__,
                "provider": {
                    "type": "python",
                    "module": mod_name
                }
            }, default_flow_style=False)
            continue

        activities = []
        target = mod_name.rsplit(".", 2)[1]
        if target not in meta["activities"]:
            meta["activities"][target] = activities
        else:
            activities = meta["activities"][target]

        for func_name in exported:
            activities.append(exported_function_info(mod, mod_name, func_name))
        meta["activities"][target] = sorted(
            activities, key=itemgetter("name"))

    return meta


def exported_function_info(mod, mod_name, func_name) -> Dict[str, Any]:
    func = getattr(mod, func_name)
    sig = inspect.signature(func)

    activity_type = ""
    mod_lastname = mod_name.rsplit(".", 1)[1]
    if mod_lastname == "actions":
        activity_type = "action"
    elif mod_lastname == "probes":
        activity_type = "probe"

    args = build_signature_info(sig)
    return_type = build_return_type_info(sig)
    as_json = called_without_args_info(
        args, mod_name, func_name, activity_type)

    return {
        "type": activity_type,
        "module": mod_name,
        "name": func_name,
        "doc": inspect.getdoc(func),
        "return": return_type,
        "signature": FormatCode("def {}{}:pass".format(
            func_name, str(sig)))[0],
        "arguments": args,
        "as_json": json.dumps(as_json, indent=2),
        "as_yaml": yaml.dump(as_json, default_flow_style=False)
    }


def build_signature_info(sig) -> List[Any]:
    args = []
    for p in sig.parameters.values():
        if p.name in ("secrets", "configuration"):
            continue

        arg = {
            "name": p.name,
            "required": "Yes"
        }

        if p.annotation != inspect.Parameter.empty:
            arg["type"] = portable_type_name(p.annotation)

        if p.default != inspect.Parameter.empty:
            arg["required"] = "No"
            if isinstance(p.default, str):
                arg["default"] = '"{}"'.format(p.default)
            else:
                arg["default"] = json.dumps(p.default)
        args.append(arg)

    return args


def build_return_type_info(sig) -> str:
    return_type = "None"
    if sig.return_annotation != inspect.Signature.empty:
        return_type = portable_type_name(sig.return_annotation)
        if return_type == "object":
            return_type = repr(sig.return_annotation).replace(
                "<class '", "").replace("'>", "").replace(
                    "typing.", "")


def called_without_args_info(args, mod_name, func_name, activity_type):
    can_be_called_without_args = args and not any(
        a["required"] == "Yes" for a in args)

    as_json = {
        "name": func_name.replace('_', '-'),
        "type": activity_type,
        "provider": {
            "type": "python",
            "module": mod_name,
            "func": func_name
        }
    }
    if not can_be_called_without_args:
        if args:
            as_json["provider"]["arguments"] = {}
            for arg in args:
                if arg["required"] == "No":
                    continue

                arg_type = get_activity_default_value(arg["type"])
                as_json["provider"]["arguments"][arg["name"]] = arg_type
    return as_json


def generate(extension: Dict[str, str], template: Template):
    with open(extension["doc_path"], "w") as f:
        meta = import_extension(extension)
        f.write(template.render(**meta))


def run():
    with open("extension.tmpl.md") as f:
        tpl = Template(f.read())

    with open("extensions.json") as f:
        exts = json.load(f)

    for ext in exts:
        generate(ext, tpl)


if __name__ == '__main__':
    run()
