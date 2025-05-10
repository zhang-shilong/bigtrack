#!/usr/bin/env python3

from typing import Optional, Any, List, Dict, Callable, Iterator


class TrackJob:

    def __init__(
            self,
            func: Callable,
            arguments: Dict,
            name: Optional[str] = None,
    ) -> None:

        self.name = name if name is not None else func.__name__
        self.func = func
        self.arguments = arguments

    def __repr__(
            self,
    ) -> str:

        if "input_path" and "output_path" in self.arguments:
            return f"Job {self.name}: {self.arguments['input_path']} -> {self.arguments['output_path']}"
        if "input_path" in self.arguments:
            return f"Job {self.name}: {self.arguments['input_path']}"
        return f"Job {self.name}"

    def __str__(
            self,
    ) -> str:

        return self.__repr__()


class TrackJobGroup:

    def __init__(
            self,
            name: str,
            jobs: Optional[List[TrackJob]] = None,
    ) -> None:

        self.name = name
        self.jobs = jobs if jobs is not None else list()

    def __iter__(
            self,
    ) -> Iterator[TrackJob]:

        return iter(self.jobs)

    def add_job(
            self,
            job: TrackJob,
    ) -> None:

        self.jobs.append(job)

    def execute_job_group(
        self,
    ) -> str:

        for job in self.jobs:
            job.func(**job.arguments)

        return self.name

