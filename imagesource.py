from abc import ABCMeta, abstractmethod
import cv2


class ImageSource(object):
    __metaclass__ = ABCMeta

    def __init__(self, mask=None):
        """

        :param mask: mask for output images
        :type mask: np.ndarray, dtype=bool
        """
        self.mask = mask

    def mask_image(self, img):
        if self.mask is None:
            return img
        else:
            return cv2.bitwise_and(img, self.mask)

    @abstractmethod
    def get_image(self, frame):
        pass

    @abstractmethod
    def get_next_image(self):
        pass

    @abstractmethod
    def rewind(self):
        pass

    def write_images(self, out_format, n_frames, start=0):
        for frame in xrange(start, start + n_frames):
            if frame % 100 == 0:
                print('writing frame ' + str(frame - start) + ' / ' + str(n_frames))
            filename = out_format % frame
            err = cv2.imwrite(out_format % frame, cv2.cvtColor(self.get_image(frame), cv2.COLOR_RGB2BGR))
            if not err:
                raise IOError('Can''t write ' + filename)


