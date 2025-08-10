#!/bin/bash

set -e
set -o pipefail

ARGS=$(getopt -a -o g:G:s: -l gff3:,gtf:,size: -- "$@")

eval set -- "${ARGS}"
while true; do
	case "$1" in
		-g|--gff3)
			gff3="$2"
			shift
			;;
		-G|--gtf)
			gtf="$2"
			shift
			;;
		-s|--size)
			size="$2"
			shift
			;;
		--)
			shift
			break
			;;
	esac
	shift
done


script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
as="${script_dir}/bigGenePred.as"

if [ "${gff3}" ]; then
	prefix="${gff3%.gz}"
	prefix="${prefix%.gff3}"
	prefix="${prefix%.gff}"
	(
		echo '##gff-version 3';
		awk 'BEGIN{FS=OFS="\t"} !/^#/ {print}' "${gff3}" | gffread --keep-comments --keep-genes -F --keep-exon-attrs;
	) \
	| gff3ToGenePred -geneNameAttr=gene_name stdin "${prefix}.genePred"
elif [ "${gtf}" ]; then
	prefix="${gtf%.gz}"
	prefix="${prefix%.gtf}"
	gtfToGenePred -genePredExt -geneNameAsName2 ${gtf} ${prefix}.genePred
else
	echo 'GFF3 or GTF should be provided.'
fi

genePredToBigGenePred "${prefix}.genePred" stdout \
| sort -k1,1 -k2,2n \
| awk 'BEGIN{FS=OFS="\t"} {if ($14 == "cmpl" && $15 == "cmpl") color = "25,25,112"; else if ($14 == "none" && $15 == "none") color = "50,205,50"; else color = "0,0,0"; $9 = color; print}' \
> "${prefix}.bigGenePredEx4.txt"
bedToBigBed -type=bed12+8 -tab -as=${as} "${prefix}.bigGenePredEx4.txt" -extraIndex=name "${size}" "${prefix}.bigBed"

awk 'BEGIN{FS=OFS="\t"} {print $4, $18, $19}' "${prefix}.bigGenePredEx4.txt" | ixIxx stdin "${prefix}.ix" "${prefix}.ixx"
