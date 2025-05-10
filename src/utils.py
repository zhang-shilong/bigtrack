#!/usr/bin/env python3

import os
import re
from typing import Optional, Any, List, Tuple, Dict, Callable, TextIO


def print_ascii_art(
        file: Optional[TextIO] = None,
) -> None:

    print(r"         ________  ___  ________ _________  ________  ________  ________  ___  __        ", file=file)
    print(r"        |\   __  \|\  \|\   ____\\___   ___\\   __  \|\   __  \|\   ____\|\  \|\  \      ", file=file)
    print(r"        \ \  \|\ /\ \  \ \  \___\|___ \  \_\ \  \|\  \ \  \|\  \ \  \___|\ \  \/  /|_    ", file=file)
    print(r"         \ \   __  \ \  \ \  \  ___  \ \  \ \ \   _  _\ \   __  \ \  \    \ \   ___  \   ", file=file)
    print(r"          \ \  \|\  \ \  \ \  \|\  \  \ \  \ \ \  \\  \\ \  \ \  \ \  \____\ \  \\ \  \  ", file=file)
    print(r"           \ \_______\ \__\ \_______\  \ \__\ \ \__\\ _\\ \__\ \__\ \_______\ \__\\ \__\ ", file=file)
    print(r"            \|_______|\|__|\|_______|   \|__|  \|__|\|__|\|__|\|__|\|_______|\|__| \|__| ", file=file)
    print("", file=file)
    print("", file=file)


def prepend_to_path(
        new_path: str,
) -> None:

    new_path = os.path.abspath(new_path)
    current_path = os.environ.get("PATH", "")
    path_list = current_path.split(os.pathsep)
    if new_path not in path_list:
        path_list.insert(0, new_path)
    os.environ["PATH"] = os.pathsep.join(path_list)


def extract_public_attrs(
        attrs: Dict[str, Any],
) -> Dict[str, Any]:

    public_attrs = dict()
    for key, value in attrs.items():
        if not key.startswith("_"):
            public_attrs[key] = value

    return public_attrs


def verify_str(
        original: str,
) -> str:

    cleaned = re.sub(r"[^\w\-.]", "_", original)
    cleaned = re.sub(r"_+", "_", cleaned)
    cleaned = cleaned.strip("-_.")

    return cleaned


def get_suffix(
        path: str,
) -> str:

    COMPRESSED_EXTS = {"gz", "bz2", "zip", "xz"}

    basename = os.path.basename(path)
    name_parts = list()

    while True:
        basename, ext = os.path.splitext(basename)
        if not ext:
            break
        name_parts.append(ext.lower().lstrip("."))

    name_parts = name_parts[::-1]

    if len(name_parts) >= 1 and name_parts[0] in COMPRESSED_EXTS:
        if len(name_parts) >= 2:
            return f"{name_parts[1]}.{name_parts[0]}"
        return name_parts[0]

    return name_parts[0] if name_parts else ""


def find_as(
        path: Optional[str],
) -> Optional[str]:

    if path is None:
        return None

    if os.path.exists(path):
        return os.path.abspath(path)

    as_path = os.path.join(AS_DIR, path)
    if os.path.exists(as_path) and os.path.isfile(as_path):
        return as_path

