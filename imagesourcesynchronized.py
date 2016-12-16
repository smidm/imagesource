from imagesourcevideo import ImageSourceVideo


class ImageSourceSynchronized(ImageSourceVideo):
    def __init__(self, filename, frame_lookup_table, frame_synchronization_errors, mask=None):
        super(ImageSourceSynchronized, self).__init__(filename, mask)
        self.frame_lookup_table = frame_lookup_table
        self.frame_synchronization_errors = frame_synchronization_errors
        self.synchronized_next_position = 0

    def get_image(self, frame, bgr=False):
        self.synchronized_next_position = frame + 1
        idx = self.frame_lookup_table[frame]
        if idx == -1:
            return None
        return super(ImageSourceSynchronized, self).get_image(idx, bgr)

    def get_synchronization_error(self, frame):
        return self.frame_synchronization_errors[frame]

    def get_next_image(self, bgr=False):
        idx = self.frame_lookup_table[self.synchronized_next_position]
        if idx == -1:
            return None
        img = super(ImageSourceSynchronized, self).get_image(idx, bgr)
        self.synchronized_next_position += 1
        return img

    def seek(self, next_frame):
        self.synchronized_next_position = next_frame

    def rewind(self):
        self.synchronized_next_position = 0
        super(ImageSourceSynchronized).rewind()
