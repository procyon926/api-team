#-*-coding:utf-8-*-
#!/usr/bin/python
import pyaudio
import wave
import sys
import time

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 11025
CHUNK = 11025*4 - 1000
RECORD_SECONDS = 10
try:
    WAVE_FILE = sys.argv[1]
except:
    print('File name is required as an argument.')
    sys.exit(1)

###
from poster.encode import multipart_encode, MultipartParam
from poster.streaminghttp import register_openers
import urllib2

url="https://api.webempath.net/v2/analyzeWav"
register_openers()
items = []

items.append(MultipartParam('apikey', "pRRD0_BLi6LtsfC92TyLtBOcwsuYyWMWnHXg6QGBXDY"))
###

iter = 0
audio = pyaudio.PyAudio()

frames = []
def callback(in_data, frame_count, time_info, status):
    global iter
    iter = iter + 1
    frames.append(in_data)
    print "check"
    wf = wave.open(WAVE_FILE + str(iter) + ".wav", 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(in_data)
    wf.close()

    print "check"
    '''items.append(MultipartParam.from_file('wav', WAVE_FILE))
    datagen, headers = multipart_encode(items)
    request = urllib2.Request(url, datagen, headers)
    response = urllib2.urlopen(request)

    if response.getcode() == 200:
        print(response.read())
    else:
        print("HTTP status %d" % (response.getcode()))'''
    return(None, pyaudio.paContinue)

stream = audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            input_device_index=0,
            frames_per_buffer=CHUNK,
            start=False,
            stream_callback=callback
        )

if __name__ == '__main__':
    stream.start_stream()
    time.sleep(RECORD_SECONDS)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    wf = wave.open(WAVE_FILE, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
