#!/usr/bin/env python3

import bigtrack


# global options
description_dir = "https://synplotter.sjtu.edu.cn/disk2/descriptions"


#################################################
# Hub
#################################################

hub = bigtrack.Hub(
    hub="T2TMacaqueHub_UCSC",
    shortLabel="T2T Macaque Hub",
    longLabel="T2T Macaque Hub",
    email="shilong.zhang@sjtu.edu.cn",
    descriptionUrl="description.html",
)


#################################################
# T2T-MMU8v2.0
#################################################

data_dir = "https://synplotter.sjtu.edu.cn/disk2/T2T-MMU8/release_v2.0"


#################################################
# Genomes
#################################################

genome_v2 = bigtrack.Genome(
    genome="GCA_049350105.2",
    htmlPath=f"{data_dir}/description.html",
)
hub.add_genome(genome_v2)


#################################################
# Groups
#################################################

group_user = bigtrack.Group(
    name="user",
    label="Custom Tracks",
    priority=1,
)
genome_v2.add_group(group_user)

group_map = bigtrack.Group(
    name="map",
    label="Mapping and Sequencing",
    priority=2,
)
genome_v2.add_group(group_map)

group_genes = bigtrack.Group(
    name="genes",
    label="Genes and Gene Predictions",
    priority=3,
)
genome_v2.add_group(group_genes)

group_rna = bigtrack.Group(
    name="rna",
    label="mRNA and EST",
    priority=4,
)
genome_v2.add_group(group_rna)

group_regulation = bigtrack.Group(
    name="regulation",
    label="Expression and Regulation",
    priority=5,
)
genome_v2.add_group(group_regulation)

group_compGeno = bigtrack.Group(
    name="compGeno",
    label="Comparative Genomics",
    priority=6,
)
genome_v2.add_group(group_compGeno)

group_varRep = bigtrack.Group(
    name="varRep",
    label="Variation and Repeats",
    priority=7,
)
genome_v2.add_group(group_varRep)


#################################################
# Mapping and Sequencing
#################################################

# make trackDb
trackDb_map = bigtrack.TrackDb(
    include="trackDb_map.txt",
)
genome_v2.add_trackDb(trackDb_map)

# make tracks
track_mappability = bigtrack.CompositeTrack(
    track="mappability",
    shortLabel="Mappability",
    longLabel="Mappability",
    type="bigWig",
    group="map",
    autoScale="Off",
    maxHeightPixels="128:36:16",
    graphTypeDefault="Bar",
    gridDefault="OFF",
    windowingFunction="Mean",
    viewLimits="0:1",
    visibility="full",
    html=f"{description_dir}/mappability-genmap.html",
)
track_mappability_k21 = bigtrack.Track(
    track="mappability_k21",
    shortLabel="k=21, e=0",
    longLabel="Mappability (k=21, e=0)",
    bigDataUrl=f"{data_dir}/T2T-MMU8v2.0.k21_e0_mappability.bigwig",
    type="bigWig",
    group="map",
    color="128,104,193",
    visibility="full",
)
track_mappability_k31 = bigtrack.Track(
    track="mappability_k31",
    shortLabel="k=31, e=0",
    longLabel="Mappability (k=31, e=0)",
    bigDataUrl=f"{data_dir}/T2T-MMU8v2.0.k31_e0_mappability.bigwig",
    type="bigWig",
    group="map",
    color="128,104,193",
    visibility="hide",
)
track_mappability.add_child(track_mappability_k21)
track_mappability.add_child(track_mappability_k31)
trackDb_map.add_track(track_mappability)

track_newly_resolved = bigtrack.CompositeTrack(
    track="newly_resolved",
    shortLabel="Newly resolved regions",
    longLabel="Newly resolved regions",
    type="bigBed 3",
    group="map",
    html=f"{description_dir}/newly_resolved_regions.html",
)
track_newly_resolved_Mmul_10 = bigtrack.Track(
    track="newly_resolved_Mmul_10",
    shortLabel="Mmul_10",
    longLabel="Newly resolved regions to Mmul_10",
    bigDataUrl=f"{data_dir}/non_syntenic_regions/non_syntenic_regions.Mmul_10.bigbed",
    type="bigBed 3",
    group="map",
    color="136,136,136",
    visibility="pack",
)
track_newly_resolved_rheMacS = bigtrack.Track(
    track="newly_resolved_rheMacS",
    shortLabel="rheMacS_1.0",
    longLabel="Newly resolved regions to rheMacS_1.0",
    bigDataUrl=f"{data_dir}/non_syntenic_regions/non_syntenic_regions.rheMacS_1.0.bigbed",
    type="bigBed 3",
    group="map",
    color="136,136,136",
    visibility="pack",
)
track_newly_resolved.add_child(track_newly_resolved_Mmul_10)
track_newly_resolved.add_child(track_newly_resolved_rheMacS)
trackDb_map.add_track(track_newly_resolved)

track_version_chains = bigtrack.SuperTrack(
    track="version_chains",
    shortLabel="Version chains",
    longLabel="Version chains",
    type="bigChain",
    group="map",
    html=f"{description_dir}/chain_alignments-versions.html",
)
for genome, identifier in {
    "T2T-MMU8v1.0": "GCA_049350105.1",
}.items():
    child = bigtrack.Track(
        track=f"version_chains_{genome}",
        shortLabel=genome,
        longLabel=f"Chain alignments to {genome} ({identifier}))",
        type=f"bigChain {identifier}",
        group="map",
        bigDataUrl=f"{data_dir}/liftover_chains/ref-T2T-MMU8v2.0_qry-{genome}.swapped.bigchain.bigbed",
        linkDataUrl=f"{data_dir}/liftover_chains/ref-T2T-MMU8v2.0_qry-{genome}.swapped.link.bigbed",
        visibility="pack",
    )
    track_version_chains.add_child(child)
