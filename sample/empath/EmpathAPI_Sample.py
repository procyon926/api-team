from poster.encode import multipart_encode, MultipartParam
from poster.streaminghttp import register_openers
import urllib2

url="https://api.webempath.net/v2/analyzeWav"
register_openers()
items = []
items.append(MultipartParam('apikey', "pRRD0_BLi6LtsfC92TyLtBOcwsuYyWMWnHXg6QGBXDY"))
items.append(MultipartParam.from_file('wav', "./sample.wav"))
datagen, headers = multipart_encode(items)
request = urllib2.Request(url, datagen, headers)
response = urllib2.urlopen(request)

if response.getcode() == 200:
    print(response.read())
else:
    print("HTTP status %d" % (response.getcode()))
