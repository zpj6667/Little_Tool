#-*- coding: utf-8 -*
import sys
import serial
import serial.tools.list_ports
import easygui as g
from time import sleep

plist = list(serial.tools.list_ports.comports()) #列表化所有串口信息
port_num = len(plist)   #串口数量
global num
num = 0

if port_num <= 0:
    print ("The Serial port can't find!")
else:
    while (port_num-num) > 0 :
        plist_usb =list(plist[num])     #把第一个串口的信息序列化
        plist_usb_name = plist_usb[1]   #获得串口属性
        name = plist_usb_name[0:3]      #取得名称
        if name =='USB':
            com_num = plist_usb[0]      #取得USB设备端口号
            break
        num = num+1

def recv(serial):
    while True:
        data = serial.read(270)
        if data == '':
            continue
        else:
            break
        sleep(0.01)
    return data

if __name__ == '__main__':

    try:
        title="选择电池类型"       # 在左上角的 标题旷里面
        msg="请选择电池类型及波特率："
        choices=['派能（115200）','一合/凯歌（9600）']  # 在选择框内 , 提供可选择项
        choice=g.choicebox(msg,title,choices) #  在这里 choice 可以得到上面你选择的那个选项
        g.msgbox("你的选择是:"+str(choice),'结果') # 打印出来
        if choice == '派能（115200）' :
            baud_rate = 115200
        else :
            baud_rate = 57600
        serial = serial.Serial(com_num,115200, bytesize=8, parity='N', stopbits=1, timeout=0.5)
        # print ("check which port was really used >",serial.name)  #输出端口号
        if serial.isOpen() :
            g.msgbox(com_num + " open success", title='电池协议校验器', ok_button='查看模拟量数据')
            print(com_num + " open success")
        else :
            g.msgbox(com_num + " open fail", title='电池协议校验器', ok_button='退出')
            print(com_num + " open fail")

        while True:
            #输入并发送报文
            # str1 = input("send:")
            # a=str1+"\n"
            #print(len(a))
            #serial.write((a).encode("gbk"))
            #sleep(0.1)

            senddata = '7e3230303134363432453030323031464433350d' 
            senddata = bytes.fromhex(senddata)    #把byte转换HEX的byte
            serial.write(senddata)
            sleep(0.3)
            # x = bytearray.fromhex(senddata)     #把HEX转换str

            data =recv(serial)
            if data == b'' :
                g.msgbox("无数据接收，请检查：\n\n\n\
                          1、通讯线路是否正确连接电池.\n\n\
                          2、电池开关是否开启.", title='通讯异常！', ok_button='退出')
                sys.exit()
            if data != b'' :
                #print('当前温度：', data[61:65])#输出当前温度的byte形式值
                # print(int.from_bytes(data[61:65], byteorder='big', signed=True))  #不固定长度的bytes类型数据转int类型数据
                # print(data)

                x = data[-39:-35].decode("gbk") #把byte转换str
                # y = bytearray.fromhex(x)      #把str转换HEX
                if  '~' in x:
                    continue
                z = int(x, 16)
                if choice == '派能（115200）' :
                    temperature1 = (z-2731)/10
                else:
                    temperature1 = z - 40
                # print('1串温度：',temperature3,'℃')

                x = data[-35:-31].decode("gbk") #把byte转换str
                # y = bytearray.fromhex(x)      #把str转换HEX
                if  '~' in x:
                    continue
                z = int(x, 16)                 
                if choice == '派能（115200）' :
                    temperature2 = (z-2731)/10
                else:
                    temperature2 = z - 40
                # print('2串温度：',temperature4,'℃')

                x = data[-31:-27].decode("gbk") #把byte转换str
                # y = bytearray.fromhex(x)      #把str转换HEX
                if  '~' in x:
                    continue
                z = int(x, 16)
                if choice == '派能（115200）' :
                    temperature3 = (z-2731)/10
                else:
                    temperature3 = z - 40
                # print('3串温度：',temperature5,'℃')

                if temperature1 > 100 :
                    temperature1 = 0
                if temperature2 > 100 :         #如果不是温度数据就默认为0度
                    temperature2 = 0
                if temperature3 > 100 :
                    temperature3 = 0

                temperature_max = max(temperature1,temperature2,temperature3)
                # print('当前温度：',temperature,'℃')
                x = data[-27:-23].decode("gbk") #把byte转换str
                if  '~' in x:
                    continue
                z = int(x, 16) 
                if data[-27:-26]==b'F':         #判断是否为负数
                    z = z - 65536
                if choice == '派能（115200）' :
                    current = z/10 
                else:
                    current = z/100
                # print('当前电流：',current,'A')

                x = data[-23:-19].decode("gbk") #把byte转换str
                # y = bytearray.fromhex(x)      #把str转换HEX
                if  '~' in x:
                    continue
                z = int(x, 16)                  #把str转换int
                if choice == '派能（115200）' :
                    voltage = z/1000
                else:
                    voltage = z/100
                # print('当前电压：',voltage,'V')

                x = data[-19:-15].decode("gbk") #把byte转换str
                # y = bytearray.fromhex(x)      #把str转换HEX
                if  '~' in x:
                    continue
                z = int(x, 16)                  #把str转换int
                if choice == '派能（115200）' :
                    z_remaining = z/1000
                else:
                    z_remaining = z/100
                # print('剩余电量：',z_remaining,'Ah (容量在65Ah以上乘以1000)')

                x = data[-13:-9].decode("gbk")  #把byte转换str
                # y = bytearray.fromhex(x)      #把str转换HEX
                if  '~' in x:
                    continue
                z = int(x, 16)                  #把str转换int
                if choice == '派能（115200）' :
                    z_all = z/1000
                else:
                    z_all = z/100
                # print('总的电量：',z_all,'Ah (容量在65Ah以上乘以1000)')
                
                z_percent = z_remaining/z_all*100
                # print('剩余电量百分比：',z_percent,'%')
                # print(isinstance(z,int))   #判断数据类型

                temperature_max = str(temperature_max)
                temperature1 = str(temperature1)
                temperature2 = str(temperature2)
                temperature3 = str(temperature3)
                current = str(current)               #msgbox方法需要输入字符串
                voltage = str(voltage)
                z_all = str(z_all)
                z_percent = str(z_percent)
                z_remaining = str(z_remaining)

                #ccbox(msg='', title=' ', choices=('Continue', 'Cancel'), image=None)
                if g.ccbox('1串温度：' + temperature1 + '℃ \n'      \
                           '2串温度：' + temperature2 + '℃ \n'      \
                           '3串温度：' + temperature3 + '℃ \n'      \
                           '最高温度：' + temperature_max + '℃ \n'  \
                           '当前电流：' + current     + 'A  \n'      \
                           '当前电压：' + voltage     + 'V  \n'      \
                           '剩余电量：' + z_remaining + 'Ah (容量在65Ah以上乘以1000) \n'  \
                           '总的电量：' + z_all       + 'Ah (容量在65Ah以上乘以1000) \n'  \
                           '剩余电量百分比：' + z_percent + '% '  \
                           ,title='电池各项模拟量值',choices=('刷新','退出'))      :
                    pass
                else:
                    print("::::::::::::::::::::")
                    exit(0)
    except Exception as e:
        e = str(e)
        if 'name' in e :
            print(e)
            g.msgbox("请检查PC是否插入USB转串口设备.", title='通讯异常！', ok_button='退出')
            sys.exit()

    # else:
    #     print ('1111111111111111111111111111111')
            # print('当前电流：', data[65:69])
            # print('当前电压：', data[69:73])
            # print('剩余电量：', data[73:77])
            # print('总的电量：', data[79:83])