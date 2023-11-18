#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
# Copyright 2017 ROBOTIS CO., LTD.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
################################################################################

# Author: Ryu Woon Jung (Leon)

#
# *********     Sync Write Example      *********
#
#
# Available Dynamixel model on this example : All models using Protocol 1.0
# This example is tested with two Dynamixel MX-28, and an USB2DYNAMIXEL
# Be sure that Dynamixel MX properties are already set as %% ID : 1 / Baudnum : 34 (Baudrate : 57600)
#
from Motor_sync import *
from IK import *
import os
import array
import time
import keyboard

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

from dynamixel_sdk import *                    # Uses Dynamixel SDK library

# Control table address
ADDR_MX_TORQUE_ENABLE      = 24               # Control table address is different in Dynamixel model
ADDR_MX_GOAL_POSITION      = 30
ADDR_MX_PRESENT_POSITION   = 36
ADDR_MX_MOVING_SPEED       = 32

# Data Byte Length -> AX시리지는 2byte 2byte임
LEN_MX_GOAL_POSITION       = 2
LEN_MX_PRESENT_POSITION    = 2

# Protocol version
PROTOCOL_VERSION            = 1.0               # See which protocol version is used in the Dynamixel

# Default setting
DXL1_ID                     = 11    # Dynamixel#1 ID : 1
DXL2_ID                     = 12 # Dynamixel#1 ID : 2
DXL3_ID                     = 13

ID_1                        = [11,12,13] 
ID_2                        = [21,22,23]
ID_3                        = [31,32,33] 
ID_4                        = [41,42,43]
ID_5                        = [51,52,53] 
ID_6                        = [61,62,63]



BAUDRATE                    = 57600             # Dynamixel default baudrate : 57600
DEVICENAME                  = 'COM3'    # Check which port is being used on your controller
                                                # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque
#DXL_MINIMUM_POSITION_VALUE =  512     # Dynamixel will rotate between this value
#DXL_MAXIMUM_POSITION_VALUE  = 1000            # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
#DXL_MINIMUM_POSITION_VALUE2 = 512        # Dynamixel will rotate between this value
#DXL_MAXIMUM_POSITION_VALUE2 = 300           # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)

DXL_MOVING_STATUS_THRESHOLD = 5              # Dynamixel moving status threshold

index = 0
#dxl_goal_position = [DXL_MINIMUM_POSITION_VALUE, DXL_MAXIMUM_POSITION_VALUE]         # Goal position
#dxl_goal_position2 = [DXL_MINIMUM_POSITION_VALUE2, DXL_MAXIMUM_POSITION_VALUE2]     

# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
# Set the protocol version
# Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Initialize GroupSyncWrite instance
groupSyncWrite = GroupSyncWrite(portHandler, packetHandler, ADDR_MX_GOAL_POSITION, LEN_MX_GOAL_POSITION)

# 필요한 함수 미리 정의
#============================================================================
def Torque_on_dynamixels(ID_list):
    for ID in ID_list:
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, ID, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        else:
            print("Dynamixel#{} has been successfully connected".format(ID))

def Torque_off_dynamixels(ID_list):
    for ID in ID_list:
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, ID, ADDR_MX_TORQUE_ENABLE, 0)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        else:
            print("Dynamixel#{} has been successfully connected".format(ID))

def Set_speed_dynamixels(ID_list):
    for ID in ID_list:
        dxl_comm_result, dxl_error =packetHandler.write2ByteTxRx(portHandler, ID , ADDR_MX_MOVING_SPEED, 400)
        print("{}번 모터 속도 초기화 완료!"  .format(ID))
quit
def gogo():
    groupSyncWrite.txPacket()
    groupSyncWrite.clearParam()
#=============================================================================
# 초기 세팅

# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    getch()
    quit()


# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()

# Enable Dynamixe l ~ 6 # Torque On
Torque_on_dynamixels(ID_1)
Torque_on_dynamixels(ID_2)
Torque_on_dynamixels(ID_3)
Torque_on_dynamixels(ID_4)
Torque_on_dynamixels(ID_5)
Torque_on_dynamixels(ID_6)

Set_speed_dynamixels(ID_1)
Set_speed_dynamixels(ID_2)
Set_speed_dynamixels(ID_3)
Set_speed_dynamixels(ID_4)
Set_speed_dynamixels(ID_5)
Set_speed_dynamixels(ID_6)




