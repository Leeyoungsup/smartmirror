import cv2
def Imagecapture(classcount):
    cap = cv2.VideoCapture(0)
    count=0
    while(count<200):
        ret, frame = cap.read() 
        dst = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        dst = cv2.resize(dst, (50,50), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite('class'+str(classcount)+'/'+str(count)+'.png',dst)
        count=count+1
    cap.release()
    cv2.destroyAllWindows()
while(True):
    a=input(':')
    if a=='1':
        Imagecapture(1)
    if a=='2':
        Imagecapture(2)
