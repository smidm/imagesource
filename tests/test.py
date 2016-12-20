# -*- coding: utf-8 -*-
import imagesource
import hashlib
import cv2
import tempfile
import os.path
import shutil
from nose.tools import eq_

files_template = 'tests/data/frames/%03d.jpg'
video = 'tests/data/MOV02522.MPG'


def test_files():
    hashes_rgb = {}
    hashes_bgr = {}
    for i in xrange(10):
        filename = files_template % i
        img = cv2.imread(filename)        
        assert img is not None, 'Can''t load ' + filename
        hashes_bgr[i] = hashlib.md5(img).hexdigest()
        hashes_rgb[i] = hashlib.md5(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)).hexdigest()

    images = imagesource.FilesSource(files_template)
    img = images.get_image(2)
    eq_(hashlib.md5(img).hexdigest(), hashes_rgb[2])
    img = images.get_next_image()
    eq_(hashlib.md5(img).hexdigest(), hashes_rgb[3])
    images.rewind()
    img = images.get_next_image()
    eq_(hashlib.md5(img).hexdigest(), hashes_rgb[0])
    
    images.color_conversion_from_bgr = None    
    img = images.get_image(2)
    eq_(hashlib.md5(img).hexdigest(), hashes_bgr[2])
    img = images.get_next_image()
    eq_(hashlib.md5(img).hexdigest(), hashes_bgr[3])
    images.rewind()
    img = images.get_next_image()
    eq_(hashlib.md5(img).hexdigest(), hashes_bgr[0])

    # tmp_dir = tempfile.TemporaryDirectory()  # from Python 3.2
    # tmp_dir.name
    tmp_dir = tempfile.mkdtemp()
    tmp_file_template = os.path.join(tmp_dir, '%03d.png')
    images.write_images(tmp_file_template, 10)
    for i in xrange(10):
        filename = tmp_file_template % i
        img = cv2.imread(filename)
        eq_(hashlib.md5(img).hexdigest(), hashes_bgr[i])
    shutil.rmtree(tmp_dir)  # not needed with tempfile.TemporaryDirectory()


def test_video():
    hashes_rgb = {}
    hashes_bgr = {}
    cap = cv2.VideoCapture(video)
    for i in xrange(10):
        retval, img = cap.read()
        assert retval
        hashes_bgr[i] = hashlib.md5(img).hexdigest()
        hashes_rgb[i] = hashlib.md5(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)).hexdigest()

    images = imagesource.VideoSource(video)
    img = images.get_image(2)
    eq_(hashlib.md5(img).hexdigest(), hashes_rgb[2])
    img = images.get_next_image()
    eq_(hashlib.md5(img).hexdigest(), hashes_rgb[3])
    images.rewind()
    img = images.get_next_image()
    eq_(hashlib.md5(img).hexdigest(), hashes_rgb[0])
    
    images.accurate_slow_seek = True
    img = images.get_image(8)
    eq_(hashlib.md5(img).hexdigest(), hashes_rgb[8])
    img = images.get_image(7)
    eq_(hashlib.md5(img).hexdigest(), hashes_rgb[7])

    images.accurate_slow_seek = False
    img = images.get_image(8)
    # eq_(hashlib.md5(img).hexdigest(), hashes_rgb[8]) # the images may differ
    img = images.get_image(7)
    # eq_(hashlib.md5(img).hexdigest(), hashes_rgb[7]) # the images may differ
    
    images.accurate_slow_seek = True
    images.color_conversion_from_bgr = None    
    img = images.get_image(2)
    eq_(hashlib.md5(img).hexdigest(), hashes_bgr[2])
    img = images.get_next_image()
    eq_(hashlib.md5(img).hexdigest(), hashes_bgr[3])
    images.rewind()
    img = images.get_next_image()
    eq_(hashlib.md5(img).hexdigest(), hashes_bgr[0])

    # tmp_dir = tempfile.TemporaryDirectory()  # from Python 3.2
    # tmp_dir.name
    tmp_dir = tempfile.mkdtemp()
    tmp_file_template = os.path.join(tmp_dir, '%03d.png')
    images.write_images(tmp_file_template, 10)
    for i in xrange(10):
        filename = tmp_file_template % i
        img = cv2.imread(filename)
        eq_(hashlib.md5(img).hexdigest(), hashes_bgr[i])
    shutil.rmtree(tmp_dir)  # not needed with tempfile.TemporaryDirectory()
    
       
def test_timedvideo(): 
    images = imagesource.TimedVideoSource(video)
    images.extract_timestamps()
    assert images.timestamps_ms is not None


# def test_mass_timedvideo():
#     import fnmatch
#     import os
#
#     matches = []
#     for root, dirnames, filenames in os.walk('...somepath...'):
#         for filename in fnmatch.filter(filenames, '*.avi'):
#             matches.append(os.path.join(root, filename))
#         for filename in fnmatch.filter(filenames, '*.AVI'):
#             matches.append(os.path.join(root, filename))
#         for filename in fnmatch.filter(filenames, '*.mp4'):
#             matches.append(os.path.join(root, filename))
#         for filename in fnmatch.filter(filenames, '*.MP4'):
#             matches.append(os.path.join(root, filename))
#
#     for video_file in matches:
#         print video_file
#         images = imagesource.TimedVideoSource(video_file)
#         images.extract_timestamps()
#         assert images.timestamps_ms is not None
#         print images.timestamps_ms[:30]

def test_synchronized():
    hashes_rgb = {}
    for i in xrange(10):
        filename = files_template % i
        img = cv2.imread(filename)
        assert img is not None, 'Can''t load ' + filename
        hashes_rgb[i] = hashlib.md5(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)).hexdigest()

    images = imagesource.FilesSource(files_template)
    frame_lookup_table = [0, 2, 4, 6, 8]
    errors = [10, 20, 30, 40, 50]
    images_synchronized = imagesource.SynchronizedSource(images, frame_lookup_table, errors)

    img = images_synchronized.get_image(0)
    eq_(hashlib.md5(img).hexdigest(), hashes_rgb[0])
    eq_(images_synchronized.get_synchronization_error(0), 10)

    img = images_synchronized.get_image(1)
    eq_(hashlib.md5(img).hexdigest(), hashes_rgb[2])
    eq_(images_synchronized.get_synchronization_error(1), 20)

    img = images_synchronized.get_image(4)
    eq_(hashlib.md5(img).hexdigest(), hashes_rgb[8])
    eq_(images_synchronized.get_synchronization_error(4), 50)






