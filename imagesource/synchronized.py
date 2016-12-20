from .base import ImageSource


class SynchronizedSource(ImageSource):
    def __init__(self, source, frame_lookup_table, frame_synchronization_errors):
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
        idx = self.frame_lookup_table[self.synchronized_next_position]
        if idx == -1:
            return None
        img = self.get_image(idx)
        self.synchronized_next_position += 1
        return img

    def seek(self, next_frame):
        self.synchronized_next_position = next_frame

    def rewind(self):
        self.synchronized_next_position = 0
        self.source.rewind()
        
    def write_images(self, out_format, n_frames, start=0):
        self.source.write_images(out_format, n_frames, start)
