#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import json
import IOT_socket
import draw_chart
import preprocess

if __name__ == "__main__":
    s = IOT_socket.socket_conn_PC()
    
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    #today = today.replace("0", " ")

    #-------need to restart everyday-----------#
    today_df, today_week_ago_df1 = preprocess.get_all_pic_and_today_df('data_storage/pandas_simple.xlsx', today)
    today_week_ago_df = preprocess.get_electricity_information(today_week_ago_df1) #put electricity information into df

    conn, addr = s.accept()
    print('connected by ' + str(addr))

    while True:
        indata = conn.recv(1024)
        if len(indata) == 0: # connection closed
            conn.close()
            print('client closed connection.')
            break
        
        df_string = indata.decode()
        #print(df_string)
        tmp = json.loads(df_string)
        #print(tmp)
        #print(type(tmp))

        df_again = pd.DataFrame.from_dict(tmp)
        #print(df_again)
        today_df = pd.concat([today_df, df_again], ignore_index=True)
        
        tmp_df = preprocess.get_electricity_information(today_df)
        tmp_df["P"] = tmp_df["P"].astype(float)
        if not tmp_df.empty:
            preprocess.get_invalid_information(today_df)
            draw_chart.export_line_chart(tmp_df, today_week_ago_df, today)
            draw_chart.export_pie_chart(tmp_df, "supply_use", today)
            draw_chart.export_pie_chart(tmp_df, "time_use", today)
            draw_chart.draw_table(tmp_df, today+"_table")
        
        tmp_day = datetime.datetime.now().strftime("%Y-%m-%d")
        if tmp_day != today:
            #today_df.to_excel('data_storage/pandas_simple.xlsx', sheet_name=str(today)) 
            today_df = today_df[0:0]
            today = datetime.datetime.now().strftime("%a %b %d")
            today = today.replace("0", " ")
        #outdata = 'echo ' + indata.decode()
        outdata = 'data echo confirmed'
        conn.send(outdata.encode())
