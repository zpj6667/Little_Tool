#-*- coding: utf-8 -*
import sys
import pygame
import socket
import float_hex
import logging
import tkinter
import socket
import modbus_tk
import easygui as g
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp

clock = pygame.time.Clock()# Initialize the joysticks
pygame.joystick.init()
logger = modbus_tk.utils.create_logger("console")
# skill_key = [] #手柄功能按键变量数组
done = False
mode = False #True 为导航模式，False为遥控模式
pygame.init()

root = tkinter.Tk()
root.title('手柄控制器')        #窗口标题
root.resizable(False, False)    #固定窗口大小
windowWidth = 850               #获得当前窗口宽
windowHeight = 600              #获得当前窗口高
screenWidth,screenHeight = root.maxsize()     #获得屏幕宽和高
geometryParam = '%dx%d+%d+%d'%(windowWidth, windowHeight, (screenWidth-windowWidth)/2, (screenHeight - windowHeight)/2)
root.geometry(geometryParam)    #设置窗口大小及偏移坐标
root.wm_attributes('-topmost',1)#窗口置顶

#label文本
label_text = tkinter.Label(root, text = '操作说明');
label_text.pack();

#label图片
img_gif = tkinter.PhotoImage(file = '手柄功能.gif')
label_img = tkinter.Label(root, image = img_gif)
label_img.pack()

root.mainloop()

