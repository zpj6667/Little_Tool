#-*- coding: utf-8
from decimal import Decimal
def bTod(n, pre=4):
    '''
    把一个带小数的二进制数n转换成十进制
    小数点后面保留pre位小数
    '''
    string_number1 = str(n) #number1 表示二进制数，number2表示十进制数
    decimal = 0  #小数部分化成二进制后的值
    flag = False   
    for i in string_number1: #判断是否含小数部分
        if i == '.':
            flag = True
            break
    if flag: #若二进制数含有小数部分
        string_integer, string_decimal = string_number1.split('.') #分离整数部分和小数部分
        for i in range(len(string_decimal)):
            decimal += 2**(-i-1)*int(string_decimal[i])  #小数部分化成二进制
        number2 = int(str(int(string_integer, 2))) + decimal
        return round(number2, pre)
    else: #若二进制数只有整数部分
        return int(string_number1, 2)#若只有整数部分 直接一行代码二进制转十进制 python还是骚 

def dTob(n, pre=4):
    '''
    把一个带小数的十进制数n转换成二进制
    小数点后面保留pre位小数
    '''
    string_number1 = str(n) #number1 表示十进制数，number2表示二进制数
    flag = False   
    for i in string_number1: #判断是否含小数部分
        if i == '.':
            flag = True
            break
    if flag:
        string_integer, string_decimal = string_number1.split('.') #分离整数部分和小数部分
        integer = int(string_integer)
        decimal = Decimal(str(n)) - integer
        l1 = [0,1]
        l2 = []
        decimal_convert = ""
        while True:  
            if integer == 0: break
            x,y = divmod(integer, 2)  #x为商，y为余数 
            l2.append(y)
            integer = x
        string_integer = ''.join([str(j) for j in l2[::-1]])  #整数部分转换成二进制 
        i = 0  
        while decimal != 0 and i < pre:  
            result = int(decimal * 2)  
            decimal = decimal * 2 - result  
            decimal_convert = decimal_convert + str(result)  
            i = i + 1  
        string_number2 = string_integer + '.' + decimal_convert
        return float(string_number2)
    else: #若十进制只有整数部分
        l1 = [0,1]
        l2 = []
        while True:  
            if n == 0: break
            x,y = divmod(n, 2)  #x为商，y为余数 
            l2.append(y)
            n = x
        string_number = ''.join([str(j) for j in l2[::-1]])
        return int(string_number)


def float_hex(n):
    u = abs(n)
    if u< 0.01 :
        n=0
    # print(n)
    if n == 0 :
        hexstr = 0
    elif n != 0:
        n = float(n)    #把n转换为浮点数
        # print('?????',n)
        minus = False #判断是否为负数标志位
        if n < 0  :
            n = abs(n)
            minus = True

        float_bin = ("%.10f" % dTob(n,23))     #浮点数转二进制，之所以精确到小数点后10位是为了避免科学计数法的出现导致程序崩溃
        # print(float_bin)
        # float_bin = str(float_bin)
        float_bin = str(float_bin).replace("2","1") #避免程序崩溃
        # print(float_bin)
        # print(isinstance(float_bin,str))
        float_bin_list=[x for x in str(float_bin)]     #for循环赋值
        # print(float_bin_list)
        # print(len(float_bin_list))

        ################阶码换算###############
        if n >= 1 :
            e = float_bin_list.index('.') - 1 + 127    #得到阶码值e
            e_bin = bin(e).replace('0b','')      #转换二进制阶码e_bin并去掉'0b'
        elif n < 1 :
            e = 127 - (float_bin_list.index('1') - float_bin_list.index('.'))
            e_bin = bin(e).replace('0b','')      #转换二进制阶码e_bin并去掉'0b'
            # print(e)

        ###########得到基数码float_bin_list
        if n >= 1 :
            float_bin_list.remove('.')          #去掉小数点
            del float_bin_list[0]               #去掉第一位
        elif n < 1 :
            del float_bin_list[0:129-e]         #去掉头部
        # print('^^^^^^^^^^^^^',float_bin_list)

        ###############基数码不足23位的部分补0
        date_length = len(float_bin_list)
        # print(date_length)
        while date_length < 23 :
            float_bin_list[date_length:23] = '0'
            date_length = date_length+1

        # print(float_bin_list)
        # print(e_bin)

        str1 = e_bin + ''.join(float_bin_list) #合并阶码和基数码
        # print (str1)
        ###################如果转换值为负数则给符号位S补1
        if minus == True :
            if len(str1) == 29 :
                str1 = '100' + str1
            elif len(str1) == 30 :
                str1 = '10' + str1
            elif len(str1) == 31 :
                str1 = '1' + str1
        # print(str1)
        hexstr = int(str1,2)
        
    return hex(hexstr)  




