from imagesourcevideo import ImageSourceVideo
from joblib import Memory
import subprocess
import numpy as np

memory = Memory(cachedir='.', verbose=0)


@memory.cache
def extract_timestamps(filename, duration_s):
    # throws CalledProcessError
    ffprobe_cmd = 'ffprobe -select_streams v -show_frames -show_entries ' \
                  'frame=best_effort_timestamp_time %s -of csv' % filename
    if duration_s:
        ffprobe_cmd += ' -read_intervals %%%d' % duration_s
    ffprobe_csv = subprocess.check_output(ffprobe_cmd.split()).decode('utf8')
    ffprobe_timestamps = np.recfromcsv(ffprobe_csv.split('\n'), usecols=1,
                                       names='best_effort_timestamp_time')
    return ffprobe_timestamps['best_effort_timestamp_time'] * 1000.


class ImageSourceTimedVideo(ImageSourceVideo):
    def __init__(self, filename, mask=None):
        super(ImageSourceTimedVideo, self).__init__(filename, mask)
        self.timestamps_ms = None  # e.g. array([    0.,    40.,    80.,   120., ...])

    def extract_timestamps(self, duration_s=None):
        self.timestamps_ms = extract_timestamps(self.filename, duration_s)

    def get_frame_for_time(self, time_ms):
        assert self.timestamps_ms is not None
        idx = np.searchsorted(self.timestamps_ms, time_ms)
        assert abs(self.timestamps_ms[idx] - time_ms) < 1000  # out of timestamps_ms range
        if idx == 0:
            return idx
        if abs(self.timestamps_ms[idx] - time_ms) > abs(self.timestamps_ms[idx - 1] - time_ms):
            return idx
        else:
            return idx - 1