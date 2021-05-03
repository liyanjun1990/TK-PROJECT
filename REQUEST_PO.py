import pandas as pd
import sys
## need change
#sys.path.append(r"C:\Users\NUC Accounting\PycharmProjects\pythonProject\AUTOPROCESSOR\library\\")
sys.path.append(r"C:\Users\admin\PycharmProjects\open_cv\Eccang\\")
#"https://eccang.yuque.com/books/share/df2ca396-46f5-4a51-a33e-73794059bb1d"

import credential
import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
import math
import numpy

url = f"http://{credential.ECANG_API}/default/svc-open/web-service-v2"


service = 'getPurchaseOrders'
userName = 'acc006'
userPass = 'ptc!2345'
paramsJson = '{"po_codes":["PO421043030001"]}'

#headers = {'content-type': 'application/soap+xml'}
headers = {'content-type': 'text/xml'}


def round_up(n, decimals=0):
  multiplier = 10 ** decimals
  return math.ceil(n * multiplier) / multiplier

def request_eccang(userName,userPass,paramsJson,service = 'getPurchaseOrders'):
  body = f"""<?xml version="1.0" encoding="UTF-8"?>
  <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:ns1="http://www.example.org/Ec/">
    <SOAP-ENV:Body>
      <ns1:callService>
        <paramsJson>{paramsJson}</paramsJson>
        <userName>{userName}</userName>
        <userPass>{userPass}</userPass>
        <service>{service}</service>
      </ns1:callService>
    </SOAP-ENV:Body>
  </SOAP-ENV:Envelope>"""
  return body

def response_to_dict(response):
  soup =BeautifulSoup(response,'lxml')
  soup_response = soup.find_all('response')
  dict_response = json.loads(soup_response[0].text)
  return dict_response

def request_po(po_number):
    body = request_eccang(userName=userName,userPass=userPass,paramsJson=f'{{"po_codes":["{po_number}"]}}',service=service)
    EC_response = requests.Session()
    response = EC_response.post(url,data=body,headers=headers)
    dict = response_to_dict(response.text)
    data = dict['data'][0]
    detail = dict['data'][0]['detail']
    needed_column_detail = ['product_sku','qty_expected','qty_pay','total_price']
    df = pd.DataFrame(detail)[needed_column_detail]
    return df

import tkinter as tk
from tkinter import ttk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Check_price"
        self.hi_there["command"] = self.openwindow
        self.hi_there.pack(side="top")

    def create_table_view(self,frame,df):

        my_tree = ttk.Treeview(frame)
        my_tree = ttk.Treeview(frame)
        my_tree["column"] = list(df.columns)
        my_tree["show"] = "headings"

        for column in my_tree["column"]:
            my_tree.heading(column, text=column)
        df_rows = df.to_numpy().tolist()
        for row in df_rows:
            my_tree.insert("", "end", values=row)

        my_tree.pack()

    def openwindow(self):

        po_number = "PO421043030001"
        df = request_po(po_number=po_number)
        new_window = tk.Toplevel(root)

        new_window.geometry("1000x500")
        new_window.title("po_number")

        self.create_table_view(frame=new_window,df=df)

root = tk.Tk()
root.geometry("+1920+0")
app = Application(master=root)
app.mainloop()
