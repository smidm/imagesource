from .base import ImageSource
import os.path
import exceptions
import cv2


class FilesSource(ImageSource):
    def __init__(self, file_name_template, mask=None):
        super(FilesSource, self).__init__(mask)
        self.file_name_template = file_name_template
        assert os.path.exists(self.file_name_template % 0), 'sequence should start with index 0'
        self.next_position = 0

    def get_image(self, frame):
        filename = self.file_name_template % frame
        self.next_position = frame + 1
        if not os.path.exists(filename):
            raise exceptions.IOError('Can''t open file ' + filename)
        else:
            img = cv2.imread(filename)
            if self.color_conversion_from_bgr is not None:
                img = cv2.cvtColor(img, self.color_conversion_from_bgr)
            return self.mask_image(img)

    def get_next_image(self):
        return self.get_image(self.next_position)

    def rewind(self):
        self.next_position = 0



