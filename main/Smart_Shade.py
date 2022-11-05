import RPi.GPIO as GPIO
import spidev
from time import sleep
import Adafruit_PCA9685
import Adafruit_DHT
# from RPLCD.i2c import CharLCD
# lcd=CharLCD('PCF8574',0x27)

robot_handle = Adafruit_PCA9685.PCA9685()
servoMin = 150
servoMax = 550

out1 = 11
out2 = 13
out3 = 15
out4 = 12

i=0
positive=0
negative=0
y=0


sensor = Adafruit_DHT.DHT11
pin = 4


GPIO.setmode(GPIO.BOARD)
GPIO.setup(out1,GPIO.OUT)
GPIO.setup(out2,GPIO.OUT)
GPIO.setup(out3,GPIO.OUT)
GPIO.setup(out4,GPIO.OUT)


anglelr = 0
angletb = 0
angletb1 = 180


def map(value,min_angle,max_angle,min_pulse,max_pulse):
    angle_range = max_angle-min_angle
    pulse_range = max_pulse-min_pulse
    scale_factor = float(angle_range)/float(pulse_range)
    return min_pulse+(value/scale_factor)
    #pulse value and motor angle  mapping
    

def set_angle(channel,angle):
    pulse = int(map(angle,0,180,servoMin,servoMax))
    robot_handle.set_pwm(channel,0,pulse)
    #motor turn
    
    robot_handle.set_pwm_freq(50)





def analog_read(channel):
    r = spi.xfer2([1, (8 + channel) << 4, 0])

    adc_out = ((r[1]&3) << 8) + r[2]

    return adc_out

if __name__ == "__main__":
    spi = spidev.SpiDev()

    spi.open(0,0)

    spi.max_speed_hz=1350000
    
    
