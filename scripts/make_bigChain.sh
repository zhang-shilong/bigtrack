#!/usr/bin/env bash

set -e -u -o pipefail

ARGS=$(getopt -a -o c:s: -l chain:,size: -- "$@")

eval set -- "${ARGS}"
while true; do
	case "$1" in
		-c|--chain)
			chain=$(realpath "$2")
			shift
			;;
		-s|--size)
			size=$(realpath "$2")
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
as_bigchain="${script_dir}/bigChain.as"
as_biglink="${script_dir}/bigLink.as"
prefix="${chain%.gz}"
prefix="${prefix%.chain}"


chainToBigChain "${chain}" "${prefix}.bigchain.pre" "${prefix}.link.pre"
bedToBigBed -type=bed6+6 -as=${as_bigchain} -tab "${prefix}.bigchain.pre" ${size} "${prefix}.bigchain.bigbed"
bedToBigBed -type=bed4+1 -as=${as_biglink} -tab "${prefix}.link.pre" ${size} "${prefix}.link.bigbed"
