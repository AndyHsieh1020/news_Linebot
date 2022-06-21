import csv
import os, sys


os.chdir(os.getcwd())
with open('company.csv', newline='') as csvfile:

  # 讀取 CSV 檔內容，將每一列轉成一個 dictionary
  rows = csv.DictReader(csvfile)

  # 以迴圈輸出指定欄位
  json_str="["
  for row in rows:
    json_str+="{\"canonicalForm\": \""+row['公司簡稱']+"\",\"list\":[\""+ row['公司代號'] +"\",\""+ row['公司簡稱'] +"\",\""+row['公司名稱']+"\"]},"
    ##print(row['公司簡稱'],row['公司代號'] )
json_str=json_str[:-1]
json_str+="]"
path = '公司簡稱.json'
f = open(path, 'w')
f.write(json_str)
f.close()