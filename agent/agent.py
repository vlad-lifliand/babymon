from sys import byteorder
from array import array
from struct import pack

import pyaudio
import wave

_CHUNK_SIZE = 1024
_FORMAT = pyaudio.paUInt8
_RATE = 9600
_SEGMENT_LENGTH = 30  # seconds

class AudioProcessor(object):
  
  def __init__(self):
    self.audio = pyaudio.PyAudio()

  def RecordSegment():
      """Records a single segment of audio and returns the average level.
      
      Returns:
        Average volume level as float, where 0 is absolute silence and 1 is
        maximum amount of noise.
  """
  stream = self.audio.open(format=FORMAT, channels=1, rate=RATE,
                           input=True, output=True,
                           frames_per_buffer=CHUNK_SIZE)

  try:    
    total_chunks = _SEGMENT_LENGTH * _RATE // _CHUNK_SIZE
    level = 0
    for unused_i in range(total_chunks):
      data = array('B', stream.read(_CHUNK_SIZE))
      level += sum(data) / float(len(data) * total_chunks)
    
    return level
  finally:
    stream.stop_stream()
    stream.close()


if __name__ == '__main__':
  audio_processor = AudioProcessor()
  while True:
    level = audio_processor.RecordSegment()
    print 'Average audio level: %f' % level
