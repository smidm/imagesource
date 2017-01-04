from .base import ImageSource
import cv2


class StaticSource(ImageSource):
    def __init__(self, file_name, mask=None):
        super(StaticSource, self).__init__(mask)
        self.file_name = file_name
        self.img = cv2.imread(self.file_name)
        assert self.img is not None, 'Can''t load image ' + self.file_name

    def get_image(self, frame):
        if self.color_conversion_from_bgr is not None:
            img = cv2.cvtColor(self.img, self.color_conversion_from_bgr)
        else:
            img = self.img
        return self.mask_image(img)

    def get_next_image(self):
        return self.get_image(0)

    def rewind(self):
        pass



