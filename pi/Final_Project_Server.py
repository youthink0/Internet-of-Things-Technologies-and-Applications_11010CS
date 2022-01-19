from bluedot.btcomm import BluetoothServer
import time
import pandas as pd
import xlsxwriter
from openpyxl import load_workbook

import sys 
try:
    reload         # Python 2
    reload(sys)
    sys.setdefaultencoding('utf8')
except NameError:  # Python 3
    from importlib import reload

import tempfile
from gtts import gTTS
from pygame import mixer
import time

def speak(sentence, lang, loops=1):
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        tts = gTTS(text=sentence, lang=lang)
        tts.save('{}.mp3'.format(fp.name))
        mixer.init()
        mixer.music.load('{}.mp3'.format(fp.name))
        mixer.music.play(loops)

def norms(input):
    psum_n = 0
    x = 0
    secs_now = int(input.split(' ')[4].split(':')[0])*3600+int(input.split(' ')[4].split(':')[1])*60+int(input.split(' ')[4].split(':')[2])
    #print(secs_now)
    for i in old_data:
        if i.split(' ')[0] == input.split(' ')[1]:
            x += 1
            #print(n)
            for j in range(len(old_data[i])):
                secs_old = int(old_data[i].time[j].split(':')[0])*3600+int(old_data[i].time[j].split(':')[1])*60+int(old_data[i].time[j].split(':')[2])
                if j == (len(old_data[i])-1):
                    secs_old_next = 24*3600
                    #print(secs_old_next)
                else:
                    secs_old_next = int(old_data[i].time[j+1].split(':')[0])*3600+int(old_data[i].time[j+1].split(':')[1])*60+int(old_data[i].time[j+1].split(':')[2])
                    #print(secs_old_next)
                if (secs_old <= secs_now) & (secs_old_next <= secs_now):
                    psum_n += old_data[i].P[j]*(secs_old_next-secs_old)
                    #print(psum_n)
                elif (secs_old <= secs_now) & (secs_old_next > secs_now):
                    psum_n += old_data[i].P[j]*(secs_now-secs_old)
                    #print(psum_n)
            if x > 2:
                break
    return (psum_n/x)

