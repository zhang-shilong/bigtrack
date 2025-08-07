#!/usr/bin/env python3

from bigtrack import Hub
from bigtrack import Genome


hub = Hub(
    hub="example",
    shortLabel="Example Hub",
    longLabel="Example Hub",
    email="example@example.com",
)

print(hub.format())

genome1 = Genome(
    genome="ExampleGenome1",
    organism="Big Track",
    scientificName="Big Track",
)

print(genome1.format())

hub.add_genome(genome1)
hub.generate()