GPIO.output(out1,GPIO.LOW)
GPIO.output(out2,GPIO.LOW)
GPIO.output(out3,GPIO.LOW)
GPIO.output(out4,GPIO.LOW)
set_angle(0,0)
set_angle(15,180)
set_angle(2,0)
set_angle(3,0) #first value       
    

    
while True:

    
    
    wind_data = analog_read(4)
    wind_speed = float(wind_data*3.3/1023)*25
    
    h,t = Adafruit_DHT.read_retry(sensor, pin)
    
    if h is not None and t is not None :
        print("Temperature = {0:0.1f}*C Humidity = {1:0.1f}%".format(t, h))
    else :
        print('Read error')
            

    print("data = %.3f m/s \t"%(wind_speed))
    
    
    
   
    
    if wind_speed <= 0.2 and t>15:
        for y in range(800,0,-1):
              if negative==1:
                  if i==7:
                      i=0
                  else:
                      i=i+1
                  y=y+2
                  negative=0
              positive=1
              #print((x+1)-y)
              if i==0:
                  GPIO.output(out1,GPIO.HIGH)
                  GPIO.output(out2,GPIO.LOW)
                  GPIO.output(out3,GPIO.LOW)
                  GPIO.output(out4,GPIO.LOW)
                  sleep(0.01)
                  #time.sleep(1)
              elif i==1:
                  GPIO.output(out1,GPIO.HIGH)
                  GPIO.output(out2,GPIO.HIGH)
                  GPIO.output(out3,GPIO.LOW)
                  GPIO.output(out4,GPIO.LOW)
                  sleep(0.01)
                  #time.sleep(1)
              elif i==2:  
                  GPIO.output(out1,GPIO.LOW)
                  GPIO.output(out2,GPIO.HIGH)
                  GPIO.output(out3,GPIO.LOW)
                  GPIO.output(out4,GPIO.LOW)
                  sleep(0.01)
                  #time.sleep(1)
              elif i==3:    
                  GPIO.output(out1,GPIO.LOW)
                  GPIO.output(out2,GPIO.HIGH)
                  GPIO.output(out3,GPIO.HIGH)
                  GPIO.output(out4,GPIO.LOW)
                  sleep(0.01)
                  #time.sleep(1)
              elif i==4:  
                  GPIO.output(out1,GPIO.LOW)
                  GPIO.output(out2,GPIO.LOW)
                  GPIO.output(out3,GPIO.HIGH)
                  GPIO.output(out4,GPIO.LOW)
                  sleep(0.01)
                  #time.sleep(1)
              elif i==5:
                  GPIO.output(out1,GPIO.LOW)
                  GPIO.output(out2,GPIO.LOW)
                  GPIO.output(out3,GPIO.HIGH)
                  GPIO.output(out4,GPIO.HIGH)
                  sleep(0.01)
                  #time.sleep(1)
              elif i==6:    
                  GPIO.output(out1,GPIO.LOW)
                  GPIO.output(out2,GPIO.LOW)
                  GPIO.output(out3,GPIO.LOW)
                  GPIO.output(out4,GPIO.HIGH)
                  sleep(0.01)
                  #time.sleep(1)
              elif i==7:    
                  GPIO.output(out1,GPIO.HIGH)
                  GPIO.output(out2,GPIO.LOW)
                  GPIO.output(out3,GPIO.LOW)
                  GPIO.output(out4,GPIO.HIGH)
                  sleep(0.01)
                  #time.sleep(1)
              if i==7:
                  i=0
                  continue
              i=i+1
              
        sleep(2)
        while True :
            GPIO.output(out1,GPIO.LOW)
            GPIO.output(out2,GPIO.LOW)
            GPIO.output(out3,GPIO.LOW)
            GPIO.output(out4,GPIO.LOW)
          
            cdstopr = analog_read(0)
            cdstopl = analog_read(1)
            cdsbotr = analog_read(2)
            cdsbotl = analog_read(3)
            cdsvtopr = cdstopr*3.3/1024
            cdsvtopl = cdstopl*3.3/1024
            cdsvbotr = cdsbotr*3.3/1024
            cdsvbotl = cdsbotl*3.3/1024
        
            avgtop = (cdstopr + cdstopl)/2
            avgbot = (cdsbotr + cdsbotl)/2
            avgright = (cdstopr + cdsbotr)/2
            avgleft = (cdstopl + cdsbotl)/2
        
            wind_data = analog_read(4)
            wind_speed = float(wind_data*3.3/1023)*25

            h, t = Adafruit_DHT.read_retry(sensor, pin)

            print("topright=%d\ttopleft=%d\tbotright=%d\tbotleft=%d\t"%(cdstopr,cdstopl,cdsbotr,cdsbotl))

            print("Wind:%.3f m/s,  Temp:%d"%(wind_speed,t))
                
            
            
        
            if wind_speed > 0.2 or t < 15:
                for y in range(800,0,-1):
                    if positive==1:
                        if i==0:
                            i=7
                        else:
                          i=i-1
                        y=y+3
                        positive=0
                    negative=1
                      #print((x+1)-y) 
                    if i==0:
                        GPIO.output(out1,GPIO.HIGH)
                        GPIO.output(out2,GPIO.LOW)
                        GPIO.output(out3,GPIO.LOW)
                        GPIO.output(out4,GPIO.LOW)
                        sleep(0.01)
                        #time.sleep(1)
                    elif i==1:
                        GPIO.output(out1,GPIO.HIGH)
                        GPIO.output(out2,GPIO.HIGH)
                        GPIO.output(out3,GPIO.LOW)
                        GPIO.output(out4,GPIO.LOW)
                        sleep(0.01)
                        #time.sleep(1)
                    elif i==2:  
                        GPIO.output(out1,GPIO.LOW)
                        GPIO.output(out2,GPIO.HIGH)
                        GPIO.output(out3,GPIO.LOW)
                        GPIO.output(out4,GPIO.LOW)
                        sleep(0.01)
                      #time.sleep(1)
                    elif i==3:    
                        GPIO.output(out1,GPIO.LOW)
                        GPIO.output(out2,GPIO.HIGH)
                        GPIO.output(out3,GPIO.HIGH)
                        GPIO.output(out4,GPIO.LOW)
                        sleep(0.01)
                          #time.sleep(1)
                    elif i==4:  
                        GPIO.output(out1,GPIO.LOW)
                        GPIO.output(out2,GPIO.LOW)
                        GPIO.output(out3,GPIO.HIGH)
                        GPIO.output(out4,GPIO.LOW)
                        sleep(0.01)
                          #time.sleep(1)
                    elif i==5:
                        GPIO.output(out1,GPIO.LOW)
                        GPIO.output(out2,GPIO.LOW)
                        GPIO.output(out3,GPIO.HIGH)
                        GPIO.output(out4,GPIO.HIGH)
                        sleep(0.01)
                          #time.sleep(1)
                    elif i==6:    
                        GPIO.output(out1,GPIO.LOW)
                        GPIO.output(out2,GPIO.LOW)
                        GPIO.output(out3,GPIO.LOW)
                        GPIO.output(out4,GPIO.HIGH)
                        sleep(0.01)
                          #time.sleep(1)
                    elif i==7:    
                        GPIO.output(out1,GPIO.HIGH)
                        GPIO.output(out2,GPIO.LOW)
                        GPIO.output(out3,GPIO.LOW)
                        GPIO.output(out4,GPIO.HIGH)
                        sleep(0.01)
                          #time.sleep(1)
                    if i==0:
                        i=7
                        continue
                    i=i-1
                sleep(2)
                break
           
        
                                    
                                    
                                    
                                
                
                
                
            if  avgtop < avgbot:
                angletb = angletb + 10
                angletb1 = angletb1 -10
                if angletb > 180 :
                    angletb = 180
                if angletb1 < 0 :
                    angletb = 180 
                set_angle(15,angletb)
                set_angle(0,angletb1)
                sleep(0.8)
        
            elif avgtop > avgbot:
                angletb = angletb - 10
                if angletb < 0 :
                    angletb = 0 
                set_angle(15,angletb)
                set_angle(0,angletb)
                sleep(0.8)
        
            else :
                set_angle(15,angletb)
                set_angle(0,angletb)
                sleep(0.8)
           
 ##               
           
