from .base import ImageSource
import os.path
import exceptions
import cv2


class FilesSource(ImageSource):
    def __init__(self, file_name_template, mask=None,
                 color_flag=cv2.COLOR_BGR2RGB):
        super(FilesSource, self).__init__(mask)
        self.file_name_template = file_name_template
        self.next_position = 0
        self.color_flag = color_flag

    def get_image(self, frame):
        filename = self.file_name_template % frame
        self.next_position = frame + 1
        if not os.path.exists(filename):
            raise exceptions.IOError('Can''t open file ' + filename)
        else:
            return self.mask_image(cv2.cvtColor(cv2.imread(filename), self.color_flag))

    def get_next_image(self):
        return self.get_image(self.next_position)

    def rewind(self):
        self.next_position = 0



