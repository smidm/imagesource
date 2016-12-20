# Image Sequence Abstraction for Python

Video data can appear in different forms: bunch of files, a video file, a network stream etc. 
We provide an abstraction for ordered image sources that serve as an isolation from a specific source type.

The interface is simple:

```python
import imagesource

images = imagesource.VideoSource('tests/data/MOV02522.MPG')
img100 = images.get_image(100)
img101 = images.get_next_image()
images.rewind()
img000 = images.get_next_image()
images.write_images('out/%03d.png', 100)

images2 = imagesource.FilesSource('tests/data/frames/%03d.jpg')
# same interface as above ...
```

The basic sources are `VideoSource` and `FilesSource` for video files and sequences of image files respectively. The `TimedVideoSource` extracts frame timestamps from video files. The `SynchronizedSource` translates frame numbers using a table. This can be used for creating a synchronized set of sources.

For more examples see `tests/test.py`

## Installation

Install OpenCV 3.x with Python bindings and Numpy using a system package manager.

`$ pip install imagesource`

The `TimedVideoSource` requires `ffprobe` command from the `ffmpeg` suite.

## Testing

```
$ pip install nose
$ nosetests
```

## Writing Extensions

It is simple to write transparent image source wrappers that post-process image data from an underlying image source (e.g. background subtraction, radial distortion removal, ...). 

An example background subtracted image source:

```python
class BackgroundSubtractedSource(imagesource.ImageSource):
    def __init__(self, source):
        self.source = source
        self.bgs = cv2.createBackgroundSubtractorMOG2(...)

        def get_image(self, frame):
            img = self.source.get_image(frame)
            return self.bgs.apply(img)

        def get_next_image(self):
            img = self.source.get_next_image()
            return self.bgs.apply(img)

        def rewind(self):
            self.source.rewind()
```    