trackDb_map.add_track(track_version_chains)

track_validation = bigtrack.SuperTrack(
    track="assembly_validation",
    shortLabel="Assembly validation",
    longLabel="Assembly validation",
    group="map",
    itemRgb="On",
    visibility="hide",
    html=f"{description_dir}/assembly_validation.html",
)
track_hifi_depth = bigtrack.Track(
    track="pacbio_hifi_depth",
    shortLabel="PacBio HiFi depth",
    longLabel="PacBio HiFi depth (MQ ≥ 1, excluding flag 3840)",
    bigDataUrl=f"{data_dir}/T2T-MMU8v2.0.AXM.hifi_depth.MQ1F3840.bigwig",
    type="bigWig",
    group="map",
    color="184,184,184",
    autoScale="off",
    maxHeightPixels="128:36:16",
    graphTypeDefault="Bar",
    gridDefault="OFF",
    windowingFunction="Mean",
    viewLimits="0:80",
    visibility="full",
    html=f"{description_dir}/read_depth-hifi.html",
)
track_ont_depth = bigtrack.Track(
    track="ont_depth",
    shortLabel="ONT depth",
    longLabel="ONT depth (MQ ≥ 1, excluding flag 3840)",
    bigDataUrl=f"{data_dir}/T2T-MMU8v2.0.AXM.ont_depth.MQ1F3840.bigwig",
    type="bigWig",
    group="map",
    color="184,184,184",
    autoScale="off",
    maxHeightPixels="128:36:16",
    graphTypeDefault="Bar",
    gridDefault="OFF",
    windowingFunction="Mean",
    viewLimits="0:60",
    visibility="full",
    html=f"{description_dir}/read_depth-ont.html",
)
track_validation.add_child(track_hifi_depth)
track_validation.add_child(track_ont_depth)
trackDb_map.add_track(track_validation)


#################################################
# Genes and Gene Predictions
#################################################

# make trackDb
trackDb_genes = bigtrack.TrackDb(
    include="trackDb_genes.txt",
)
genome_v2.add_trackDb(trackDb_genes)

# make tracks
track_liftoff_mfa8 = bigtrack.Track(
    track="liftoff_mfa8",
    shortLabel="Liftoff T2T-MFA8v1.1 RefSeq",
    longLabel="Liftoff from T2T-MFA8v1.1 (GCF_037993035.2-RS_2025_03)",
    type="bigGenePred",
    group="genes",
    bigDataUrl=f"{data_dir}/T2T-MMU8v2.0.liftoff-RefSeq_GCF_037993035.2_AXY-Mmul_10_M.bigBed",
    itemRgb="On",
    visibility="pack",
    baseColorDefault="genomicCodons",
    labelFields="name2,name",
    defaultLabelFields="name2,name",
    searchIndex="name,geneName,geneName2",
    searchTrix=f"{data_dir}/T2T-MMU8v2.0.liftoff-RefSeq_GCF_037993035.2_AXY-Mmul_10_M.ix",
    html=f"{description_dir}/gene_annotation-liftoff.html",
)
trackDb_genes.add_track(track_liftoff_mfa8)

track_liftoff_mmul_10 = bigtrack.Track(
    track="liftoff_mmul_10",
    shortLabel="Liftoff Mmul_10 RefSeq",
    longLabel="Liftoff from Mmul_10 (GCF_003339765.1 Annotation Release 103)",
    type="bigGenePred",
    group="genes",
    bigDataUrl=f"{data_dir}/T2T-MMU8v2.0.liftoff-RefSeq_Mmul_10.bigBed",
    itemRgb="On",
    visibility="hide",
    baseColorDefault="genomicCodons",
    labelFields="name2,name",
    defaultLabelFields="name2,name",
    searchIndex="name,geneName,geneName2",
    searchTrix=f"{data_dir}/T2T-MMU8v2.0.liftoff-RefSeq_Mmul_10.ix",
    html=f"{description_dir}/gene_annotation-liftoff.html",
)
trackDb_genes.add_track(track_liftoff_mmul_10)


#################################################
# Expression and Regulation
#################################################

# make trackDb
trackDb_regulation = bigtrack.TrackDb(
    include="trackDb_regulation.txt",
)
genome_v2.add_trackDb(trackDb_regulation)

# make tracks
track_methylation = bigtrack.SuperTrack(
    track="methylation",
    shortLabel="Methylation",
    longLabel="Methylation",
    group="regulation",
    superTrack="on show",
    html=f"{description_dir}/methylation-dorado.html",
)
track_methylated_cpgs = bigtrack.Track(
    track="methylated_cpgs",
    shortLabel="Methylated CpGs %",
    longLabel="Methylated CpGs %, ONT R10.4.1, traditional preset",
    bigDataUrl=f"{data_dir}/T2T-MMU8v2.0.AXM.Nanopore_R10_5mCG.ge5.bigwig",
    type="bigWig",
    group="regulation",
    color="29,29,141",
    visibility="full",
    maxHeightPixels="128:36:16",
    graphTypeDefault="Bar",
    gridDefault="OFF",
    windowingFunction="Mean",
    viewLimits="0:100",
)
track_bigmethyl = bigtrack.Track(
    track="cpg_bigmethyl",
    shortLabel="CpG methylation",
    longLabel="CpG methylation, ONT R10.4.1, traditional preset",
    bigDataUrl=f"{data_dir}/T2T-MMU8v2.0.AXM.Nanopore_R10.ge5.bigMethyl",
    type="bigMethyl",
    group="regulation",
    visibility="hide",
)
track_methylation.add_child(track_methylated_cpgs)
track_methylation.add_child(track_bigmethyl)
trackDb_regulation.add_track(track_methylation)