if __name__ == "__main__":
    #建立一个socket对象并连接用于接收rbk返回的数据
    client = socket.socket()   
    # client.connect(('192.168.4.184', 502))
    # master = modbus_tcp.TcpMaster(host="192.168.4.184", port=502)
    client.connect(('192.168.192.5', 502))
    master = modbus_tcp.TcpMaster(host="192.168.192.5", port=502)
    master.set_timeout(0.1)
    # logger.info("connected")
    # logger.info(master.execute(1, cst.WRITE_SINGLE_REGISTER, 1, output_value=1))# 写寄存器地址为0的保持寄存器
    # logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 1))

    while done==False:
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done=True # Flag that we are done so we exit this loop
             
            # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
            # if event.type == pygame.JOYBUTTONDOWN:
            #     print("Joystick button pressed DOWN.")
            # if event.type == pygame.JOYBUTTONUP:
            #     print("Joystick button released UP.")
        joystick_count = pygame.joystick.get_count()


        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            ##########左摇杆变量######################
            axes = joystick.get_numaxes()
            for i in range( axes ):
                axis = joystick.get_axis( i )
                if   i == 4 :
                    Rocker_L_R = axis * -1  #手柄值的方向是反的乘以-1
                elif i == 1 :
                    Rocker_U_D = axis * -1
            # print(Rocker_U_D)

            ########按键变量########################
            skill_key = []  #清零重新统计功能按键值
            buttons = joystick.get_numbuttons()
            for i in range( buttons ):
                button = joystick.get_button( i )
                skill_key.append(button)
            # print(skill_key)
            key_y = skill_key[3]
            key_a = skill_key[0]
            key_back = skill_key[6]
            key_start = skill_key[7]

            ###############排除手柄的科学计数法最小数避免程序崩溃############
            Rocker_U_D = float("%.10f" % Rocker_U_D)     #避免科学计数法的出现导致float_hex程序崩溃
            Rocker_L_R = float("%.10f" % Rocker_L_R)     #避免科学计数法的出现导致float_hex程序崩溃
            Vx = float_hex.float_hex(Rocker_U_D)
            Vw = float_hex.float_hex(Rocker_L_R)
            # print('x :',Rocker_U_D,float_hex.float_hex(Rocker_U_D))
            # print('w :',Rocker_L_R,float_hex.float_hex(Rocker_L_R))

            w =  abs(Rocker_L_R)
            x =  abs(Rocker_U_D)
            ###############线速度值处理##############
            if x <0.01 :
                Rocker_U_D = 0
                Vx_H = 0x0000
                Vx_L = 0x0000
            else :
                Vx = list(Vx)
                # a = list('0x1234')
                Vx_H = ''.join(Vx[0:6])   #把逗号去掉，获得32位8字节的16进制浮点数的高4字
                # print(len(x_1))
                # print('Vx_H ：',Vx_H)
                Vx_H = int(Vx_H,16)        #转换成int型数据等待发送
                # print('x_1 ：',x_1)
                
                if len(Vx) <= 6 :
                    Vx_L = 0x0000        #如果Vx的值小于65536没有低4字则补0
                else:
                    Vx_L = ''.join(Vx[0:2]+Vx[6:])  #把逗号去掉，获得32位8字节的16进制浮点数的低4字
                    # print('Vx_L ：',Vx_L)
                    Vx_L = int(Vx_L,16)
            ###############角速度值处理##############
            if w <0.01 :
                Rocker_L_R = 0
                Vw_L = 0x0000
                Vw_H = 0x0000
            else :
                Vw = list(Vw)
                # a = list('0x1234')
                Vw_H = ''.join(Vw[0:6])   #把逗号去掉，获得32位8字节的16进制浮点数的高4字
                # print(len(x_1))
                # print('Vw_H ：',Vw_H)
                Vw_H = int(Vw_H,16)       #转换成int型数据等待发送
                # print('x_1 ：',x_1)
                
                if len(Vw) <= 6 :
                    Vw_L = 0x0000        #如果Vx的值小于65536没有低4字则补0
                else:
                    Vw_L = ''.join(Vw[0:2]+Vw[6:])  #把逗号去掉，获得32位8字节的16进制浮点数的低4字
                    # print('Vw_L ：',Vw_L)
                    # print('11111111111')
                    Vw_L = int(Vw_L,16)


            if mode == False :# True 为导航模式，False为遥控模式
                #####################通过ModbusTCP协议把Vw/Vx数据发送给RBK#################
                    # print('Turn')
                # print('x :',x)
                # print('w :',w)
                try:
                    logger.info(master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 9, output_value=[Vw_H,Vw_L]))
                    logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 2))
                except socket.timeout as err:
                    pass
                    # print('go')
                    # print('x :',x)
                    # print('w :',w)
                try:
                    logger.info(master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 5, output_value=[Vx_H,Vx_L]))
                    logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 2))
                except socket.timeout as err:
                    pass
                    # Rocker_R = axis[2]
                    # Rocker_U = axis[3]
                    # Rocker_D = axis[4]
                if  Rocker_L_R == 0 and Rocker_U_D == 0 :
                    mode = True

            elif 1 in skill_key or mode == True :    #确认位置正确
                if key_start == 1 :
                    try:
                        # 写寄存器地址为0的线圈寄存器，写入内容为0（位操作）
                        logger.info(master.execute(1, cst.WRITE_SINGLE_COIL, 2, output_value=1))
                        logger.info(master.execute(1, cst.READ_COILS, 0, 1))
                    except socket.timeout as err:
                        pass
                if key_back == 1 :
                    try:
                        logger.info(master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 0, output_value=[0x0001]))  #去1目标点
                        logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 1))
                    except socket.timeout as err:
                        pass
                if key_y == 1 :
                    
                    senddata = bytes.fromhex('00 07 00 00 00 06 01 04 00 21 00 01')# 读取当前机器人所在站点
                    client.sendall(senddata)
                    # logger.info(master.execute(1, cst.READ_INPUT_REGISTERS, 21, 1))#调用这个库rbk接收不到数据,不知道什么原因
                    data = client.recv(1024)
                    print('Y当前位置',data[10])
                    data = data[10]
                    if data != 0 : #AGV必须在某个点上
                        try:
                            logger.info(master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 0, output_value=[data + 1]))  #去下一目标点
                            logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 1))
                        except socket.timeout as err:
                            pass
                    # time.sleep(5)
                if key_a == 1 :
                    senddata = bytes.fromhex('00 07 00 00 00 06 01 04 00 21 00 01')
                    client.sendall(senddata)
                    # logger.info(master.execute(1, cst.READ_INPUT_REGISTERS, 21, 1))# 调用这个库rbk接收不到数据不知道什么原因
                    data = client.recv(1024)
                    print('A当前位置',data[10])   
                    data = data[10]       
                    if data > 0 :
                        try:
                            logger.info(master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 0, output_value=[data - 1])) #去上一目标点
                            logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 1))
                        except socket.timeout as err:
                            pass
                    # time.sleep(5)
                if  Rocker_L_R != 0 or Rocker_U_D != 0 :
                    mode = False

        # Limit to 20 frames per second
        clock.tick(20)

pygame.quit ()