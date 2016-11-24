# requirements:
# opencv
from imagesource import ImageSource
import cv2
try:
    import pyvideocaptureas
    VideoCapture = pyvideocaptureas.VideoCaptureAS
except ImportError:
    VideoCapture = cv2.VideoCapture
import os.path
from warnings import warn
import copy


class ImageSourceVideo(ImageSource):

    def __init__(self, filename, mask=None):
        '''
        :param filename: video file definition
        :type filename: str
        '''
        super(ImageSourceVideo, self).__init__(mask)
        self.filename = filename
        self.stream = {}
        self.next_position = {}
        self.frame_count = {}
        self.__init_stream__()

    def __init_stream__(self):
        if self.filename is not None:
            self.stream = VideoCapture(self.filename)
            self.frame_count = self.stream.get(cv2.CAP_PROP_FRAME_COUNT)
        self.next_position = 0

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, copy.deepcopy(v, memo))
        result.__init_stream__()
        return result

    def init_seeking(self, seek_table_filename):
        if not os.path.exists(seek_table_filename):
            print('creating seek table...')
            self.stream.registerKeyFrames()
            if not self.stream.saveKeyFrameCache(seek_table_filename):
                return False
        else:
            if not self.stream.loadKeyFrameCache(seek_table_filename):
                return False
        return True

    def get_image(self, frame, bgr=False):
        if frame >= self.frame_count:
            raise IOError
        if self.stream.set(cv2.CAP_PROP_POS_FRAMES, frame):  # in more recent versions cv2.CAP_PROP_POS_FRAMES
            # cv2.cv.CV_CAP_PROP_POS_FRAMES
            self.next_position = frame
            return self.__get_next_image__(bgr)
        else:
            # code above doesn't work all the time
            warn('opencv seek unsuccessful, using slower method')
            assert self.next_position <= frame
            while self.next_position <= frame:
                img = self.__get_next_image__(bgr)
            return img

    def get_next_image(self, bgr=False):
        return self.__get_next_image__(bgr)

    def __get_next_image__(self, bgr=False):
        retval, img = self.stream.read()
        if not retval:
            raise IOError
        self.next_position += 1
        if not bgr:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return self.mask_image(img)

    def seek(self, next_frame):
        if next_frame == 0:
            self.rewind()
        else:
            self.get_image(next_frame - 1)

    def rewind(self):
        if not self.stream.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, 0):
            warn('opencv seek unsuccessful, reopening stream')
            self.__init_stream__()

