#!/usr/bin/env python3

import random
from .track import Track


class SampledTrack(Track):

    def __init__(self, full_track: Track, number: int, random_seed: int = 0, **kwargs):

        super().__init__(**self.full_track.kwargs)
        self.parent = full_track.parent
        random.seed(random_seed)
        self.children = random.sample(full_track.tracks, k=number)
        
        for k, v in kwargs.items():
            self.kwargs[k] = v
