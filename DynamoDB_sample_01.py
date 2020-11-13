import sys

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime as dt

import boto3
from boto3.dynamodb.conditions import Key

import argparse
parser = argparse.ArgumentParser(description='Sencensing and upload script')
parser.add_argument( '-l','--location', default='anritsu_headquarters', help='Sensor location name' )

# from ctypes import *
# user32 = windll.user32

import tkinter
from tkinter import messagebox
#tk = tkinter.Tk()
#tk.withdraw()

def query_items(locationname, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('t_sensordata')
    response = table.query(
        KeyConditionExpression=Key('locationname').eq(locationname)
    )
    return response['Items']


# グラフ描画
def plot_graph( x_temp, y_temp, title="Not Defined" ):

#    for i in range(len(x_temp)):
#        print( x_temp[i], y_temp[i] )


    # Instanse of Graph
    fig = plt.figure()
    fig.subplots_adjust(bottom=0.25, right=0.75)


    axes_temp = fig.add_subplot(111)
    axes_temp.set_ylabel("Celsius")
    axes_temp.grid(which = "major", axis = "x")
	
    axes_temp.xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))

#    axes_temp_predict = fig.add_subplot(111)

    axes_temp.plot(x_temp, y_temp, "b-", label="Measured Temp.", linewidth = 1.5)

    axes_temp.tick_params(axis='x', labelrotation=90 )

    plt.rc('legend', fontsize = 'small')
#    fig.legend(loc='upper center', bbox_to_anchor=(0.45, 0.08), ncol=3)
#    plt.title( sample_date_start.strftime('%Y/%m') + ' - ' + sample_date_end.strftime('%Y/%m') )
    plt.title( title )
    plt.show()

    return()



if __name__ == '__main__':

    args = parser.parse_args()
    query_location = args.location

#    print(f"Items from {query_location}")
    items = query_items(query_location)
	
    x_temp = []
    y_temp = []
    for item in items:
#        print(item['locationname'], ":", item['temperature'])
        x_temp.append(dt.fromtimestamp( item['unixtime'] ))
        y_temp.append(item['temperature'])

    if 0 == len(x_temp):
#        user32.MessageBoxA( 0, "Hello, MessageBox!", "Python to Windows API", 0x00000010)
        root = tkinter.Tk()
        root.withdraw()
        messagebox.showerror( "Table Error", "Can't find table of your specified location." )
        exit()

    else:
        plot_graph(x_temp, y_temp, "Temperature of " + query_location )


    exit()

