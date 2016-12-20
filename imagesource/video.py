from .base import ImageSource
import cv2
try:
    # not released code
    import pyvideocaptureas
    VideoCapture = pyvideocaptureas.VideoCaptureAS
    has_fast_seeking = True
except ImportError:
    VideoCapture = cv2.VideoCapture
    has_fast_seeking = False
import os.path
from warnings import warn
import copy


class VideoSource(ImageSource):

    def __init__(self, filename, mask=None):
        '''
        :param filename: video file definition
        :type filename: str
        '''
        super(VideoSource, self).__init__(mask)
        self.filename = filename
        self.stream = None
        self.next_position = None
        self.frame_count = None
        self.seek_table_filename = None
        self.accurate_slow_seek = True
        self.__init_stream__()

    def __init_stream__(self):
        if self.filename is not None:
            self.stream = VideoCapture(self.filename)
            self.frame_count = self.stream.get(cv2.CAP_PROP_FRAME_COUNT)
            if self.frame_count == -1:
                self.frame_count = float('inf')          
            if has_fast_seeking:
                self.seek_table_filename = os.path.splitext(self.filename)[0] + '.framecache'
                if not self.init_accurate_seek():
                    warn('problem loading or saving seek table: ' + self.seek_table_filename)

        self.next_position = 0
        
    def init_accurate_seek(self):
        if not os.path.exists(self.seek_table_filename):
            print('creating seek table...')
            self.stream.registerKeyFrames()
            if not self.stream.saveKeyFrameCache(self.seek_table_filename):
                return False
        else:
            if not self.stream.loadKeyFrameCache(self.seek_table_filename):
                return False
        return True        

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

    def get_image(self, frame):
        self.seek(frame)
        return self.__get_next_image__()        

    def get_next_image(self):
        return self.__get_next_image__()

    def __get_next_image__(self):
        retval, img = self.stream.read()
        if not retval:
            raise IOError
        self.next_position += 1
        if self.color_conversion_from_bgr is not None:
            img = cv2.cvtColor(img, self.color_conversion_from_bgr)
        return self.mask_image(img)

    def seek(self, next_frame):
        if next_frame >= self.frame_count:
            raise IOError        
        if has_fast_seeking:
            self.stream.set(cv2.CAP_PROP_POS_FRAMES, next_frame)
        elif self.accurate_slow_seek:
            self.__slow_accurate_seek__(next_frame)
        else:
            if self.stream.set(cv2.CAP_PROP_POS_FRAMES, next_frame):
                warn('opencv seek is not frame accurate')
            else:
                warn('opencv seek unsuccessful, using slow seek method')
                self.__slow_accurate_seek__(next_frame)            
            
    def __slow_accurate_seek__(self, next_frame):
        if self.next_position > next_frame:
            self.rewind()
        while self.next_position < next_frame:
            self.__get_next_image__()

    def rewind(self):
        self.next_position = 0
        if not self.stream.set(cv2.CAP_PROP_POS_FRAMES, 0):
            # seek to start unsuccessful, reopening stream
            self.__init_stream__()

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['stream']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        next_position = self.next_position
        self.__init_stream__()
        if self.seek_table_filename:
            self.init_seeking()
        self.seek(next_position)

