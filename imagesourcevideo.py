from imagesource import ImageSource
import cv2
try:
    import pyvideocaptureas
    VideoCapture = pyvideocaptureas.VideoCaptureAS
    has_fast_seeking = True
except ImportError:
    VideoCapture = cv2.VideoCapture
    has_fast_seeking = False
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
        self.stream = None
        self.next_position = None
        self.frame_count = None
        self.seek_table_filename = None
        self.__init_stream__()

    def __init_stream__(self):
        if self.filename is not None:
            self.stream = VideoCapture(self.filename)
            self.frame_count = self.stream.get(cv2.CAP_PROP_FRAME_COUNT)
            frame_cache = os.path.splitext(self.filename)[0] + '.framecache'
            if has_fast_seeking and os.path.exists(frame_cache):
                if not self.stream.loadKeyFrameCache(frame_cache):
                    warn('unable to load framecache: ' + frame_cache)
                else:
                    print('framecache ' + frame_cache + ' loaded')
            else:
                print('framecache not found in ' + frame_cache + '\ncreating new framecache')
                self.stream.registerKeyFrames()
                if not self.stream.saveKeyFrameCache(frame_cache):
                    warn('unable to save framecache to ' + frame_cache)

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
        self.seek_table_filename = seek_table_filename
        return True

    def get_image(self, frame, bgr=False):
        if frame >= self.frame_count:
            raise IOError
        if self.stream.set(cv2.CAP_PROP_POS_FRAMES, frame):  # in more recent versions cv2.CAP_PROP_POS_FRAMES
            if not has_fast_seeking:
                warn('opencv seek is not frame accurate')
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
        self.next_position = 0
        if not self.stream.set(cv2.CAP_PROP_POS_FRAMES, 0):
            warn('opencv seek unsuccessful, reopening stream')
            self.__init_stream__()

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['stream']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        next_position = self.next_position
        self.__init_stream__()
        self.seek(next_position)
        if self.seek_table_filename:
            self.init_seeking(self.seek_table_filename)


