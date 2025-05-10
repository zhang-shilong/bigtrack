#!/usr/bin/env python3

import os
import sys
from typing import Optional, Any, List, Tuple, Dict, TextIO, Callable
from src.group import Group
from src.track import Track
from src.track_job import TrackJob, TrackJobGroup
from src.utils import *
from src.wrappers import *


class Genome:

    def __init__(
            self,
            identifier: str,
            hub_identifier: str,
            path: str,
            **kwargs,
    ) -> None:

        self.identifier = identifier
        self.hub_identifier = hub_identifier
        self.path = os.path.realpath(os.path.expanduser(path))
        self.kwargs = kwargs
        self.kwargs["trackDb"] = os.path.join(self.identifier, "trackDb.txt")
        self.kwargs["groups"] = os.path.join(self.identifier, "groups.txt")
        self.kwargs["twoBitPath"] = os.path.join(self.identifier, "genome.2bit")
        self.two_bit_path = os.path.join(self.hub_identifier, self.identifier, "genome.2bit")
        self.sizes_path = os.path.join(self.hub_identifier, self.identifier, "genome.sizes")
        # Parameters in kwargs will be written to `genomes.txt`, while parameters in self represent paths relative to the working directory

        assert "trackDb" in self.kwargs
        assert "groups" in self.kwargs
        assert "twoBitPath" in self.kwargs
        assert "organism" in self.kwargs
        assert "scientificName" in self.kwargs

        self.groups = dict()

    def __repr__(
            self,
    ) -> str:

        return f"Genome(identifier='{self.identifier}')"

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
            other: "Genome",
    ) -> bool:

        if type(other) != Genome:
            raise TypeError(f"Genome expected, got {type(other)}.")

        return hash(self) == hash(other)

    def add_group(
            self,
            group: Group,
    ) -> None:

        if group.identifier not in self.groups:
            self.groups[group.identifier] = group

    def fetch_jobs(
            self,
            group: str,
    ) -> TrackJobGroup:

        job_group = TrackJobGroup(name=group)

        if self.path.lower().endswith((".2bit", ".twobit")):
            job_group.add_job(TrackJob(
                func=make_symlink,
                arguments={"input_path": self.path, "output_path": self.two_bit_path},
            ))
        else:
            job_group.add_job(TrackJob(
                func=fa_to_two_bit,
                arguments={"input_path": self.path, "output_path": self.two_bit_path},
            ))

        job_group.add_job(TrackJob(
            func=two_bit_info,
            arguments={"input_path": self.two_bit_path, "sizes_path": self.sizes_path},
        ))

        return job_group

    def print(
            self,
            file: Optional[TextIO] = None,
    ) -> None:

        print(f"genome {self.identifier}", file=file)
        for key, value in self.kwargs.items():
            print(f"{key} {value}", file=file)

        print("", file=file)

    def generate(
            self,
            dry_run: bool = False,
    ) -> None:

        if self.groups:
            groups_file = sys.stdout if dry_run else open(os.path.join(self.hub_identifier, self.kwargs["groups"]), "w")
            tracks_file = sys.stdout if dry_run else open(os.path.join(self.hub_identifier, self.kwargs["trackDb"]), "w")
            for group_identifier in self.groups:
                self.groups[group_identifier].print(file=groups_file)
                for track_identifier in self.groups[group_identifier].tracks:
                    self.groups[group_identifier].tracks[track_identifier].print(file=tracks_file)
            None if dry_run else groups_file.close()
            None if dry_run else tracks_file.close()