def data_received(data):
    global n, p, date, df, psum, time_v, f
    x = data.split(' ')[-8:-1]
    data = ''
    for i in x:
        data += i + ' '
    data = data[:-1]
    print(data)
    p_norm = round(norms(data))
    #print(data, n, p, p_norm)
    if data.split(" ")[3] != date:
        books = load_workbook('pandas_simple1.xlsx')
        writer = pd.ExcelWriter('pandas_simple1.xlsx', engine='openpyxl')
        writer.book = books
        df.to_excel(writer, sheet_name=data.split(" ")[1]+' '+data.split(" ")[2]+''+data.split(" ")[3], index=False)
        writer.save()
        df = pd.DataFrame({'P':[], 'week':[], 'month':[], 'date':[], 'time':[], 'year':[], 'sec':[], 'Application':[], 'valid':[]})
        if float(data.split(" ")[0]) > 50:
            newdata = pd.DataFrame([(data+' hairdryer Y').split(" ")], columns=l)
        elif (abs(1.8-float(data.split(" ")[0]))/1.8 < 0.1) | (abs(4.8-float(data.split(" ")[0]))/4.8 < 0.03) | (abs(6.8-float(data.split(" ")[0]))/6.8 < 0.03) | (abs(9-float(data.split(" ")[0]))/9 < 0.03):
            newdata = pd.DataFrame([(data+' lamp Y').split(" ")], columns=l)
        elif float(data.split(" ")[0]) > 1:
            newdata = pd.DataFrame([(data+' cellphone Y').split(" ")], columns=l)
        df = df.append(newdata, ignore_index=True)
        writer = pd.ExcelWriter('pandas_simple.xlsx', engine='xlsxwriter')
        df.to_excel(writer, sheet_name=newdata.week[0]+' '+newdata.month[0]+' '+newdata.date[0], index=False)
        writer.save()
        psum = 0
    if p > 1:
        psum += float(data.split(" ")[0])
        #print(psum)
        if abs((p-float(data.split(" ")[0]))/p) < 0.05:
            n += 1
            if n == 2:
                if float(data.split(" ")[0]) > 50:
                    newdata = pd.DataFrame([(data+' hairdryer Y').split(" ")], columns=l)
                elif (abs(1.8-float(data.split(" ")[0]))/1.8 < 0.1) | (abs(4.8-float(data.split(" ")[0]))/4.8 < 0.03) | (abs(6.8-float(data.split(" ")[0]))/6.8 < 0.03) | (abs(9-float(data.split(" ")[0]))/9 < 0.03):
                    newdata = pd.DataFrame([(data+' lamp Y').split(" ")], columns=l)
                elif float(data.split(" ")[0]) > 1:
                    newdata = pd.DataFrame([(data+' cellphone Y').split(" ")], columns=l)
                df = df.append(newdata, ignore_index=True)
                writer = pd.ExcelWriter('pandas_simple.xlsx', engine='xlsxwriter')
                df.to_excel(writer, sheet_name=newdata.week[0]+' '+newdata.month[0]+' '+newdata.date[0], index=False)
                writer.save()
                print(df)
        elif (float(data.split(" ")[0])<1):
            n = 0
            newdata = pd.DataFrame([(data+' none Y').split(" ")], columns=l)
            df = df.append(newdata, ignore_index=True)
            writer = pd.ExcelWriter('pandas_simple.xlsx', engine='xlsxwriter')
            df.to_excel(writer, sheet_name=newdata.week[0]+' '+newdata.month[0]+' '+newdata.date[0], index=False)
            writer.save()
            print(df)
        else:
            n = 0
    print('p_sum: ',round(psum), '\t p_norm: ', p_norm, '\t ratio: ',  psum/p_norm)
    if (psum/p_norm) > 1.1:
        s.send('r')
        if (float(data.split(" ")[6])-time_v)>10:            
            if float(data.split(" ")[0]) > 50:
                newdata = pd.DataFrame([(data+' hairdryer N').split(" ")], columns=l)
                f = 0
            elif (abs(1.8-float(data.split(" ")[0]))/1.8 < 0.1) | (abs(4.8-float(data.split(" ")[0]))/4.8 < 0.03) | (abs(6.8-float(data.split(" ")[0]))/6.8 < 0.03) | (abs(9-float(data.split(" ")[0]))/9 < 0.03):
                newdata = pd.DataFrame([(data+' lamp N').split(" ")], columns=l)
                f = 0
            elif float(data.split(" ")[0]) > 1:
                #print(data, type(data))
                newdata = pd.DataFrame([(data+' cellphone N').split(" ")], columns=l)
                f = 0
            else:
                f = 1
            if f == 0:
                df = df.append(newdata, ignore_index=True)
                writer = pd.ExcelWriter('pandas_simple.xlsx', engine='xlsxwriter')
                df.to_excel(writer, sheet_name=newdata.week[0]+' '+newdata.month[0]+' '+newdata.date[0], index=False)
                writer.save()
                print(df)
                speak('over limit', 'en')
            time_v = float(data.split(" ")[6])
    elif (psum/p_norm) > 1:
        s.send('y')
    elif (psum/p_norm) <= 1:
        s.send('g')
    p=float(data.split(" ")[0])
    date=data.split(" ")[3]

#import socket
#import IOT_socket
#
#sr = IOT_socket.socket_conn_Pi()

data = ''
s = BluetoothServer(data_received) 
n = 0
p = 0
f = 0
norm = 0
psum = 0
time_v = 0
starttime = time.asctime( time.localtime(time.time()) )
n = starttime.split(' ')
for i in n:
    if i == '':
        n.remove('')
        break
starttime = ''
for i in n:
    starttime += i + ' '
n = 0
date = starttime.split(" ")[2]
old_data = pd.read_excel('pandas_simple.xlsx', engine='openpyxl', sheet_name = None)  
if old_data.get((starttime.split(" ")[0]+' '+starttime.split(" ")[1]+' '+starttime.split(" ")[2]), pd.DataFrame({'P':[]})).P.any():
    df = pd.DataFrame({'P':[], 'week':[], 'month':[], 'date':[], 'time':[], 'year':[], 'sec':[], 'Application':[], 'valid':[]})
    df = old_data.get((starttime.split(" ")[0]+' '+starttime.split(" ")[1]+' '+starttime.split(" ")[2]))
    for i in range(len(df)-1):
        psum += df.P[i]*(df.sec[i+1]-df.sec[i])
else:
    df = pd.DataFrame({'P':[], 'week':[], 'month':[], 'date':[], 'time':[], 'year':[], 'sec':[], 'Application':[], 'valid':[]})
    psum = 0
old_data = pd.read_excel('pandas_simple1.xlsx', engine='openpyxl', sheet_name = None)  
l = ['P', 'week', 'month', 'date', 'time', 'year', 'sec', 'Application', 'valid']
print(psum)
print(df)

while (True):
    pass