#################################################
# Comparative Genomics
#################################################

# make trackDb
trackDb_compGeno = bigtrack.TrackDb(
    include="trackDb_compGeno.txt",
)
genome_v2.add_trackDb(trackDb_compGeno)

# add tracks
track_macaque_chains = bigtrack.SuperTrack(
    track="macaque_chains",
    shortLabel="Macaque chains",
    longLabel="Macaque chains",
    type="bigChain",
    group="compGeno",
    html=f"{description_dir}/chain_alignments-other_assemblies.html",
)
for genome, identifier in {
    "Mmul_10": "GCF_003339765.1",
    "T2T-MFA8v1.1": "GCF_037993035.2",
    "rheMacS_1.0": "GCA_008058575.1",
}.items():
    child = bigtrack.Track(
        track=f"macaque_chains_{genome}",
        shortLabel=genome,
        longLabel=f"Chain alignments to {genome} ({identifier})",
        type=f"bigChain {identifier}",
        group="compGeno",
        bigDataUrl=f"{data_dir}/liftover_chains/ref-T2T-MMU8v2.0_qry-{genome}.swapped.bigchain.bigbed",
        linkDataUrl=f"{data_dir}/liftover_chains/ref-T2T-MMU8v2.0_qry-{genome}.swapped.link.bigbed",
        visibility="pack",
    )
    track_macaque_chains.add_child(child)
trackDb_compGeno.add_track(track_macaque_chains)

track_primate_chains = bigtrack.SuperTrack(
    track="primate_chains",
    shortLabel="Primate chains",
    longLabel="Primate chains",
    type="bigChain",
    group="compGeno",
    html=f"{description_dir}/chain_alignments-other_assemblies.html",
)
for genome, identifier in {
    "T2T-CHM13v2.0": "GCF_009914755.1",
    "mGorGor1_v2.0_pri": "GCF_029281585.2",
    "mPanPan1_v2.0_pri": "GCF_029289425.2",
    "mPanTro3_v2.0_pri": "GCF_028858775.2",
    "mPonAbe1_v2.0_pri": "GCF_028885655.2",
    "mPonPyg2_v2.0_pri": "GCF_028885625.2",
    "mSymSyn1_v2.0_pri": "GCF_028878055.2",
}.items():
    child = bigtrack.Track(
        track=f"primate_chains_{genome}",
        shortLabel=genome,
        longLabel=f"Chain alignments to {genome} ({identifier})",
        type=f"bigChain {identifier}",
        group="compGeno",
        bigDataUrl=f"{data_dir}/liftover_chains/ref-T2T-MMU8v2.0_qry-{genome}.swapped.bigchain.bigbed",
        linkDataUrl=f"{data_dir}/liftover_chains/ref-T2T-MMU8v2.0_qry-{genome}.swapped.link.bigbed",
        visibility="pack",
    )
    track_primate_chains.add_child(child)
trackDb_compGeno.add_track(track_primate_chains)


#################################################
# Variation and Repeats
#################################################

# make trackDb
trackDb_varRep = bigtrack.TrackDb(
    include="trackDb_varRep.txt",
)
genome_v2.add_trackDb(trackDb_varRep)

# make tracks
track_alpha_sat = bigtrack.Track(
    track="alpha_sat",
    shortLabel="Alpha satellites",
    longLabel="Alpha satellites",
    bigDataUrl=f"{data_dir}/T2T-MMU8v2.0.alpha_satellite.bigbed",
    type="bigBed 9",
    itemRgb="On",
    labelFields="none",
    group="varRep",
    html=f"{description_dir}/repeatmasker-alpha_satellites.html",
)
trackDb_varRep.add_track(track_alpha_sat)

