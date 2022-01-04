#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import pandas as pd
import time
import IOT_socket

col = ['P', 'week', 'month', 'date', 'time', 'year', 'sec', 'Application', 'valid']
inputdata = ["9.0","Thu","Dec","23","22:55:59","2021","1640271360","lamp","Y"]

if __name__ == "__main__":  
    s = IOT_socket.socket_conn_Pi()
    while True:
        
        for i in range(5):
        #inputdata = list(map(int,input("\nEnter the numbers : ").strip().split()))[:2]

            df = pd.DataFrame([inputdata], columns = col)
            print(df)
            df_string = df.to_json()
            
            s.send(df_string.encode())


            indata = s.recv(1024)
            if len(indata) == 0: # connection closed
                s.close()
                print('server closed connection.')
                break
            print('recv: ' + indata.decode())
            
            time.sleep(7)
            df["P"] = str(i*i + 10)
