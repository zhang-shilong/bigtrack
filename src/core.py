#!/usr/bin/env python3

import os
import json
import tomllib
import multiprocessing
from typing import Optional, Any, List, Tuple, Dict, TextIO, Callable
from tqdm import tqdm
from src.hub import Hub
from src.genome import Genome
from src.group import Group
from src.track import Track
from src.track_job import TrackJob, TrackJobGroup
from src.utils import *


class HubCore:

    def __init__(
            self,
    ) -> None:

        self.info = None
        self.hub: Hub = None
        self.hub_identifier: str = ""
        self.genomes: Dict[str, Genome] = dict()
        self.groups: Dict[str, Group] = dict()
        self.tracks: Dict[str, Track] = dict()
        self.job_groups: List[JobGroup] = list()

    def parse_configuration_file(
            self,
            config_path: str,
    ) -> None:

        config_suffix = get_suffix(config_path).lower()

        if config_suffix == "toml":
            with open(config_path, "rb") as f:
                self.info = tomllib.load(f)

        elif config_suffix == "json":
            with open(config_path, "r") as f:
                self.info = json.load(f)

        else:
            raise ValueError(f"Only TOML and JSON supported: {config_path}.")

    def build_hub(
            self,
            force_overwrite: bool = False,
    ) -> None:

        # parse hub
        assert len(self.info["hub"]) == 1
        self.hub_identifier = list(self.info["hub"])[0]
        self.hub = Hub(identifier=self.hub_identifier, **extract_public_attrs(self.info["hub"][self.hub_identifier]))

        # check directory
        if os.path.exists(self.hub_identifier) and not force_overwrite:
            raise FileExistsError(f"{self.hub_identifier} already exists.")
        os.makedirs(self.hub_identifier, exist_ok=True)

        # parse genomes
        for genome_identifier in self.info["genomes"]:
            self.genomes[genome_identifier] = Genome(identifier=genome_identifier, hub_identifier=self.hub_identifier, path=self.info["genomes"][genome_identifier]["_path"], **extract_public_attrs(self.info["genomes"][genome_identifier]))
            os.makedirs(os.path.join(self.hub_identifier, genome_identifier), exist_ok=True)

        # link hub and genomes
        if "_genomes" in self.info["hub"][self.hub_identifier]:
            for genome_identifier in self.info["hub"][self.hub_identifier]["_genomes"]:
                self.hub.add_genome(self.genomes[genome_identifier])
        for genome_identifier in self.info["genomes"]:
            if "_hub" in self.info["genomes"][genome_identifier]:
                self.hub.add_genome(self.genomes[genome_identifier])

        # parse groups
        for group_identifier in self.info["groups"]:
            self.groups[group_identifier] = Group(identifier=group_identifier, **extract_public_attrs(self.info["groups"][group_identifier]))

        # link genomes and groups
        for genome_identifier in self.info["genomes"]:
            if "_groups" in self.info["genomes"][genome_identifier]:
                for group_identifier in self.info["genomes"][genome_identifier]["_groups"]:
                    self.genomes[genome_identifier].add_group(self.groups[group_identifier])
        for group_identifier in self.info["groups"]:
            if "_genome" in self.info["groups"][group_identifier]:
                self.genomes[self.info["groups"][group_identifier]["_genome"]].add_group(self.groups[group_identifier])

        # parse tracks and link groups and tracks
        for track_identifier in self.info.get("tracks", []):
            track_info = self.info["tracks"][track_identifier]
            group_identifier = track_info["group"]
            genome_identifier = None
            for g in self.genomes:
                if group_identifier in self.genomes[g].groups:
                    genome_identifier = g
            self.tracks[track_identifier] = Track(identifier=track_identifier, hub_identifier=self.hub_identifier, genome_identifier=genome_identifier, path=track_info["_path"], as_path=track_info.get("_as", None), **extract_public_attrs(track_info))
            self.groups[group_identifier].add_track(self.tracks[track_identifier])

    def fetch_jobs(
            self,
    ) -> None:

        self.job_groups = list()  # empty jobs
        job_group_id = 0

        for genome_identifier in self.genomes:
            self.job_groups.append(self.genomes[genome_identifier].fetch_jobs(str(job_group_id)))
            job_group_id += 1
        for track_identifier in self.tracks:
            self.job_groups.append(self.tracks[track_identifier].fetch_jobs(str(job_group_id)))
            job_group_id += 1

    def print_jobs(
            self,
            file: Optional[TextIO] = None,
    ) -> None:

        print("💡 These jobs will be executed:", file=file)
        for job_group in self.job_groups:
            for job in job_group:
                print(f"Group {job_group.name}\t{job}", file=file)
        print(u"\u2500" * os.get_terminal_size().columns, file=file)
        print("", file=file)

    def execute_jobs(
            self,
            threads: int = 1,
    ):

        with multiprocessing.Pool(processes=threads) as pool:
            with tqdm(
                total=len(self.job_groups),
                desc="Processing",
                bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [Elapsed: {elapsed}]",
            ) as pbar:

                results = pool.imap_unordered(_execute_job_group, self.job_groups, chunksize=1)

                for result in results:
                    tqdm.write(f"✅ Finished: Group {result}")
                    pbar.update()

            tqdm.write(f"✅ All jobs are done! Please check your hub at {os.path.realpath(os.path.expanduser(self.hub_identifier))}.")


def _execute_job_group(
        job_group: TrackJobGroup,
) -> List[Any]:
    # for serialization
    return job_group.execute_job_group()
