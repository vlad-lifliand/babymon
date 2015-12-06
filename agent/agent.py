import array
import datetime
import optparse
import pyaudio
import requests

_FORMAT = pyaudio.paInt16
_RATE = 8000
_CHUNK_SIZE = _RATE / 2
_SEGMENT_LENGTH = 30  # seconds
_NORMALIZATION_FACTOR = 50

class AudioProcessor(object):
  
  def __init__(self):
    self.audio = pyaudio.PyAudio()

  def RecordSegment(self):
    '''Records a single segment of audio and returns the average level.
    
    Returns:
      Average volume level as float, where 0 is absolute silence and 1 is
      maximum amount of noise.
    '''
    stream = self.audio.open(format=_FORMAT, channels=1, rate=_RATE,
                             input=True, frames_per_buffer=_CHUNK_SIZE)
  
    try:    
      total_chunks = _SEGMENT_LENGTH * _RATE // _CHUNK_SIZE
      level = 0
      for unused_i in range(total_chunks):
        data = array.array('h', stream.read(_CHUNK_SIZE))
        level += sum(map(abs, data)) / (len(data) * total_chunks * 16384.0)
      
      return min(1.0, level * _NORMALIZATION_FACTOR)
    finally:
      stream.stop_stream()
      stream.close()


if __name__ == '__main__':
  parser = optparse.OptionParser(usage='agent.py <options>')
  parser.add_option('--url', metavar='URL', dest='url',
                    help='URL of the reporting service')
  
  (options, args) = parser.parse_args()
  
  audio_processor = AudioProcessor()
  while True:
    level = audio_processor.RecordSegment()
    print('{}: Average audio level: {}'.format(datetime.datetime.now(), level))
    
    if options.url:
      response = requests.post(options.url, data={'level': level})
      if response.status_code != requests.codes.ok:
        print('Failed to post status update: %s' % response)
      else:
        print('Posted to backend successfully')
