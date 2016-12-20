from .video import VideoSource
from joblib import Memory
import subprocess
import numpy as np
import json
from warnings import warn

memory = Memory(cachedir='.', verbose=0)


@memory.cache
def extract_timestamps(filename, duration_s):
    # throws CalledProcessError
    ffprobe_cmd = 'ffprobe -hide_banner -select_streams v -show_entries ' \
                  'frame=best_effort_timestamp_time -of json'
    if duration_s:
        ffprobe_cmd += ' -read_intervals %%%d' % duration_s
    ffprobe_output = subprocess.check_output(ffprobe_cmd.split() + [filename]).decode('utf8')
    ffprobe_timestamps = json.loads(ffprobe_output)
    if 'frames' not in ffprobe_timestamps:
        warn('no frames section in ffprobe output')
        return None          
            
    # last entry may be missing
    if ffprobe_timestamps['frames'][-1] == {}:
        ffprobe_timestamps['frames'] = ffprobe_timestamps['frames'][:-1]
    
    timestamps = [float(frame['best_effort_timestamp_time'])
                  for frame in ffprobe_timestamps['frames']]
    return np.array(timestamps) * 1000.


class TimedVideoSource(VideoSource):
    def __init__(self, filename, mask=None):
        super(TimedVideoSource, self).__init__(filename, mask)
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