track_microsatellites = bigtrack.CompositeTrack(
    track="microsatellites",
    shortLabel="Microsatellites",
    longLabel="Microsatellites",
    type="bigWig",
    group="varRep",
    autoScale="Off",
    maxHeightPixels="128:36:16",
    graphTypeDefault="Bar",
    gridDefault="OFF",
    windowingFunction="Mean",
    viewLimits="0:100",
    html=f"{description_dir}/microsatellites.html",
)
track_microsatellites_GA = bigtrack.Track(
    track="microsatellites_GA",
    shortLabel="GA Microsatellites",
    longLabel="GA Microsatellites in 128-bp windows",
    bigDataUrl=f"{data_dir}/T2T-MMU8v2.0.microsatellite_GA_w128.bigwig",
    type="bigWig",
    group="varRep",
    color="83,105,255",
    visibility="full",
)
track_microsatellites_TC = bigtrack.Track(
    track="microsatellites_TC",
    shortLabel="TC Microsatellites",
    longLabel="TC Microsatellites in 128-bp windows",
    bigDataUrl=f"{data_dir}/T2T-MMU8v2.0.microsatellite_TC_w128.bigwig",
    type="bigWig",
    group="varRep",
    color="102,0,102",
    visibility="full",
)
track_microsatellites_GC = bigtrack.Track(
    track="microsatellites_GC",
    shortLabel="GC Microsatellites",
    longLabel="GC Microsatellites in 128-bp windows",
    bigDataUrl=f"{data_dir}/T2T-MMU8v2.0.microsatellite_GC_w128.bigwig",
    type="bigWig",
    group="varRep",
    color="188,115,19",
    visibility="full",
)
track_microsatellites_AT = bigtrack.Track(
    track="microsatellites_AT",
    shortLabel="AT Microsatellites",
    longLabel="AT Microsatellites in 128-bp windows",
    bigDataUrl=f"{data_dir}/T2T-MMU8v2.0.microsatellite_AT_w128.bigwig",
    type="bigWig",
    group="varRep",
    color="51,102,0",
    visibility="full",
)
track_microsatellites.add_child(track_microsatellites_GA)
track_microsatellites.add_child(track_microsatellites_TC)
track_microsatellites.add_child(track_microsatellites_GC)
track_microsatellites.add_child(track_microsatellites_AT)
trackDb_varRep.add_track(track_microsatellites)

track_rdna = bigtrack.Track(
    track="rDNA",
    shortLabel="rDNA models",
    longLabel="rDNA models",
    bigDataUrl=f"{data_dir}/T2T-MMU8v2.0.rDNA.bigbed",
    type="bigBed 3",
    group="varRep",
    html=f"{description_dir}/rDNA_models.html",
)
trackDb_varRep.add_track(track_rdna)

track_longdust = bigtrack.Track(
    track="longdust",
    shortLabel="LongDust",
    longLabel="Genomic intervals masked by LongDust",
    bigDataUrl=f"{data_dir}/T2T-MMU8v2.0.longdust.bigbed",
    type="bigBed 3",
    group="varRep",
    visibility="hide",
    html=f"{description_dir}/longdust.html",
)
trackDb_varRep.add_track(track_longdust)

track_sd = bigtrack.Track(
    track="sd",
    shortLabel="Segmental duplications",
    longLabel="Segmental duplications by SEDEF",
    bigDataUrl=f"{data_dir}/T2T-MMU8v2.0.SDs.bigbed",
    type="bigBed 9 +",
    itemRgb="On",
    group="varRep",
    visibility="pack",
    maxItems=100000,
    html=f"{description_dir}/segmental_duplications-sedef.html",
)
trackDb_varRep.add_track(track_sd)

track_numt = bigtrack.Track(
    track="numt",
    shortLabel="NUMT",
    longLabel="Nuclear-embedded mitochondrial DNA",
    bigDataUrl=f"{data_dir}/T2T-MMU8v2.0.NUMTs.bigbed",
    type="bigBed 3",
    group="varRep",
    visibility="hide",
    html=f"{description_dir}/numt.html",
)
trackDb_varRep.add_track(track_numt)

track_satr = bigtrack.CompositeTrack(
    track="satr",
    shortLabel="SATR family",
    longLabel="SATR family",
    type="bigBed",
    group="varRep",
    html=f"{description_dir}/repeatmasker-satr_family.html",
)
track_satr1 = bigtrack.Track(
    track="satr1",
    shortLabel="SATR1",
    longLabel="SATR1",
    bigDataUrl=f"{data_dir}/SATR1.bigbed",
    type="bigBed 9",
    group="varRep",
    visibility="dense",
    itemRgb="On",
    labelFields="none",
)
track_satr1v = bigtrack.Track(
    track="satr1v",
    shortLabel="SATR1v",
    longLabel="SATR1v",
    bigDataUrl=f"{data_dir}/SATR1v.bigbed",
    type="bigBed 9",
    group="varRep",
    visibility="dense",
    itemRgb="On",
    labelFields="none",
)
track_satr2 = bigtrack.Track(
    track="satr2",
    shortLabel="SATR2",
    longLabel="SATR2",
    bigDataUrl=f"{data_dir}/SATR2.bigbed",
    type="bigBed 9",
    group="varRep",
    visibility="dense",
    itemRgb="On",
    labelFields="none",
)
track_satr.add_child(track_satr1)
track_satr.add_child(track_satr1v)
track_satr.add_child(track_satr2)
trackDb_varRep.add_track(track_satr)

track_sequence_identity = bigtrack.SuperTrack(
    track="sequence_identity",
    shortLabel="Sequence identity",
    longLabel="Sequence identity",
    type="bigBed 9",
    group="varRep",
    itemRgb="On",
    visibility="hide",
    html=f"{description_dir}/sequence_identity-mashmap.html",
)
for chrom in ["chr1", "chr2", "chr3", "chr4", "chr5", "chr6", "chr7", "chr8", "chr9", "chr10", "chr11", "chr12", "chr13", "chr14", "chr15", "chr16", "chr17", "chr18", "chr19", "chr20", "chrX", "chrY"]:
    child = bigtrack.Track(
        track=f"sequence_identity_{chrom}",
        shortLabel=chrom,
        longLabel=chrom,
        bigDataUrl=f"{data_dir}/sequence_identity/{chrom}.bigbed",
        type="bigBed 9",
        group="varRep",
        visibility="dense",
    )
    track_sequence_identity.add_child(child)
