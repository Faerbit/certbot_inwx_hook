import xmlrpc.client
from xmlrpc.client import _Method
import urllib.request, urllib.error, urllib.parse
import base64
import struct
import time
import hmac
import hashlib
import platform

class domrobot ():
    def __init__ (self, address, debug = False):
        self.url = address
        self.debug = debug
        self.cookie = None
        self.version = "1.0"

    def __getattr__(self, name):
        return _Method(self.__request, name)

    def __request (self, methodname, params):
        tuple_params = tuple([params[0]])
        requestContent = xmlrpc.client.dumps(tuple_params, methodname)
        if(self.debug == True):
            print("Request: "+str(requestContent))
        headers = { 'User-Agent' : 
                'DomRobot/'+self.version+' Python-v'+platform.python_version(), 
                'Content-Type': 'text/xml',
                'content-length': str(len(requestContent))}
        if(self.cookie!=None):
            headers['Cookie'] = self.cookie

        req = urllib.request.Request(self.url, bytearray(requestContent,
            'ascii'), headers)

        response = urllib.request.urlopen(req)
        responseContent = response.read()

        cookies = response.getheader('Set-Cookie')

        if(self.debug == True):
            print("Response: " + responseContent.decode("utf-8"))
        apiReturn = xmlrpc.client.loads(responseContent)
        apiReturn = apiReturn[0][0]
        if (apiReturn["code"] == 2200 and
                "Authentication error" in apiReturn["msg"]):
            raise NameError("Unable to log in. Check your login configuration")
            return False
        if(apiReturn["code"]!=1000):
            raise NameError(f"There was a problem: {apiReturn['msg']} "
                    f"(Error code {apiReturn['code']})")
            return False

        if(cookies!=None):
                cookies = response.getheader('Set-Cookie')
                self.cookie = cookies
                if(self.debug == True):
                    print(("Cookie: " + self.cookie))
        return apiReturn

