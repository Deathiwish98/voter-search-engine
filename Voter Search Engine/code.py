import win32api
def hash(s):
    s = bytearray(s.encode("utf-8"))

    import hashlib
    m = hashlib.sha256(s)
    return m.hexdigest()


from uuid import getnode as getMac


mac = getMac()

i = 1

while hash( str(mac) + str(i) + str(win32api.GetVolumeInformation("C:\\")[1] +
                                    win32api.GetVolumeInformation("C:\\")[2] +
                                    win32api.GetVolumeInformation("C:\\")[3]) + "B|)$*123")[0:4] != "0000":
    i += 1

file = open("C:\Windows\System32\kwin64.dll", "w")
file.write(str(i))
file.close()
print(i)

input("Press any key to exit")

