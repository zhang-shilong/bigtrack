#!/usr/bin/env python3

import os
import re
from typing import Optional, Any, List, Tuple, Dict, Callable
from src.abstract_track import AbstractTrack
from src.track_job import TrackJob, TrackJobGroup
from src.utils import *
from src.wrappers import *


class Track(AbstractTrack):

    def __init__(
            self,
            identifier: str,
            hub_identifier: str,
            genome_identifier: str,
            path: str,
            as_path: Optional[str] = None,
            **kwargs,
    ) -> None:

        super().__init__(identifier=identifier, hub_identifier=hub_identifier, genome_identifier=genome_identifier, **kwargs)
        self.path = os.path.realpath(os.path.expanduser(path))
        self.suffix = get_suffix(self.path).lower()
        self.sizes_path = os.path.join(hub_identifier, genome_identifier, "genome.sizes")
        self.as_path = as_path

        assert "type" in self.kwargs

        if re.match(r"^bigBed", self.kwargs["type"]):
            self.kwargs["bigDataUrl"] = verify_str(f"{self.identifier}.bigBed")
        elif self.kwargs["type"] == "bigWig":
            self.kwargs["bigDataUrl"] = verify_str(f"{self.identifier}.bigWig")
        elif self.kwargs["type"] == "bigGenePred":
            self.kwargs["bigDataUrl"] = verify_str(f"{self.identifier}.bigGenePred")
        elif self.kwargs["type"] == "bigChain":
            self.kwargs["bigDataUrl"] = verify_str(f"{self.identifier}.bigChain")
        elif self.kwargs["type"] == "vcfTabix":
            self.kwargs["bigDataUrl"] = verify_str(f"{self.identifier}.vcf.gz")
        elif self.kwargs["type"] == "bam" and self.suffix == "bam":
            self.kwargs["bigDataUrl"] = verify_str(f"{self.identifier}.bam")
        elif self.kwargs["type"] == "bam" and self.suffix == "cram":
            self.kwargs["bigDataUrl"] = verify_str(f"{self.identifier}.cram")
        elif self.kwargs["type"] == "hic":
            self.kwargs["bigDataUrl"] = verify_str(f"{self.identifier}.hic")
        else:
            raise ValueError(f"Unknown file type {self.path}.")

        self.big_data_url = os.path.join(self.hub_identifier, self.genome_identifier, self.kwargs["bigDataUrl"])

    def fetch_jobs(
            self,
            group: str,
    ) -> TrackJobGroup:

        job_group = TrackJobGroup(name=group)

        # bed -> bigBed
        if re.match(r"^bigBed", self.kwargs["type"]):
            if self.suffix in ("bigbed", "bb",):
                job_group.add_job(TrackJob(
                    func=make_symlink,
                    arguments={"input_path": self.path, "output_path": self.big_data_url},
                ))
            elif re.match(r"^bed\d?$", self.suffix):
                job_group.add_job(TrackJob(
                    func=bed_to_big_bed,
                    arguments={"input_path": self.path, "sizes_path": self.sizes_path, "bigbed_type": self.kwargs["type"], "output_path": self.big_data_url,"as_path": find_as(self.as_path)},
                ))
            else:
                raise ValueError(f"Unknown file type: {self.path}.")

        # bedGraph / bam -> bigWig
        elif self.kwargs["type"] == "bigWig":
            if self.suffix in ("bw", "bigwig",):
                job_group.add_job(TrackJob(
                    func=make_symlink,
                    arguments={"input_path": self.path, "output_path": self.big_data_url},
                ))
            elif re.match(r"^bed\d?$", self.suffix) or self.suffix in ("bedgraph",):
                job_group.add_job(TrackJob(
                    func=bedgraph_to_big_wig,
                    arguments={"input_path": self.path, "sizes_path": self.sizes_path, "output_path": self.big_data_url},
                ))
            elif self.suffix in ("bam",):
                job_group.add_job(TrackJob(
                    func=bam_to_big_wig,
                    arguments={"input_path": self.path, "output_path": self.big_data_url},
                ))
            else:
                raise ValueError(f"Unknown file type: {self.path}.")

        # gff / gtf -> bigGenePred
        elif self.kwargs["type"] == "bigGenePred":
            if self.suffix in ("biggenepred",):
                job_group.add_job(TrackJob(
                    func=make_symlink,
                    arguments={"input_path": self.path, "output_path": self.big_data_url},
                ))
            elif self.suffix in ("gff", "gff3",):
                job_group.add_job(TrackJob(
                    func=gff_to_big_gene_pred,
                    arguments={"input_path": self.path, "as_path": find_as("bigGenePred.as"), "sizes_path": self.sizes_path, "output_path": self.big_data_url},
                ))
            elif self.suffix in ("gtf",):
                job_group.add_job(TrackJob(
                    func=gtf_to_big_gene_pred,
                    arguments={"input_path": self.path, "as_path": find_as("bigGenePred.as"), "sizes_path": self.sizes_path, "output_path": self.big_data_url},
                ))
            else:
                raise ValueError(f"Unknown file type: {self.path}.")

        # hic
        elif self.kwargs["type"] == "hic":
            if self.suffix in ("hic",):
                job_group.add_job(TrackJob(
                    func=make_symlink,
                    arguments={"input_path": self.path, "output_path": self.big_data_url},
                ))
            else:
                raise ValueError(f"Unknown file type: {self.path}.")

        # bam
        elif self.kwargs["type"] == "bam":
            if self.suffix in ("bam", "cram",):
                job_group.add_job(TrackJob(
                    func=make_symlink,
                    arguments={"input_path": self.path, "output_path": self.big_data_url},
                ))
                job_group.add_job(TrackJob(
                    func=samtools_index,
                    arguments={"input_path": self.big_data_url},
                ))
            else:
                raise ValueError(f"Unknown file type: {self.path}.")

        # vcfTabix
        elif self.kwargs["type"] == "vcfTabix":
            if self.suffix in ("vcf.gz",):
                job_group.add_job(TrackJob(
                    func=make_symlink,
                    arguments={"input_path": self.path, "output_path": self.big_data_url},
                ))
                job_group.add_job(TrackJob(
                    func=tabix,
                    arguments={"preset": "vcf", "input_path": self.big_data_url},
                ))
            else:
                raise ValueError(f"Unknown file type: {self.path}.")

        else:
            raise ValueError(f"Unknown type: {self.kwargs['type']}.")

        return job_group