#         if avgright < avgleft:
#             anglelr = anglelr + 10
#             if anglelr > 180 :
#                 anglelr = 180 
#             set_angle(15,anglelr)
#             sleep(0.8)
#                 
#                 
# 
#         elif avgright > avgleft:
#             anglelr = anglelr - 10
#             if angletb < 0 :
#                 angletb = 0 
#             set_angle(15,anglelr)
#             sleep(0.8)
#             
#         else :
#             set_angle(15,anglelr)
#             sleep(0.8)
                    
                    
                    
                    
                    
                    
                    
        
#         if avgtop < avgbot :
#             angletb = angletb + 10
#             if angletb > 180 :
#                 angletb = 180 
#             set_angle(0,angletb)
#             sleep(0.8)
#     
#         elif avgtop > avgbot:
#             angletb = angletb - 10
#             if angletb < 0 :
#                 angletb = 0 
#             set_angle(0,angletb)
#             sleep(0.8)
#     
#         else :
#             set_angle(0,angletb)
#             sleep(0.8)
           
                
           
#         if avgright < avgleft:
#             anglelr = anglelr + 10
#             if anglelr > 180 :
#                 anglelr = 180 
#             set_angle(0,anglelr)
#             sleep(0.8)
#                 
#                 
# 
#         elif avgright > avgleft:
#             anglelr = anglelr - 10
#             if angletb < 0 :
#                 angletb = 0 
#             set_angle(0,anglelr)
#             sleep(0.8)
#             
#         else :
#             set_angle(0,anglelr)
#             sleep(0.8)
                    

                