trackDb_varRep.add_track(track_sequence_identity)


#################################################
# T2T-MFA8v1.1
#################################################

data_dir = "https://synplotter.sjtu.edu.cn/disk2/T2T-MFA8/release_v1.1"


#################################################
# Genomes
#################################################

genome_v11 = bigtrack.Genome(
    genome="GCF_037993035.2",
    htmlPath=f"{data_dir}/description.html",
)
hub.add_genome(genome_v11)


#################################################
# Groups
#################################################

group_user = bigtrack.Group(
    name="user",
    label="Custom Tracks",
    priority=1,
)
genome_v11.add_group(group_user)

group_map = bigtrack.Group(
    name="map",
    label="Mapping and Sequencing",
    priority=2,
)
genome_v11.add_group(group_map)

group_genes = bigtrack.Group(
    name="genes",
    label="Genes and Gene Predictions",
    priority=3,
)
genome_v11.add_group(group_genes)

group_rna = bigtrack.Group(
    name="rna",
    label="mRNA and EST",
    priority=4,
)
genome_v11.add_group(group_rna)

group_regulation = bigtrack.Group(
    name="regulation",
    label="Expression and Regulation",
    priority=5,
)
genome_v11.add_group(group_regulation)

group_compGeno = bigtrack.Group(
    name="compGeno",
    label="Comparative Genomics",
    priority=6,
)
genome_v11.add_group(group_compGeno)

group_varRep = bigtrack.Group(
    name="varRep",
    label="Variation and Repeats",
    priority=7,
)
genome_v11.add_group(group_varRep)


#################################################
# Mapping and Sequencing
#################################################

# make trackDb
trackDb_map = bigtrack.TrackDb(
    include="trackDb_map.txt",
)
genome_v11.add_trackDb(trackDb_map)

# make tracks
track_mappability = bigtrack.CompositeTrack(
    track="mappability",
    shortLabel="Mappability",
    longLabel="Mappability",
    type="bigWig",
    group="map",
    autoScale="Off",
    maxHeightPixels="128:36:16",
    graphTypeDefault="Bar",
    gridDefault="OFF",
    windowingFunction="Mean",
    viewLimits="0:1",
    visibility="full",
    html=f"{description_dir}/mappability-genmap.html",
)
track_mappability_k21 = bigtrack.Track(
    track="mappability_k21",
    shortLabel="k=21, e=0",
    longLabel="Mappability (k=21, e=0)",
    bigDataUrl=f"{data_dir}/T2T-MFA8v1.1.k21_e0_mappability.bigwig",
    type="bigWig",
    group="map",
    color="128,104,193",
    visibility="full",
)
track_mappability_k31 = bigtrack.Track(
    track="mappability_k31",
    shortLabel="k=31, e=0",
    longLabel="Mappability (k=31, e=0)",
    bigDataUrl=f"{data_dir}/T2T-MFA8v1.1.k31_e0_mappability.bigwig",
    type="bigWig",
    group="map",
    color="128,104,193",
    visibility="hide",
)
track_mappability.add_child(track_mappability_k21)
track_mappability.add_child(track_mappability_k31)
trackDb_map.add_track(track_mappability)

track_validation = bigtrack.SuperTrack(
    track="assembly_validation",
    shortLabel="Assembly validation",
    longLabel="Assembly validation",
    group="map",
    itemRgb="On",
    visibility="hide",
    html=f"{description_dir}/assembly_validation.html",
)
track_hifi_depth = bigtrack.Track(
    track="pacbio_hifi_depth",
    shortLabel="PacBio HiFi depth",
    longLabel="PacBio HiFi depth (MQ ≥ 1, excluding flag 3840)",
    bigDataUrl=f"{data_dir}/T2T-MFA8v1.1.AXM.hifi_depth.MQ1F3840.bigwig",
    type="bigWig",
    group="map",
    color="184,184,184",
    autoScale="off",
    maxHeightPixels="128:36:16",
    graphTypeDefault="Bar",
    gridDefault="OFF",
    windowingFunction="Mean",
    viewLimits="0:100",
    visibility="full",
    html=f"{description_dir}/read_depth-hifi.html",
)
track_ont_depth = bigtrack.Track(
    track="ont_depth",
    shortLabel="ONT depth",
    longLabel="ONT depth (MQ ≥ 1, excluding flag 3840)",
    bigDataUrl=f"{data_dir}/T2T-MFA8v1.1.AXM.ont_depth.MQ1F3840.bigwig",
    type="bigWig",
    group="map",
    color="184,184,184",
    autoScale="off",
    maxHeightPixels="128:36:16",
    graphTypeDefault="Bar",
    gridDefault="OFF",
    windowingFunction="Mean",
    viewLimits="0:120",
    visibility="full",
    html=f"{description_dir}/read_depth-ont.html",
)
track_validation.add_child(track_hifi_depth)
track_validation.add_child(track_ont_depth)
trackDb_map.add_track(track_validation)


#################################################
# Genes and Gene Predictions
#################################################

# make trackDb
trackDb_genes = bigtrack.TrackDb(
    include="trackDb_genes.txt",
)
genome_v11.add_trackDb(trackDb_genes)

