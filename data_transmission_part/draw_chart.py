import datetime
import pandas as pd
import matplotlib.pyplot as plt
import pytab as pt
from pandas.plotting import table 

def export_line_chart(df, df_week_ago, today):
    ax = df.plot(x='time', y = 'P', kind = 'line', c = "r", style=".-", label="today", rot=45, grid=False)
    
    # 設定圖例，參數為標籤、位置
    ax.legend(loc = 'best')
    ax.set_xlabel("Time", fontweight = "bold")                # 設定x軸標題及粗體
    ax.set_ylabel("Power Supply", fontweight = "bold")    # 設定y軸標題及粗體
    ax.set_title(label=str(today)+" electric folding line diagram", fontsize = 15, fontweight = "bold", y = 1.1)   
    # 設定標題、文字大小、粗體及位置
    ax.set_facecolor('white')
    
    if df_week_ago.empty:
        fig = ax.get_figure()
    else:
        plot = df_week_ago.plot(x='time', y = 'P', kind = 'line', c = "k", style='s-', label="week ago", 
                                ax=ax, rot=45, grid=False) # 將x軸數字旋轉45度，避免文字重疊, 且移除格子
        ma = df_week_ago['supply_use'].rolling(3).mean() #計算均線
        mstd = df_week_ago['supply_use'].rolling(3).std() #計算標準差
        plot.fill_between(mstd.index, df_week_ago['supply_use'], ma+1*mstd, color='0.3', alpha=0.2) #draw *1 標準差
        plot.fill_between(mstd.index, ma+1*mstd, ma+2*mstd, color='0.7', alpha=0.2) #draw *2 標準差
        
        fig = plot.get_figure()
    fig.savefig("picture/"+str(today)+"_Line chart.jpg",   # 儲存圖檔
                bbox_inches='tight',               # 去除座標軸占用的空間
                pad_inches=0.0,
                transparent=True)

size = []
unit_flag = 0
def absolute_value(val):
    a  = sum(size)*val/100
    if unit_flag:
        return '{:.1f}%\n{:.2f} min'.format(val, a)
    else:
        return '{:.1f}%\n{:.2f} KJ'.format(val, a)
    
def export_pie_chart(df, col, today):
    #pie chart
    plt.figure(figsize=(6,9))    # 顯示圖框架大小
    lamp_sum = df.loc[df['Application'] == "lamp", col].sum()
    cellphone_sum = df.loc[df['Application'] == "cellphone", col].sum()
    hairdryer_sum = df.loc[df['Application'] == "hairdryer", col].sum()
    #print(lamp_sum, hairdryer_sum)
    labels = ["lamp", "cellphone", "hairdry"]      # 製作圓餅圖的類別標籤
    global size
    global unit_flag
    if col == "time_use":
        unit_flag = 1
        size = [lamp_sum/60, cellphone_sum/60, hairdryer_sum/60]                         # 製作圓餅圖的數值來源
    else:
        unit_flag = 0
        size = [lamp_sum, cellphone_sum, hairdryer_sum]
    plt.pie(size,                           # 數值
            labels = labels,                # 標籤
            autopct = absolute_value,       # 將數值百分比並留到小數點一位且保留真實數值
            pctdistance = 0.6,              # 數字距圓心的距離
            textprops = {"fontsize" : 12},  # 文字大小
            shadow=True)                    # 設定陰影


    plt.axis('equal')                                          # 使圓餅圖比例相等
    plt.title(str(today) + " " + col + " ratio", {"fontsize" : 18})  # 設定標題及其文字大小
    plt.legend(loc = "best")                                   # 設定圖例及其位置為最佳

    plt.savefig('picture/'+str(today) + " " + col + " ratio.jpg",   # 儲存圖檔
                bbox_inches='tight',               # 去除座標軸占用的空間
                pad_inches=0.0,                    # 去除所有白邊
                transparent=True)
    plt.close()      # 關閉圖表

def draw_table(df):
    data = df[["week", "month", "date", "time", "Application"]].astype(str)
    # DataFrame=>png
    plt.figure('invalid table')            # 視窗名稱
    ax = plt.axes(frame_on=False)# 不要額外框線
    ax.xaxis.set_visible(False)  # 隱藏X軸刻度線
    ax.yaxis.set_visible(False)  # 隱藏Y軸刻度線
    pd.plotting.table(ax, data, loc='center') #將mytable投射到ax上，且放置於ax的中間
    plt.savefig('picture/'+ "Invalid Records" + ".jpg", transparent=True)     # 存檔
    plt.close()
    


