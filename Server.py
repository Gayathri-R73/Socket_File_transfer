######################### RPi TO COMP ###########################

##SERVER PROGRAM (to be executed in RPi)##

import numpy as np
from skimage import img_as_ubyte
from skimage.color import rgb2gray
import cv2
import datetime
import argparse
import imutils
import torch
from time import sleep
from imutils.video import VideoStream
from CNN_NET import CNN_NET
import socket

def soc():
    s = socket.socket()
    local = socket.gethostname()  
    print(local)
    host= 'X.X.X.X'                 # IP of CLIENT
    port = 12345   
    s.connect((host,port))
    fnm = "to send.jpg"
    f = open(fnm,"rb")
    l = f.read(1024)

    while (l):
        print ('Sending...')
        s.send(l)
        l = f.read(1024)
    f.close()
    print ("Done Sending")
    s.shutdown(socket.SHUT_WR)
    print (s.recv(1024))
    print("Image transferred")
    s.close()

model=torch.load('last_hope.h5')
ap = argparse.ArgumentParser()
ap.add_argument("-p","--picamera",type=int,default=-1,help="RPi Camer should be used")
args = vars(ap.parse_args())

vs = VideoStream(usePiCamera=args["picamera"]>0).start()
sleep(2.0)

def ImagePreProcess(im_orig, fr):
    
  im_gray = rgb2gray(im_orig)
  img_gray_u8 = img_as_ubyte(im_gray)
  (thresh, im_bw) = cv2.threshold(img_gray_u8, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
  img_resized = cv2.resize(im_bw,(28,28))
  im_gray_invert = 255 - img_resized  
  im_final = im_gray_invert.reshape(1,1,28,28)
  im_final = torch.from_numpy(im_final)
  im_final = im_final.type('torch.FloatTensor')
  ans = model(im_final)
  ans = ans[0].tolist().index(max(ans[0].tolist()))
  a= "Predicted digit: "
  b= str(ans)
  c=a+b
  cv2.putText(fr, c, (70,270), cv2.FONT_HERSHEY_SIMPLEX,1, (12,66,144), 2)
  cv2.imwrite("to send.jpg", fr)
  soc()
  cv2.imshow('OUTPUT',fr)
  print('DNN predicted digit is: ',ans)
  
def main():
            
      while True:
        try:
          frame = vs.read()
          frame = imutils.resize(frame, width=400)
          
          #FRAME          
          cv2.imshow("Show the digit", frame)
          key = cv2.waitKey(1) & 0xFF
                    
          if key == ord("q"):
              
            break
            cv2.destroyAllWindows()
            vs.stop()
            
          ###################################
          ### PREDICTION WITH "t" COMMAND ###
            
          elif key == ord("t"):
            cv2.imwrite("num.jpg", frame)
            im_orig = cv2.imread("num.jpg")
            ImagePreProcess(im_orig, frame)
            
          else:
            pass
        
          ###################################
        
          '''
          #############################
          ### CONTINUOUS PREDICTION ###
          else:
              cv2.imwrite("num.jpg",frame)
              im_orig = cv2.imread("num.jpg")
              ImagePreProcess(im_orig, frame)
          ##############################
          '''
          
        except KeyboardInterrupt:
          cv2.destroyAllWindows()
          vs.stop()
       
if __name__=="__main__":
  main()


