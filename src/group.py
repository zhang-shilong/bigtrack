#!/usr/bin/env python3

import os
from typing import Optional, TextIO
from src.track import Track
from src.utils import *


class Group:

    def __init__(
            self,
            identifier: str,
            **kwargs,
    ) -> None:

        self.identifier = identifier
        self.kwargs = kwargs

        assert "label" in self.kwargs

        self.tracks = dict()

    def __repr__(
            self,
    ) -> str:

        return f"Group(identifier='{self.identifier}')"

    def __str__(
            self,
    ) -> str:

        return self.__repr__()

    def __hash__(
            self,
    ) -> int:

        return hash(self.identifier)

    def __eq__(
            self,
            other: "Group",
    ) -> bool:

        if type(other) != Group:
            raise TypeError(f"Group expected, got {type(other)}.")

        return hash(self) == hash(other)

    def add_track(
            self,
            track: Track,
    ) -> None:

        if track.identifier not in self.tracks:
            self.tracks[track.identifier] = track

    def print(
            self,
            file: Optional[TextIO] = None,
    ) -> None:

        print(f"name {self.identifier}", file=file)
        for key, value in self.kwargs.items():
            print(f"{key} {value}", file=file)

        print("", file=file)


