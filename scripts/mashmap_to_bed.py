#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
    print("Usage: python3 mashmap_to_bed.py <mashmap_file>", file=sys.stderr)
    sys.exit(1)

infile = sys.argv[1]

# Use non-interactive backend for matplotlib so script works headless
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


def percent_identity_to_rgb(percent_identity, min_percent_identity=80):
    """
    Map percent_identity (0-100) to an RGB string "R,G,B".
    - If percent_identity == 0 -> white "255,255,255"
    - If percent_identity < min_percent_identity -> pale yellow "255,255,220"
    - Else map linearly from min_percent_identity..100 to colormap YlOrRd
    """
    try:
        pid = float(percent_identity)
    except Exception:
        # fallback to white if cannot parse
        return "255,255,255"

    if pid == 0:
        return "255,255,255"
    if pid < min_percent_identity:
        return "255,255,220"

    cmap = plt.get_cmap("YlOrRd")
    norm = mcolors.Normalize(vmin=min_percent_identity, vmax=100.0)
    rgba = cmap(norm(pid))
    rgb = tuple(int(round(255 * x)) for x in rgba[:3])
    return f"{rgb[0]},{rgb[1]},{rgb[2]}"


with open(infile, "r") as fh:
    for line in fh:
        line = line.rstrip("\n")
        if not line:
            continue
        if line.startswith("#"):
            continue

        parts = line.split("\t")
        # Basic safety: need at least up to index 12 ideally
        if len(parts) < 13:
            # skip malformed lines
            continue

        try:
            chrom = parts[0]
            # original code used parts[2], parts[3] as start/end
            start = int(parts[2])
            end = int(parts[3])

            # percent identity: original: parts[12].split(':')[2]
            pid_field = parts[12]
            # try to robustly extract numeric part: if contains colon groups like x:y:z
            if ":" in pid_field:
                pid_tokens = pid_field.split(":")
                # choose last token if it's numeric, else try token[2] if exists
                if pid_tokens[-1].replace(".", "", 1).isdigit():
                    pid = float(pid_tokens[-1])
                elif len(pid_tokens) >= 3 and pid_tokens[2].replace(".", "", 1).isdigit():
                    pid = float(pid_tokens[2])
                else:
                    pid = float(pid_tokens[-1])  # may raise
            else:
                pid = float(pid_field)

            # Some tools report identity as fraction 0-1; convert to percent if needed
            if pid <= 1.0:
                pid *= 100.0

            # query interval info (used for name)
            q_chr = parts[5]
            q_start = int(parts[7])
            q_end = int(parts[8])

            score_str = f"{round(pid, 1)}"
            name = f"{q_chr}:{q_start}-{q_end}_{score_str}%"
            strand = "."
            thick_start = start
            thick_end = end

            score = int(round(10 * pid))  # follow original scaling

            rgb = percent_identity_to_rgb(pid)

            out_fields = [
                chrom,
                str(start),
                str(end),
                name,
                str(score),
                strand,
                str(thick_start),
                str(thick_end),
                rgb,
            ]
            print("\t".join(out_fields))
        except Exception:
            # if any parsing error occurs for this line, skip it silently or print to stderr
            # Uncomment next line to debug:
            # print("Warning: failed to parse line:", line, file=sys.stderr)
            continue
