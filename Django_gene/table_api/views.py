from django.shortcuts import render

from django.shortcuts import render
from rest_framework import viewsets, permissions, status, serializers
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.db import connection
import pandas as pd
import json
import pymysql
from rest_framework import serializers


# Database管理及操作
class DatabaseManager(object):

    _instance = None
    db_cursor = None
    db_conn = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.db_conn = pymysql.connect(
                                    host="localhost",
                                    database="lab_training",
                                    user="shouweihuang",
                                    password="jj533675",
                                    port=3306,
                                    charset='utf8',
                                    cursorclass=pymysql.cursors.DictCursor
        )

        self.db_cursor = self.db_conn.cursor()
        print("SUCCESS: Connection to the database succeeded")
        
    
    def query_GeneAnnotation(self, **kwargs):
        # 接收DataTable傳來的參數
        
        # 第幾次操作table, eg:0, 1, 2...
        draw = int(kwargs.get('draw', None)[0])
        # 顯示的資料筆數, eg: 10, 25...
        length = int(kwargs.get('length', None)[0]) 
        # 從第幾筆顯示, eg:0, 10, 20
        start = int(kwargs.get('start', None)[0]) 
        # 輸入框內容: eg:search content
        search_value = kwargs.get('search[value]', None)[0]
        # 排序方式 eg: asc/desc
        # order_column = kwargs.get('order[0][column]', None)[0] 
        # 由哪個column排序 eg:0, 1...
        order = kwargs.get('order[0][dir]', None)[0] 

        # 資料庫拿取資料
        sql = """
            SELECT * FROM `Lbarbarum_table` ORDER BY `Lbarbarum_table`.%s %s;;
        """%('index', order)
        self.db_cursor.execute(sql)
        data = self.db_cursor.fetchall()
        
        # 對資料篩選
        
        # 選取包含search value的row
        if len(search_value) != 0:
            data = [dictionary for dictionary in data if any(search_value in value for value in dictionary.values())]
            
        # 留下需要的資料筆數
        count = len(data)
        if count > length:
            data = data[start: start + length]

        
        # 回傳以通過篩選的資料
        return {
            'query_data':data,
            'count':count,
            'total':33431,
            'draw':draw
        }
     
# API
class UPDATEGEBEANNOTATIONViewSet(viewsets.ModelViewSet):
    queryset = None
    response = None
    parser_classes = (JSONParser,)
    dbm = DatabaseManager()

    def list(self, request, **kwargs):
        try:
            # 接收通過篩選的資料庫的值
            res = self.dbm.query_GeneAnnotation(**request.query_params)
            result = dict()
            result['data'] = res['query_data']
            result['draw'] = res['draw']
            result['recordsTotal'] = res['total']
            result['recordsFiltered'] = res['count']
            return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)

        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)
