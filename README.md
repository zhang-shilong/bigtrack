# bigtrack

A lightweight Python package for creating UCSC Track Hubs with ease.

_Note: This package was primarily developed to generate track hubs for my previous publications. It has not been tested for production use._

## Installation

Build the latest version from source:

```bash
git clone https://github.com/zhang-shilong/bigtrack
cd bigtrack/
pip install .
```

## Usage

### Quick start

```python
import bigtrack

# generate a hub
hub = bigtrack.Hub(
    hub="ExampleHub",
    shortLabel="ExampleHub",
    longLabel="ExampleHub",
    email="example@email.com",
)

# make a genome
genome = bigtrack.Genome(
    genome="ExampleGenome",
    organism="Example Organism",
    scientificName="Example Organism",
    twoBitPath="/path/to/two/bit/file",
    chromSizes="/path/to/sizes/file",
    defaultPos="chr1:0-100000",
    orderKey=1,
    description="This is a example",
    htmlPath="/path/to/html/description",
)
hub.add_genome(genome)  # add the genome to hub

# make a group
group_map = bigtrack.Group(
    name="map",
    label="Mapping and Sequencing",
    priority=2,
)
genome.add_group(group_map)  # add the group to genome

# make a trackDb
trackDb_map = bigtrack.TrackDb(
    include="trackDb_map.txt",
)
genome.add_trackDb(trackDb_map)  # add the trackDb to genome

# make a track
track_ideogram = bigtrack.Track(
    track="cytoBandIdeo",
    shortLabel="Chromosome Band (Ideogram)",
    longLabel="Ideogram for Orientation",
    bigDataUrl="/path/to/track/file",
    type="bigBed 4 +",
    group="map",
)
trackDb_map.add_track(track_ideogram)  # add the track to trackDb

# finally, one function to generate the file structure
hub.generate()
```

Then, find your track hub under the `ExampleHub/` directory.

### Data structure

When `hub.generate()` runs, bigtrack writes a directory tree suitable for hosting as a UCSC Track Hub. The exact layout can be configured, but a typical generated structure looks like:

```
ExampleHub/
├─ hub.txt
├─ genomes.txt
├─ ExampleGenome/
│  ├─ groups.txt
│  ├─ trackDb.txt  # include all trackDbs
│  ├─ trackDb_map.txt
│  └─ trackDb_xxx.txt
└─ AnotherGenome/
   ├─ groups.txt
   ├─ trackDb.txt  # include all trackDbs
   ├─ trackDb_map.txt
   └─ trackDb_xxx.txt
```

You can host this directory on any web server (HTTP/HTTPS/FTP) and point UCSC Genome Browser at the `hub.txt` URL.

### Hub components

bigtrack models the standard UCSC hub components as Python classes. Each object has reserved keywords — those are required for correct hub generation. Some fields have sensible defaults. Below are the main components, their purpose and required keys. Please note, required keys may not consistent with UCSC guidance.

#### Hub

Top-level hub object. Represents `hub.txt`.

Required keys: `hub`, `shortLabel`, `longLabel`, `genomesFile` (default: `genomes.txt`), `email`.

#### Genome

Represents a genome entry (appears in `genomes.txt` and holds per-genome resources).

Required keys: `genome`, `trackDb` (default: `trackDb.txt`), `groups` (default: `groups.txt`), `organism`, `scientificName`.

#### Group

A logical grouping for tracks used for UI organization.

Required keys: `name`, `label`, `priority` (default: 1), `defaultIsClosed` (default: 0).

#### TrackDb

A container class that holds tracks and writes a trackDb file.

Required keys: `include`.

#### Track

Basic (atomic) track object.

Required keys: `track`, `parent` (default: `None`), `shortLabel`, `longLabel`, `type`.

To enhance usage, track collections are also available.

#### CompositeTrack

A composite track groups multiple subtracks that share the same type. See UCSC docs for [composite track settings](https://genome.ucsc.edu/goldenpath/help/trackDb/trackDbHub.html#Composite_Track_Settings).

Required keys: `track`, `compositeTrack` (default: `on`), `parent` (default: `None`), `shortLabel`, `longLabel`, `type`.

#### SampledCompositeTrack

A convenience helper that produces a sampled subset of a CompositeTrack automatically. Useful when you have many samples and want to produce a smaller subset for quick browsing.

```python
bigtrack.SampledCompositeTrack(
    full_track: bigtrack.CompositeTrack,
    number: int,  # number of sampled child tracks from full_track
    random_seed: int = 0,
    suffix: str = "_subset",
    **kwargs,  # kwargs to override
)
```

#### SuperTrack

A superTrack provides a higher-level container that can contain multiple composite tracks or plain tracks. See UCSC docs for [super track settings](https://genome.ucsc.edu/goldenpath/help/trackDb/trackDbHub.html#superTrack).

Required keys: `track`, `superTrack` (default: `on`), `parent` (default: `None`), `shortLabel`, `longLabel`.

### Example

See codes for [T2T Macaque Hub](./trackhubs/generate_T2TMacaqueHub.py).

## Todo

- [ ] Add pre-flight checks while generating hubs
- [ ] Add PyPi / conda support
- [ ] Add automatic format conversion

## Acknowledgement

Thanks to the Python package [trackhub](https://github.com/daler/trackhub).

## License

This project is licensed under the MIT License — see the [LICENSE](./LICENSE) file for details.
