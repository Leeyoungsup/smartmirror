import time
f = open("calender.txt", 'r')
caly1=''
def calender():
    global caly1,f
    caly=f.readline()
    if caly[:8]==time.strftime("%y/%m/%d"):
        caly1=caly1+caly[9:]
    return caly1
