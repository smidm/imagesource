from .base import ImageSource
import numpy as np


class SynchronizedSource(ImageSource):
    def __init__(self, source, frame_lookup_table=None, frame_synchronization_errors=None):
        self.source = source
        self.frame_lookup_table = frame_lookup_table
        self.frame_synchronization_errors = frame_synchronization_errors
        self.synchronized_next_position = 0

    def get_image(self, frame):
        self.synchronized_next_position = frame + 1
        idx = self.frame_lookup_table[frame]
        if idx == -1:
            return None
        return self.source.get_image(idx)

    def get_synchronization_error(self, frame):
        return self.frame_synchronization_errors[frame]

    def get_next_image(self):
        img = self.get_image(self.synchronized_next_position)
        return img

    def seek(self, next_frame):
        self.synchronized_next_position = next_frame

    def rewind(self):
        self.synchronized_next_position = 0
        self.source.rewind()
        
    def save(self, filename):
        np.savez(filename, **{'frame_lookup_table': self.frame_lookup_table,
                              'frame_synchronization_errors': self.frame_synchronization_errors})

    def load(self, filename):
        with np.load(filename) as data:
            self.frame_lookup_table = data['frame_lookup_table']
            self.frame_synchronization_errors = data['frame_synchronization_errors']
