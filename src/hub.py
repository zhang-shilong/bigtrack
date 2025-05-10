#!/usr/bin/env python3

import os
import sys
from typing import Optional, TextIO
from src.genome import Genome
from src.utils import *


class Hub:

    def __init__(
            self,
            identifier: str,
            **kwargs,
    )-> None:

        self.identifier = identifier
        self.kwargs = kwargs
        self.kwargs["genomesFile"] = "genomes.txt"

        assert "shortLabel" in self.kwargs
        assert "longLabel" in self.kwargs
        assert "genomesFile" in self.kwargs

        self.hub_file = "hub.txt"
        self.genomes = dict()

    def __repr__(
            self,
    ) -> str:

        return f"Hub(identifier='{self.identifier}', shortLabel='{self.kwargs['shortLabel']}', longLabel='{self.kwargs['longLabel']}')"

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
            other: "Hub",
    ) -> bool:

        if type(other) != Hub:
            raise TypeError(f"Hub expected, got {type(other)}.")

        return hash(self) == hash(other)

    def add_genome(
            self,
            genome: Genome,
    ) -> None:

        if genome.identifier not in self.genomes:
            self.genomes[genome.identifier] = genome

    def print(
            self,
            file: Optional[TextIO] = None,
    ) -> None:

        print(f"hub {self.identifier}", file=file)
        for key, value in self.kwargs.items():
            print(f"{key} {value}", file=file)

        print("", file=file)

    def generate(
            self,
            dry_run: bool = False,
    ) -> None:

        hub_file = sys.stdout if dry_run else open(os.path.join(self.identifier, self.hub_file), "w")
        self.print(file=hub_file)
        None if dry_run else hub_file.close()

        if self.genomes:
            genomes_file = sys.stdout if dry_run else open(os.path.join(self.identifier, self.kwargs["genomesFile"]), "w")
            for genome_identifier in self.genomes:
                self.genomes[genome_identifier].print(file=genomes_file)
                self.genomes[genome_identifier].generate(dry_run=dry_run)
            None if dry_run else genomes_file.close()