# make tracks
track_liftoff_mmul_10 = bigtrack.Track(
    track="liftoff_mmul_10",
    shortLabel="Liftoff Mmul_10 RefSeq",
    longLabel="Liftoff from Mmul_10 (GCF_003339765.1 Annotation Release 103)",
    type="bigGenePred",
    group="genes",
    bigDataUrl=f"{data_dir}/T2T-MFA8v1.1.liftoff_Mmul_10.bigBed",
    itemRgb="On",
    visibility="hide",
    baseColorDefault="genomicCodons",
    labelFields="name2,name",
    defaultLabelFields="name2,name",
    searchIndex="name,geneName,geneName2",
    searchTrix=f"{data_dir}/T2T-MFA8v1.1.liftoff_Mmul_10.ix",
    html=f"{description_dir}/gene_annotation-liftoff.html",
)
trackDb_genes.add_track(track_liftoff_mmul_10)


#################################################
# Expression and Regulation
#################################################

# make trackDb
trackDb_regulation = bigtrack.TrackDb(
    include="trackDb_regulation.txt",
)
genome_v11.add_trackDb(trackDb_regulation)

# make tracks
track_methylation = bigtrack.SuperTrack(
    track="methylation",
    shortLabel="Methylation",
    longLabel="Methylation",
    group="regulation",
    superTrack="on show",
    html=f"{description_dir}/methylation-nanopolish.html",
)
track_methylated_cpgs = bigtrack.Track(
    track="methylated_cpgs",
    shortLabel="Methylated CpGs %",
    longLabel="Methylated CpGs %, Nanopolish v0.14.0",
    bigDataUrl=f"{data_dir}/T2T-MFA8v1.1.ONT_methylation.nanopolish_v0.14.0.bigwig",
    type="bigWig",
    group="regulation",
    color="29,29,141",
    visibility="full",
    maxHeightPixels="128:36:16",
    graphTypeDefault="Bar",
    gridDefault="OFF",
    windowingFunction="Mean",
    viewLimits="0:100",
)
track_methylation.add_child(track_methylated_cpgs)
trackDb_regulation.add_track(track_methylation)


#################################################
# Comparative Genomics
#################################################

# make trackDb
trackDb_compGeno = bigtrack.TrackDb(
    include="trackDb_compGeno.txt",
)
genome_v11.add_trackDb(trackDb_compGeno)


#################################################
# Variation and Repeats
#################################################

# make trackDb
trackDb_varRep = bigtrack.TrackDb(
    include="trackDb_varRep.txt",
)
genome_v11.add_trackDb(trackDb_varRep)

# make tracks
track_alpha_sat = bigtrack.Track(
    track="alpha_sat",
    shortLabel="Alpha satellites",
    longLabel="Alpha satellites",
    bigDataUrl=f"{data_dir}/T2T-MFA8v1.1.alpha_satellites.bigbed",
    type="bigBed 9",
    itemRgb="On",
    labelFields="none",
    group="varRep",
    html=f"{description_dir}/repeatmasker-alpha_satellites.html",
)
trackDb_varRep.add_track(track_alpha_sat)

track_rdna = bigtrack.Track(
    track="rDNA",
    shortLabel="rDNA models",
    longLabel="rDNA models",
    bigDataUrl=f"{data_dir}/T2T-MFA8v1.1.rDNA.bigbed",
    type="bigBed 3",
    group="varRep",
    html=f"{description_dir}/rDNA_models.html",
)
trackDb_varRep.add_track(track_rdna)

track_microsatellites = bigtrack.CompositeTrack(
    track="microsatellites",
    shortLabel="Microsatellites",
    longLabel="Microsatellites",
    type="bigWig",
    group="varRep",
    autoScale="Off",
    maxHeightPixels="128:36:16",
    graphTypeDefault="Bar",
    gridDefault="OFF",
    windowingFunction="Mean",
    viewLimits="0:100",
    html=f"{description_dir}/microsatellites.html",
)
track_microsatellites_GA = bigtrack.Track(
    track="microsatellites_GA",
    shortLabel="GA Microsatellites",
    longLabel="GA Microsatellites in 128-bp windows",
    bigDataUrl=f"{data_dir}/T2T-MFA8v1.1.microsatellite_GA_w128.bigwig",
    type="bigWig",
    group="varRep",
    color="83,105,255",
    visibility="full",
)
track_microsatellites_TC = bigtrack.Track(
    track="microsatellites_TC",
    shortLabel="TC Microsatellites",
    longLabel="TC Microsatellites in 128-bp windows",
    bigDataUrl=f"{data_dir}/T2T-MFA8v1.1.microsatellite_TC_w128.bigwig",
    type="bigWig",
    group="varRep",
    color="102,0,102",
    visibility="full",
)
track_microsatellites_GC = bigtrack.Track(
    track="microsatellites_GC",
    shortLabel="GC Microsatellites",
    longLabel="GC Microsatellites in 128-bp windows",
    bigDataUrl=f"{data_dir}/T2T-MFA8v1.1.microsatellite_GC_w128.bigwig",
    type="bigWig",
    group="varRep",
    color="188,115,19",
    visibility="full",
)
track_microsatellites_AT = bigtrack.Track(
    track="microsatellites_AT",
    shortLabel="AT Microsatellites",
    longLabel="AT Microsatellites in 128-bp windows",
    bigDataUrl=f"{data_dir}/T2T-MFA8v1.1.microsatellite_AT_w128.bigwig",
    type="bigWig",
    group="varRep",
    color="51,102,0",
    visibility="full",
)
track_microsatellites.add_child(track_microsatellites_GA)
track_microsatellites.add_child(track_microsatellites_TC)
track_microsatellites.add_child(track_microsatellites_GC)
track_microsatellites.add_child(track_microsatellites_AT)
trackDb_varRep.add_track(track_microsatellites)