#=============================================================================
# 미리 gait 프로세싱 해놓기
import numpy as np
import matplotlib.pyplot as plt

#xl 은 왼쪽으로 다리를 끌고
#xr 은 오른쪽으로 다리를 끈다

steplength = 30
step_size = 6

xl = np.linspace(steplength * np.pi / 2, steplength * -np.pi / 2,step_size)
yl = np.full_like(xl, -80)  # y를 길이 5의 배열로 생성하여 -80으로 채웁니다.



xl2 = np.linspace(steplength * -np.pi / 2, steplength * np.pi / 2, step_size)
yl2 = (80 - 0) * np.cos(xl2 / steplength) - 80

#plt.plot(x2, y2, "o")

#plt.show() 
xr = np.linspace(-steplength * np.pi / 2, steplength * np.pi / 2,step_size)
yr = np.full_like(xr, -80)  # y를 길이 5의 배열로 생성하여 -80으로 채웁니다.



xr2 = np.linspace(steplength * np.pi / 2, steplength * -np.pi / 2, step_size)
yr2 = (80 - 0) * np.cos(xr2 / steplength) - 80

#=============================================================================

leg1 = LEG(ID_1,groupSyncWrite,packetHandler)
leg2 = LEG(ID_2,groupSyncWrite,packetHandler)
leg3 = LEG(ID_3,groupSyncWrite,packetHandler)
leg4 = LEG(ID_4,groupSyncWrite,packetHandler)
leg5 = LEG(ID_5,groupSyncWrite,packetHandler)
leg6 = LEG(ID_6,groupSyncWrite,packetHandler)

# 모터 initial 자세 이후 base자세
angle1 , angle2, angle3 = inverse_kinematics(0,0,201.878)
leg1.sync_param_add(angle1, angle2, angle3)
leg2.sync_param_add(angle1, angle2, angle3)
leg3.sync_param_add(angle1, angle2, angle3)
leg4.sync_param_add(angle1, angle2, angle3)
leg5.sync_param_add(angle1, angle2, angle3)
leg6.sync_param_add(angle1, angle2, angle3)
gogo()
time.sleep(3)

angle1 , angle2, angle3 = inverse_kinematics(100,0,-80)
angle = [angle1, angle2, angle3]
print(angle)
leg1.sync_param_add(angle1, angle2, angle3)
leg2.sync_param_add(angle1, angle2, angle3)
leg3.sync_param_add(angle1, angle2, angle3)
leg4.sync_param_add(angle1, angle2, angle3)
leg5.sync_param_add(angle1, angle2, angle3)
leg6.sync_param_add(angle1, angle2, angle3)
gogo()
    


