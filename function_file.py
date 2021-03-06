

def print_string_hex(data):
    lin = ['%02X' % ord(i) for i in data]
    print(" ".join(lin))

# 数据发送函数
def data_send_function(str1, str2, str3):
    global input_speed_form
    global hex_command1

    if str1 >= 0 and str2 >= 0:
        input_speed_1 = hex(str1)[2:].zfill(4)
        input_speed_2 = hex(str2)[2:].zfill(4)
        # 校验位
        lit = [0x07, 0x08, eval('0x'+str3), 0x00, eval('0x'+input_speed_1[0:2]), eval('0x'+str(input_speed_1)[
                                                                             2:]), eval('0x'+input_speed_2[0:2]), eval('0x'+str(input_speed_2)[
                                                                             2:]), 0x00, 0x00]
        t = None
        for i in range(len(lit)):
            if i:
                t ^= lit[i]
            else:
                t = lit[i] ^ 0

        input_speed_form = '55 AA 07 08 ' + str3 + ' 00 ' + input_speed_1[0:2] + ' ' + str(input_speed_1)[
                                                                             2:] + ' ' + input_speed_2[
                                                                                         0:2] + ' ' + str(
            input_speed_2)[2:] + ' 00 00 ' + hex(t)[2:].zfill(2) + ' F0'
        hex_command1 = bytes.fromhex(input_speed_form)

    elif str1 < 0 and str2 < 0:
        input_speed_abs1 = hex(32768 - abs(str1) + 32768)
        input_speed_abs2 = hex(32768 - abs(str2) + 32768)
        # 校验位
        lit = [0x07, 0x08, eval('0x' + str3), 0x00, eval('0x' + input_speed_abs1[-4:-2]), eval('0x' + str(input_speed_abs1)[
                                                                                      -2:]), eval('0x' + input_speed_abs2[-4:-2]),
               eval('0x' + str(input_speed_abs2)[
                      -2:]), 0x00, 0x00]
        t = None
        for i in range(len(lit)):
            if i:
                t ^= lit[i]
            else:
                t = lit[i] ^ 0
        input_speed_form = '55 AA 07 08 ' + str3 + ' 00 ' + input_speed_abs1[-4:-2] + ' ' + str(input_speed_abs1)[
                                                                                  -2:] + ' ' + input_speed_abs2[
                                                                                               -4:-2] + ' ' + str(
            input_speed_abs2)[-2:] + ' 00 00 ' + hex(t)[2:].zfill(2) + ' F0'

        hex_command1 = bytes.fromhex(input_speed_form)

    elif str1 >= 0 and str2 < 0:
        input_speed_1 = hex(str1)[2:].zfill(4)
        input_speed_abs2 = hex(32768 - abs(str2) + 32768)
        # 校验位
        lit = [0x07, 0x08, eval('0x' + str3), 0x00, eval('0x' + input_speed_1[0:2]), eval('0x' + str(input_speed_1)[
                                                                                           2:]),
               eval('0x' + input_speed_abs2[-4:-2]),
               eval('0x' + str(input_speed_abs2)[
                      -2:]), 0x00, 0x00]
        t = None
        for i in range(len(lit)):
            if i:
                t ^= lit[i]
            else:
                t = lit[i] ^ 0
        input_speed_form = '55 AA 07 08 ' + str3 + ' 00 ' + input_speed_1[0:2] + ' ' + str(input_speed_1)[
                                                                             2:] + ' ' + input_speed_abs2[
                                                                                         -4:-2] + ' ' + str(
            input_speed_abs2)[-2:] + ' 00 00 ' + hex(t)[2:].zfill(2) + ' F0'
        hex_command1 = bytes.fromhex(input_speed_form)

    elif str1 < 0 and str2 >= 0:
        input_speed_abs1 = hex(32768 - abs(str1) + 32768)
        input_speed_2 = hex(str2)[2:].zfill(4)
        # 校验位
        lit = [0x07, 0x08, eval('0x' + str3), 0x00, eval('0x' + input_speed_abs1[-4:-2]), eval('0x' + str(input_speed_abs1)[
                                                                                      -2:]),
               eval('0x' + input_speed_2[0:2]),
               eval('0x' + str(input_speed_2)[
                      2:]), 0x00, 0x00]
        t = None
        for i in range(len(lit)):
            if i:
                t ^= lit[i]
            else:
                t = lit[i] ^ 0
        input_speed_form = '55 AA 07 08 ' + str3 + ' 00 ' + input_speed_abs1[-4:-2] + ' ' + str(input_speed_abs1)[
                                                                                  -2:] + ' ' + input_speed_2[
                                                                                               0:2] + ' ' + str(
            input_speed_2)[2:] + ' 00 00 ' + hex(t)[2:].zfill(2) + ' F0'
        hex_command1 = bytes.fromhex(input_speed_form)

    return hex_command1, input_speed_form




# 接收数据后判断正负，有符号十六进制数转为十进制数
def data_receive_process(str1, int1, int2):
    rec3_er = bin(int(str1, 16))[2:].zfill(int1)
    if rec3_er[0] == '1':
        rec3_er_new = -(2 ** (int1-1) - int(rec3_er[1:], 2))/int2
    else:
        rec3_er_new = int(rec3_er[1:], 2) / int2
    return rec3_er_new

