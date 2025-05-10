#!/usr/bin/env python3

import subprocess
from typing import Optional
from src.utils import *


def make_symlink(
        input_path: str,
        output_path: str,
) -> None:

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Source file {input_path} does not exist.")

    if os.path.exists(output_path):
        os.remove(output_path)

    os.symlink(os.path.abspath(input_path), output_path)


def fa_to_two_bit(
        input_path: str,
        output_path: str,
) -> None:

    subprocess.run(f"faToTwoBit {input_path} {output_path}", shell=True, check=True)


def two_bit_info(
        input_path: str,
        sizes_path: str,
) -> None:

    subprocess.run(f"twoBitInfo {input_path} {sizes_path}", shell=True, check=True)


def bed_to_big_bed(
        input_path: str,
        sizes_path: str,
        bigbed_type: str,
        output_path: str,
        as_path: Optional[str] = None,
) -> None:

    bed_type = bigbed_type.lstrip("big").replace(" ", "").lower()
    bed_type = "bed3" if bed_type == "bed" else bed_type
    if as_path is None:
        subprocess.run(f"bedToBigBed -tab -type={bed_type} {input_path} {sizes_path} {output_path}", shell=True, check=True)
    else:
        subprocess.run(f"bedToBigBed -tab -type={bed_type} -as {as_path} {input_path} {sizes_path} {output_path}", shell=True, check=True)


def bedgraph_to_big_wig(
        input_path: str,
        sizes_path: str,
        output_path: str,
) -> None:
    subprocess.run(f"bedGraphToBigWig {input_path} {sizes_path} {output_path}", shell=True, check=True)


def bam_to_big_wig(
        input_path: str,
        output_path: str,
) -> None:

    subprocess.run(f"""
bamCoverage \
    --numberOfProcessors max \
    --minMappingQuality 0 \
    --binSize 1 \
    --skipNonCoveredRegions \
    --bam {input_path} \
    --outFileName {output_path}
""", shell=True, check=True)


def gff_to_big_gene_pred(
        input_path: str,
        as_path: str,
        sizes_path: str,
        output_path: str,
) -> None:

    subprocess.run(f"""
gff3ToGenePred {input_path} stdout \
    | genePredToBigGenePred stdin stdout \
    | bedToBigBed -type=bed12+8 -tab -as={as_path} stdin {sizes_path} {output_path}
""", shell=True, check=True)


def gtf_to_big_gene_pred(
        input_path: str,
        as_path: str,
        sizes_path: str,
        output_path: str,
) -> None:

    subprocess.run(f"""
gtfToGenePred -genePredExt {input_path} stdout \
    | genePredToBigGenePred stdin stdout \
    | bedToBigBed -type=bed12+8 -tab -as={as_path} stdin {sizes_path} {output_path}
""", shell=True, check=True)


def samtools_index(
        input_path: str,
) -> None:

    subprocess.run(f"samtools index {input_path}", shell=True, check=True)


def tabix(
        preset: str,
        input_path: str,
) -> None:

    subprocess.run(f"tabix -p {preset} {input_path}", shell=True, check=True)


