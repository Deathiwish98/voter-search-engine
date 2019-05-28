import win32api
def hash(s):
    s = bytearray(s.encode("utf-8"))

    import hashlib
    m = hashlib.sha256(s)
    return m.hexdigest()

from uuid import getnode as getMac

mac = getMac()
#print(hash("jatin"))

i=1

while hash( str(mac) + str(i) + str(win32api.GetVolumeInformation("C:\\")[1] +
                                    win32api.GetVolumeInformation("C:\\")[2] +
                                    win32api.GetVolumeInformation("C:\\")[3]) + "B|)$*123")[0:4] != "0000":
    i += 1
print(i)

input("Press any key to exit")

