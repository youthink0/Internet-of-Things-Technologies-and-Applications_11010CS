import datetime
import pandas as pd
import json
import draw_chart

def get_electricity_information(df):
    if df.empty:
        return df
    df["last_sec"] = df["sec"].shift(-1)
    df["last_sec"] = df['last_sec'].fillna(df['sec']) #remove NaN
    df["time_use"] = (df["last_sec"].astype(int) - df["sec"].astype(int))
    df["supply_use"] = (df["P"].astype(float)*df["time_use"])/1000 #unit : 1000J
    #P(W)*time(S) = energy(J)
    #print(df)
    return df

def get_all_pic_and_today_df(path, today):
    df_res = pd.DataFrame()
    df_week_ago_res = pd.DataFrame()
    today_date_str = str(today)
    with pd.ExcelFile(path, engine="openpyxl") as xls:
        for sheet_name in xls.sheet_names:  #get sheet_name
            df1 = pd.read_excel(xls, sheet_name=sheet_name)
            df = get_electricity_information(df1) #put electricity information into df
            #print(df1.dtypes)

            month_tmp = datetime.datetime.strptime(df["month"][0], "%b")
            sheet_date = str(df['year'][0])+"-"+str(month_tmp.month)+"-"+str(df['date'][0])

            tmp = datetime.datetime.strptime(sheet_date, "%Y-%m-%d")
            week_ago_date = (tmp + datetime.timedelta(days=-1)).strftime("%a %b %d")
            week_ago_date = week_ago_date.replace("0", " ") #find week ago's sheet name
            print(sheet_date, tmp, week_ago_date, today)

            df_week_ago1 = pd.DataFrame()
            if week_ago_date in xls.sheet_names:
                df_week_ago1 = pd.read_excel(xls, sheet_name=week_ago_date)
                #print(df_week_ago.head(2))
            df_week_ago = get_electricity_information(df_week_ago1) #put electricity information into df
		
            
            if str(today) == sheet_name:
                df_res = df1
                df_week_ago_res = df_week_ago1
                today_date_str = sheet_date
            else:
                draw_chart.export_line_chart(df, df_week_ago, sheet_date) #draw line chart
                draw_chart.export_pie_chart(df, "supply_use", sheet_date) #draw supply_use pie chart
                draw_chart.export_pie_chart(df, "time_use", sheet_date) #draw time_use pie chart
            #print(df)

            print("------------------------------------------------------------")
    return df_res, df_week_ago_res, today_date_str
