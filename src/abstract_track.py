#!/usr/bin/env python3

import os
from typing import Optional, Any, List, Tuple, Dict, TextIO, Callable
from src.utils import *


class AbstractTrack:

    def __init__(
            self,
            identifier: str,
            hub_identifier: str,
            genome_identifier: str,
            **kwargs,
    ) -> None:

        self.identifier = identifier
        self.hub_identifier = hub_identifier
        self.genome_identifier = genome_identifier
        self.kwargs = kwargs
        if "shortLabel" not in self.kwargs:
            self.kwargs["shortLabel"] = self.identifier
        if "longLabel" not in self.kwargs:
            self.kwargs["longLabel"] = self.kwargs["shortLabel"]

        assert "shortLabel" in self.kwargs
        assert "longLabel" in self.kwargs

    def __repr__(
            self,
    ) -> str:

        return f"AbstractTrack(identifier='{self.identifier}')"

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
            other: "AbstractTrack",
    ) -> bool:

        if type(other) != AbstractTrack:
            raise TypeError(f"AbstractTrack expected, got {type(other)}.")

        return hash(self) == hash(other)

    def print(
            self,
            file: Optional[TextIO] = None,
    ) -> None:

        print(f"track {self.identifier}", file=file)
        for key, value in self.kwargs.items():
            print(f"{key} {value}", file=file)

        print("", file=file)