track_longdust = bigtrack.Track(
    track="longdust",
    shortLabel="LongDust",
    longLabel="Genomic intervals masked by LongDust",
    bigDataUrl=f"{data_dir}/T2T-MFA8v1.1.longdust.bigbed",
    type="bigBed 3",
    group="varRep",
    visibility="hide",
    html=f"{description_dir}/longdust.html",
)
trackDb_varRep.add_track(track_longdust)

track_sd = bigtrack.Track(
    track="sd",
    shortLabel="Segmental duplications",
    longLabel="Segmental duplications by SEDEF",
    bigDataUrl=f"{data_dir}/T2T-MFA8v1.1.SDs.bigbed",
    type="bigBed 9 +",
    itemRgb="On",
    group="varRep",
    visibility="pack",
    maxItems=100000,
    html=f"{description_dir}/segmental_duplications-sedef.html",
)
trackDb_varRep.add_track(track_sd)

track_numt = bigtrack.Track(
    track="numt",
    shortLabel="NUMT",
    longLabel="Nuclear-embedded mitochondrial DNA",
    bigDataUrl=f"{data_dir}/T2T-MFA8v1.1.NUMTs.bigbed",
    type="bigBed 3",
    group="varRep",
    visibility="hide",
    html=f"{description_dir}/numt.html",
)
trackDb_varRep.add_track(track_numt)

track_cnv_mfa = bigtrack.CompositeTrack(
    track="cnv_mfa",
    shortLabel="CN of crab-eating macaques",
    longLabel="Copy number estimation for crab-eating macaques",
    type="bigBed 9",
    group="varRep",
    itemRgb="On",
    html=f"{description_dir}/cnv-fastcn.html",
)
for sample in ["MFA0214", "MFA157", "MFA683", "MFA0251", "MFA16", "MFA746", "MFA0334", "MFA160135", "MFA768", "MFA0345", "MFA160383", "MFA802", "MFA0347", "MFA160485", "MFA82", "MFA0353", "MFA160563", "MFA825", "MFA0400", "MFA169", "MFA928", "MFA0464", "MFA173", "MFA96", "MFA0486", "MFA186", "MFA962", "MFA0497", "MFA186ZAI", "MFA963", "MFA0505", "MFA191", "MFA964", "MFA0522", "MFA2", "MFA965", "MFA0713", "MFA237", "MFA966", "MFA080", "MFA289", "MFA970", "MFA10", "MFA336", "MFA971", "MFA1000", "MFA344", "MFA972", "MFA1001", "MFA355", "MFA973", "MFA1003", "MFA362", "MFA974", "MFA1004", "MFA380", "MFA975", "MFA1005", "MFA395", "MFA976", "MFA1006", "MFA444", "MFA978", "MFA1007", "MFA454", "MFA980", "MFA1008", "MFA457", "MFA981", "MFA1010", "MFA469", "MFA982", "MFA1011", "MFA494", "MFA983", "MFA1012", "MFA513", "MFA985", "MFA1013", "MFA521", "MFA986", "MFA1014", "MFA53", "MFA987", "MFA1015", "MFA534", "MFA988", "MFA1016", "MFA535", "MFA989", "MFA1017", "MFA556", "MFA990", "MFA1021", "MFA565", "MFA991", "MFA1022", "MFA566", "MFA992", "MFA1023", "MFA582-1", "MFA993", "MFA1024", "MFA610", "MFA994", "MFA1025", "MFA615", "MFA995", "MFA1028", "MFA617", "MFA997", "MFA12", "MFA634", "MFA998", "MFA13", "MFA676", "MFA999"]:
    child = bigtrack.Track(
        track=f"cnv_mfa_{sample}",
        shortLabel=f"{sample} CN WSSD",
        longLabel=f"{sample} CN WSSD",
        bigDataUrl=f"{data_dir}/T2T-MFA8v1.0.MFA_CN/T2T-MFA8v1.1.{sample}.bigbed",
        type="bigBed 9",
        group="varRep",
        visibility="dense",
    )
    track_cnv_mfa.add_child(child)
trackDb_varRep.add_track(track_cnv_mfa)

track_cnv_mfa_subset = bigtrack.SampledCompositeTrack(
    full_track=track_cnv_mfa,
    number=20,
    shortLabel="CN of crab-eating macaques (subset)",
    longLabel="Copy number estimation for crab-eating macaques (subset)",
)
trackDb_varRep.add_track(track_cnv_mfa_subset)

track_cnv_mmu = bigtrack.CompositeTrack(
    track="cnv_mmu",
    shortLabel="CN of for rhesus macaques",
    longLabel="Copy number estimation for rhesus macaques",
    type="bigBed 9",
    group="varRep",
    itemRgb="On",
    html=f"{description_dir}/cnv-fastcn.html",
)
for sample in ["MMU0595", "MMU5029", "MMU5131", "MMU0715", "MMU5046", "MMU5136", "MMU0756", "MMU5049", "MMU5139", "MMU1003063", "MMU5050", "MMU5141", "MMU1005159", "MMU5059", "MMU5142", "MMU1005163", "MMU5062", "MMU5149", "MMU1205169", "MMU5063", "MMU5150", "MMU2019108-1", "MMU5066", "MMU5187", "MMU5001", "MMU5073", "MMU5202", "MMU5003", "MMU5076", "MMU5204", "MMU5018", "MMU5085", "MMU5205", "MMU5023", "MMU5115", "MMU5206"]:
    child = bigtrack.Track(
        track=f"cnv_mmu_{sample}",
        shortLabel=f"{sample} CN WSSD",
        longLabel=f"{sample} CN WSSD",
        bigDataUrl=f"{data_dir}/T2T-MFA8v1.0.MMU_CN/T2T-MFA8v1.1.{sample}.bigbed",
        type="bigBed 9",
        group="varRep",
        visibility="dense",
    )
    track_cnv_mmu.add_child(child)
