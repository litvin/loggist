#!/usr/bin/python3.3
# -*- coding: utf-8 -*-

import sys,  pprint, re, os, mysql.connector
from datetime import date, datetime, timedelta

DIRNAME="/usr/local/XPGK/billing/"
SERVERNAME="corp"
PREFIX=""

cnx = mysql.connector.connect(user='loggist', password='', host='db2.avantel.ru', database='loggist')

ddd = {
'LOG-NAME':'',
'LOG-TIME':'',
'DIALPEER-NAME':'',
'DISCONNECT-CODE-LOCAL':'',
'DISCONNECT-CODE-Q931':'',
'DISCONNECT-TIME':'',
'DST-CODEC':'',
'DST-IP':'',
'DST-NAME':'',
'DST-NUMBER-BILL':'',
'DST-NUMBER-IN':'',
'DST-NUMBER-OUT':'',
'ELAPSED-TIME':'',
'HOST':'',
'LAST-CHECKED-DIALPEER':'',
'PDD-REASON':'',
'PDD-TIME':'',
'QOS':'',
'ROUTE-RETRIES':'',
'SCD-TIME':'',
'SETUP-TIME':'',
'SRC-CODEC':'',
'SRC-IP':'',
'SRC-NAME':'',
'SRC-NUMBER-BILL':'',
'SRC-NUMBER-IN':'',
'SRC-NUMBER-OUT':''
}


def _str_sql():
    str1 = "INSERT INTO "+SERVERNAME+" ("
    str2 = "VALUES ("

    for k, v in ddd.items():
      str1 = str1+k+", "
      str2 = str2+"%("+k+")s, "
    str1 = str1.replace("-", "_")
    return( str1[0:-2]+") "+str2[0:-2]+")" )

def _file_parse(dirname, filename):
   dl = ddd.copy()
   add_val = ddd.copy()
   add_sql = _str_sql()

   f = open(dirname+filename, 'r')

   for line in f:
     l=("LOG-NAME="+filename+", LOG-TIME="+line)
     dl.update(item.split("=") for item in l.split(", "))
     for k, v in dl.items():
       if k in ddd:
         if k in "DISCONNECT-TIME":
           v =  (datetime.strptime(v, '%H:%M:%S.%f %z %a %b %d %Y')).strftime("%Y-%m-%d %H:%M:%S%z")
           add_val.update({k:v})
         elif k in  "SETUP-TIME":
           v =  (datetime.strptime(v, '%H:%M:%S.%f %z %a %b %d %Y')).strftime("%Y-%m-%d %H:%M:%S%z")
           add_val.update({k:v})
         elif k in "LOG-TIME":
           v = (datetime.strptime(v, '%a %b %d %H:%M:%S %Y')).strftime("%Y-%m-%d %H:%M:%S%z")
           add_val.update({k:v})
         else:
           add_val.update({k:v})
     cursor.execute(add_sql, add_val)
     dl = ddd.copy()
     add_val = ddd.copy()   

def _list_db_f():
   query  = "SELECT DISTINCT LOG_NAME FROM "+SERVERNAME
   cursor.execute(query)
   data =  cursor.fetchall()
   list_add_file=[]
 
   for rec in data:
     list_add_file.append(rec[0])
   return(list_add_file)

def _list_l(directory):
   list_file=[]
   list=os.listdir(directory)
   for file in list:
    if file.startswith(PREFIX):
      list_file.append(file)
   return(list_file)

def _data_insert():
   for filename in _list_l(DIRNAME):
       if not filename in _list_db_f():
#          print("New file: "+filename)
          _file_parse(DIRNAME, filename)
          cnx.commit()
#          print("File "+filename+" inserted OK." )
#       else:
#          print("file in db: "+filename)
          
cursor = cnx.cursor(buffered=True)
_data_insert()	
cursor.close()
cnx.close() 

