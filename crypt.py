import os
import base64
import config
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.kbkdf import \
(CounterLocation, KBKDFHMAC, Mode)
from cryptography.hazmat.backends import default_backend


class Disenchant(object):
  def __getSerialNum(self,file_location):
    found = False 
    with open(file_location,'r') as fileobj:
      for line in fileobj:
        if line.__contains__('Serial'):
          found = True
          break
      if found:
        return line[len(line)-17:len(line)-1]
      else:
        return ''
      
  def __genKey(self):
    label = "!There is the sun label"
    context = "!There is the sun context"
    kdf = KBKDFHMAC(algorithm=hashes.SHA256(),\
    mode=Mode.CounterMode,length=32,\
    rlen=4,\
    llen=4,\
    location=CounterLocation.BeforeFixed,\
    label=label,\
    context=context,\
    fixed=None,\
    backend=default_backend())
    return base64.urlsafe_b64encode(kdf.derive(self.__getSerialNum(config.serN_file_location)))
  
  def getDBpassword(self):
    file_location = "passes\pi"+str(config.RPI_ID())+"_pass.bin"
    fileobj = open(file_location,'rb')
    string = fileobj.read(-1)
    fileobj.close()
    key = self.__genKey()
    f = Fernet(key)
    token = f.decrypt(string)
    return token
    