trackDb_varRep.add_track(track_cnv_mmu)

track_cnv_mmu_subset = bigtrack.SampledCompositeTrack(
    full_track=track_cnv_mmu,
    number=20,
    shortLabel="CN of for rhesus macaques (subset)",
    longLabel="Copy number estimation for rhesus macaques (subset)",
)
trackDb_varRep.add_track(track_cnv_mmu_subset)

track_cnv_1kgp = bigtrack.CompositeTrack(
    track="cnv_1kgp",
    shortLabel="CN of human populations in 1KGP",
    longLabel="Copy number estimation for human populations in 1KGP",
    type="bigBed 9",
    group="varRep",
    itemRgb="On",
    html=f"{description_dir}/cnv-fastcn.html",
)
for sample in ["HG00096", "HG01137", "HG02654", "NA07051", "NA19704", "HG00097", "HG01500", "HG02655", "NA07347", "NA19707", "HG00099", "HG01501", "HG02922", "NA07357", "NA19711", "HG00100", "HG01503", "HG02923", "NA18486", "NA19712", "HG00101", "HG01504", "HG02943", "NA18489", "NA20502", "HG00102", "HG01506", "HG02944", "NA18498", "NA20503", "HG00103", "HG01507", "HG02973", "NA18499", "NA20504", "HG00105", "HG01509", "HG02974", "NA18501", "NA20505", "HG00171", "HG01510", "HG03006", "NA18502", "NA20506", "HG00173", "HG01565", "HG03007", "NA18504", "NA20507", "HG00174", "HG01566", "HG03052", "NA18505", "NA20508", "HG00176", "HG01571", "HG03057", "NA18526", "NA20509", "HG00177", "HG01572", "HG03058", "NA18532", "NA20845", "HG00178", "HG01577", "HG03078", "NA18537", "NA20846", "HG00179", "HG01578", "HG03084", "NA18542", "NA20847", "HG00180", "HG01882", "HG03085", "NA18545", "NA20849", "HG00442", "HG01883", "HG03096", "NA18547", "NA20850", "HG00443", "HG01885", "HG03097", "NA18550", "NA20851", "HG00445", "HG01886", "HG03099", "NA18552", "NA20852", "HG00446", "HG01889", "HG03100", "NA18940", "NA20853", "HG00448", "HG01890", "HG03615", "NA18942", "HG00449", "HG01917", "HG03616", "NA18943", "HG00451", "HG01918", "HG03642", "NA18944", "HG00452", "HG01956", "HG03643", "NA18945", "HG00553", "HG02014", "HG03644", "NA18947", "HG00554", "HG02016", "HG03673", "NA18948", "HG00637", "HG02017", "HG03679", "NA18949", "HG00638", "HG02019", "HG03684", "NA19017", "HG00640", "HG02020", "HG03713", "NA19019", "HG00641", "HG02023", "HG03714", "NA19020", "HG00731", "HG02025", "HG03716", "NA19023", "HG00732", "HG02026", "HG03717", "NA19024", "HG00759", "HG02029", "HG03722", "NA19025", "HG00766", "HG02461", "HG03727", "NA19026", "HG00844", "HG02462", "HG03729", "NA19027", "HG00851", "HG02464", "HG03730", "NA19625", "HG00864", "HG02465", "HG03793", "NA19648", "HG00867", "HG02490", "HG03796", "NA19649", "HG00879", "HG02491", "HG03800", "NA19651", "HG00881", "HG02561", "HG03803", "NA19652", "HG01112", "HG02562", "HG03885", "NA19654", "HG01113", "HG02570", "HG03886", "NA19655", "HG01124", "HG02571", "NA06985", "NA19657", "HG01125", "HG02600", "NA06986", "NA19658", "HG01133", "HG02601", "NA06994", "NA19700", "HG01134", "HG02603", "NA07000", "NA19701", "HG01136", "HG02604", "NA07037", "NA19703"]:
    child = bigtrack.Track(
        track=f"cnv_1kgp_{sample}",
        shortLabel=f"{sample} CN WSSD",
        longLabel=f"{sample} CN WSSD",
        bigDataUrl=f"{data_dir}/T2T-MFA8v1.0.1KGP_CN/T2T-MFA8v1.1.{sample}.bigbed",
        type="bigBed 9",
        group="varRep",
        visibility="dense",
    )
    track_cnv_1kgp.add_child(child)
trackDb_varRep.add_track(track_cnv_1kgp)

track_cnv_1kgp_subset = bigtrack.SampledCompositeTrack(
    full_track=track_cnv_1kgp,
    number=20,
    shortLabel="CN of human populations in 1KGP (subset)",
    longLabel="Copy number estimation for human populations in 1KGP (subset)",
)
trackDb_varRep.add_track(track_cnv_1kgp_subset)


#################################################
# Generate track hub
#################################################

hub.generate()