def perform_action(action):
    if action == 'up': #전진
        print("행동 1을 수행합니다.")
        for i in range(1,step_size):
            angle1 , angle2, angle3 = inverse_kinematics(100,xl[i],yl[i])
            angler1 , angler2, angler3 = inverse_kinematics(100,xr[i],yr[i])

            leg2.sync_param_add(angler1+30, angler2, angler3)
            leg4.sync_param_add(angler1-30, angler2, angler3)
            leg6.sync_param_add(angle1, angle2, angle3)
            
            angle4, angle5, angle6 = inverse_kinematics(100,xl2[i],yl2[i])
            angler4, angler5, angler6 = inverse_kinematics(100,xr2[i],yr2[i])

            leg1.sync_param_add(angle4-30, angle5, angle6)
            leg3.sync_param_add(angler4, angler5, angler6)
            leg5.sync_param_add(angle4+30, angle5, angle6)
            
            gogo()
            time.sleep(0.02)
        
        for i in range(1,step_size):
            angle1 , angle2, angle3 = inverse_kinematics(100,xl2[i],yl2[i])
            angler1 , angler2, angler3 = inverse_kinematics(100,xr2[i],yr2[i])
              
            leg2.sync_param_add(angler1+30, angler2, angler3)
            leg4.sync_param_add(angler1-30, angler2, angler3)
            leg6.sync_param_add(angle1, angle2, angle3)
            
            angle4, angle5, angle6 = inverse_kinematics(100,xl[i],yl[i])
            angler4, angler5, angler6 = inverse_kinematics(100,xr[i],yr[i])

            leg1.sync_param_add(angle4-30, angle5, angle6)
            leg3.sync_param_add(angler4, angler5, angler6)
            leg5.sync_param_add(angle4+30, angle5, angle6)
            
            gogo()
            time.sleep(0.02)



    elif action == 'down': #후진
        print("행동 2를 수행합니다.")
        for i in range(1,step_size):
                angle1 , angle2, angle3 = inverse_kinematics(100,xr[i],yr[i])
                angler1 , angler2, angler3 = inverse_kinematics(100,xl[i],yl[i])

                leg2.sync_param_add(angler1+30, angler2, angler3)
                leg4.sync_param_add(angler1-30, angler2, angler3)
                leg6.sync_param_add(angle1, angle2, angle3)
                
                angle4, angle5, angle6 = inverse_kinematics(100,xr2[i],yr2[i])
                angler4, angler5, angler6 = inverse_kinematics(100,xl2[i],yl2[i])

                leg1.sync_param_add(angle4-30, angle5, angle6)
                leg3.sync_param_add(angler4, angler5, angler6)
                leg5.sync_param_add(angle4+30, angle5, angle6)
                
                gogo()
                time.sleep(0.02)
        
        for i in range(1,step_size):
            angle1 , angle2, angle3 = inverse_kinematics(100,xr2[i],yr2[i])
            angler1 , angler2, angler3 = inverse_kinematics(100,xl2[i],yl2[i])
              
            leg2.sync_param_add(angler1+30, angler2, angler3)
            leg4.sync_param_add(angler1-30, angler2, angler3)
            leg6.sync_param_add(angle1, angle2, angle3)
            
            angle4, angle5, angle6 = inverse_kinematics(100,xr[i],yr[i])
            angler4, angler5, angler6 = inverse_kinematics(100,xl[i],yl[i])

            leg1.sync_param_add(angle4-30, angle5, angle6)
            leg3.sync_param_add(angler4, angler5, angler6)
            leg5.sync_param_add(angle4+30, angle5, angle6)
            
            gogo()
            time.sleep(0.02)



    elif action == 'left':#좌회전
        print("행동 3을 수행합니다.")
        # 행동 3에 대한 로봇 동작 수행 코드 추가
        for i in range(1,step_size):
            angle1 , angle2, angle3 = inverse_kinematics(100,xl[i],yl[i])

            leg2.sync_param_add(angle1, angle2, angle3)
            leg4.sync_param_add(angle1, angle2, angle3)
            leg6.sync_param_add(angle1, angle2, angle3)
            
            angle4, angle5, angle6 = inverse_kinematics(100,xl2[i],yl2[i])

            leg1.sync_param_add(angle4, angle5, angle6)
            leg3.sync_param_add(angle4, angle5, angle6)
            leg5.sync_param_add(angle4, angle5, angle6)
            
            gogo()
            time.sleep(0.02)
        
        for i in range(1,step_size):
            angle1 , angle2, angle3 = inverse_kinematics(100,xl2[i],yl2[i])

            leg2.sync_param_add(angle1, angle2, angle3)
            leg4.sync_param_add(angle1, angle2, angle3)
            leg6.sync_param_add(angle1, angle2, angle3)
            
            angle4, angle5, angle6 = inverse_kinematics(100,xl[i],yl[i])

            leg1.sync_param_add(angle4, angle5, angle6)
            leg3.sync_param_add(angle4, angle5, angle6)
            leg5.sync_param_add(angle4, angle5, angle6)
            
            gogo()
            time.sleep(0.02)
        # 행동 2에 대한 로봇 동작 수행 코드 추가






    elif action == 'right':#우회전
        print("행동 4을 수행합니다.")
        # 행동 4에 대한 로봇 동작 수행 코드 추가
        for i in range(1,step_size):
            angle1 , angle2, angle3 = inverse_kinematics(100,xr[i],yr[i])

            leg2.sync_param_add(angle1, angle2, angle3)
            leg4.sync_param_add(angle1, angle2, angle3)
            leg6.sync_param_add(angle1, angle2, angle3)
            
            angle4, angle5, angle6 = inverse_kinematics(100,xr2[i],yr2[i])

            leg1.sync_param_add(angle4, angle5, angle6)
            leg3.sync_param_add(angle4, angle5, angle6)
            leg5.sync_param_add(angle4, angle5, angle6)
            
            gogo()
            time.sleep(0.02)
        
        for i in range(1,step_size):
            angle1 , angle2, angle3 = inverse_kinematics(100,xr2[i],yr2[i])

            leg2.sync_param_add(angle1, angle2, angle3)
            leg4.sync_param_add(angle1, angle2, angle3)
            leg6.sync_param_add(angle1, angle2, angle3)
            
            angle4, angle5, angle6 = inverse_kinematics(100,xr[i],yr[i])

            leg1.sync_param_add(angle4, angle5, angle6)
            leg3.sync_param_add(angle4, angle5, angle6)
            leg5.sync_param_add(angle4, angle5, angle6)
            
            gogo()
            time.sleep(0.02)
        # 행동 2에 대한 로봇 동작 수행 코드 추가


    elif action == 'default':
        print("올바른 행동을 선택해주세요.")
        # angle1 , angle2, angle3 = inverse_kinematics(100,0,-80)
        # leg1.sync_param_add(angle1, angle2, angle3)
        # leg2.sync_param_add(angle1, angle2, angle3)
        # leg3.sync_param_add(angle1, angle2, angle3)
        # leg4.sync_param_add(angle1, angle2, angle3)
        # leg5.sync_param_add(angle1, angle2, angle3)
        # leg6.sync_param_add(angle1, angle2, angle3)
        # gogo()

        angle1 , angle2, angle3 = inverse_kinematics(100,0,-80)
      

        leg2.sync_param_add(angle1, angle2, angle3)
        leg4.sync_param_add(angle1, angle2, angle3)
        leg6.sync_param_add(angle1, angle2, angle3)
        
        angle4, angle5, angle6 = inverse_kinematics(120,0,-10)
       

        leg1.sync_param_add(angle4, angle5, angle6)
        leg3.sync_param_add(angle4, angle5, angle6)
        leg5.sync_param_add(angle4, angle5, angle6)

        gogo()
        time.sleep(0.3)

        angle1 , angle2, angle3 = inverse_kinematics(100,0,-80)
        leg1.sync_param_add(angle1, angle2, angle3)
        leg2.sync_param_add(angle1, angle2, angle3)
        leg3.sync_param_add(angle1, angle2, angle3)
        leg4.sync_param_add(angle1, angle2, angle3)
        leg5.sync_param_add(angle1, angle2, angle3)
        leg6.sync_param_add(angle1, angle2, angle3)
        gogo()
        time.sleep(0.2)
        
        angle1 , angle2, angle3 = inverse_kinematics(120,0,-10)
      

        leg2.sync_param_add(angle1, angle2, angle3)
        leg4.sync_param_add(angle1, angle2, angle3)
        leg6.sync_param_add(angle1, angle2, angle3)
        
        angle4, angle5, angle6 = inverse_kinematics(100,0,-80)
       

        leg1.sync_param_add(angle4, angle5, angle6)
        leg3.sync_param_add(angle4, angle5, angle6)
        leg5.sync_param_add(angle4, angle5, angle6)

        gogo()
        time.sleep(0.3)

        angle1 , angle2, angle3 = inverse_kinematics(100,0,-80)
        leg1.sync_param_add(angle1, angle2, angle3)
        leg2.sync_param_add(angle1, angle2, angle3)
        leg3.sync_param_add(angle1, angle2, angle3)
        leg4.sync_param_add(angle1, angle2, angle3)
        leg5.sync_param_add(angle1, angle2, angle3)
        leg6.sync_param_add(angle1, angle2, angle3)
        gogo()
        time.sleep(0.2)


while True:
    if keyboard.is_pressed('q'):
        print("프로그램을 종료합니다.")
        break
    elif keyboard.is_pressed('up'):
        perform_action('up')
    elif keyboard.is_pressed('down'):
        perform_action('down')
    elif keyboard.is_pressed('left'):
        perform_action('left')
    elif keyboard.is_pressed('right'):
        perform_action('right')
    else:
        perform_action('default')
        

Torque_off_dynamixels(ID_1)
Torque_off_dynamixels(ID_2)
Torque_off_dynamixels(ID_3)
Torque_off_dynamixels(ID_4)
Torque_off_dynamixels(ID_5)
Torque_off_dynamixels(ID_6)

# Close port
portHandler.closePort()
