import io
import os
import sqlite3
import subprocess
import uuid
from zipfile import ZipFile
import zipfile
from flask import Flask, jsonify, make_response, redirect, render_template, request, send_file, send_from_directory, url_for
# 确保当前工作目录是项目目录

from flask_cors import CORS
from PIL import Image
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from collections import defaultdict

import pytz

# 应用其他设置之后添加 CORS 支持

from ts import textUtil
# from XuNet import pgmUtil
# from XuNet import stego_detector

from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from utils import find_file_with_extension, find_recordOperation, find_recordRes, find_recordType



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['SERVER_TIMEOUT'] = 6000  # 设置超时时间为 300 秒
app.config['TIMEOUT'] = 5000  # 设置连接超时时间为5秒
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB
# CORS(app)
# CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5000"}})
# CORS(app=app, supports_credentials=True, resources={r"/*": {"origins": "*"}})
CORS(app, resources=r'/*', supports_credentials=True)

# 创建了网址 /show/info 和函数index之间的对应关系，以后用户在浏览器上访问/show/info，网站自动执行index函数
@app.route('/')
def text():
    return render_template('text.html')

@app.route('/index/')
def index():
    return render_template('index.html')


@app.route("/api/login123", methods=["POST"])
def login():
    if request.method == "POST":
        username = request.json.get('username')
        password = request.json.get('password')

        print(username)
        # 注意：实际生产环境中不应该打印密码或任何敏感信息

        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            
            # 检查用户名是否存在
            cur.execute("SELECT userId, userPassword FROM user WHERE userName=?", (username,))
            result = cur.fetchone()
            
            if result:
                user_id, stored_password = result
                # 用户存在，检查密码是否匹配
                if check_password_hash(stored_password, password):
                    data = {
                        'login': True,
                        'message': "登录成功",
                        'uid': user_id,  # 使用从数据库获取的userId
                        'name': username,
                        'token': "7D354bdB-FB33-DadD-6c7d-BBe6c0A753e4"
                    }
                else:
                    data = {
                        'login': False,
                        'message': "密码错误，请重新输入"
                    }
            else:
                # 用户不存在，创建新用户，并加密密码
                hashed_password = generate_password_hash(password)
                cur.execute("INSERT INTO user (userName, userPassword) VALUES (?, ?)", (username, hashed_password))
                con.commit()
                
                # 获取新创建的userId
                cur.execute("SELECT last_insert_rowid() FROM user")
                user_id = cur.fetchone()[0]
                
                data = {
                    'login': True,
                    'message': "新用户注册成功，登录成功",
                    'uid': user_id,  # 使用新创建的userId
                    'name': username,
                    'token': "7D354bdB-FB33-DadD-6c7d-BBe6c0A753e4"
                }
        
        con.close()

        return jsonify(data)


@app.route("/api/getNavlist", methods=["GET"])
def getNavlist():
    # 从查询字符串中获取参数
    userId = request.args.get('userId')

    print("userId:")
    print(userId)

    # 连接到数据库
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        
        query = "SELECT * FROM user WHERE userId=?"
        params = [userId]  # 初始化参数列表，至少包含一个参数

        cur.execute(query, params)  # 执行查询
        user = cur.fetchone()  # 获取查询结果的第一行
        
        if user:
            # 如果查询到了用户，userType字段是第二列（索引为1）
            if user[1] == 0:
                print("用户类型为0")
                # 在这里执行用户类型为1时的操作
                        # 定义 head 部分
                data = [
                    {
                        'path': '/home',
                        'name': '首页'
                    },
                    {
                        'name': '深度学习算法',
                        'child': [
                            {
                                'path': '/stego/jpgDL',
                                'name': 'jpg图像'
                            },
                            {
                                'path': '/stego/txtDL',
                                'name': 'txt生成式文本'
                            },
                            {
                                'path': '/stego/wavDL',
                                'name': 'wav音频'
                            },
                            {
                                'path': '/stego/aviDL',
                                'name': 'avi视频'
                            }
                        ]
                    },
                    {
                        'name': '非深度学习算法',
                        'child': [
                            {
                                'path': '/stego/bmp',
                                'name': 'bmp图像'
                            },
                            {
                                'path': '/stego/wav',
                                'name': 'wav音频'
                            },
                            {
                                'path': '/stego/mid',
                                'name': 'mid音频'
                            },
                            {
                                'path': '/stego/wma',
                                'name': 'wma音频'
                            },
                            {
                                'path': '/stego/mp4',
                                'name': 'mp4视频'
                            }
                        ]
                    },
                    {
                        'name': '记录查询',
                        'child': [
                            {
                                'path': '/record/statistics',
                                'name': '使用次数'
                            },
                            {
                                'path': '/record/type',
                                'name': '类型统计'
                            },
                            {
                                'path': '/record/history',
                                'name': '历史记录'
                            }
                        ]
                    },
                    {
                        'path': '/theme',
                        'name': '系统设置'
                    }
                ]


                print(data)

                return jsonify(data)  # 将数据序列化为 JSON 并返回

            elif user[1] == 1:
                print("用户类型为1")
                data = [
                    {
                        'path': '/home',
                        'name': '首页'
                    },
                    {
                        'name': '记录查询',
                        'child': [
                            {
                                'path': '/record/statistics',
                                'name': '使用次数'
                            },
                            {
                                'path': '/record/type',
                                'name': '类型统计'
                            },
                            {
                                'path': '/record/history',
                                'name': '历史记录'
                            }
                        ]
                    },
                    {
                        'path': '/theme',
                        'name': '系统设置'
                    }
                ]

                print(data)

                return jsonify(data)  # 将数据序列化为 JSON 并返回
        else:
            print("未找到用户")
            # 在这里执行未找到用户时的操作



# 定义路由和视图函数
@app.route('/api/upload', methods=['POST'])
def upload_file():
    # 检查是否有文件在请求中
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    # 如果用户没有选择文件，浏览器可能会提交一个没有文件名的空部分
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        # 为文件名增加随机前缀以避免覆盖
        # 生成随机 UUID

        # 使用 os.path.splitext 获取文件后缀名
        _, file_extension = os.path.splitext(file.filename)

        # 将后缀名转换为小写
        file_extension = file_extension.lower()

        file_extension = file_extension[1:].lower()

        print(file_extension)  # 输出: txt


        random_filenameJPG = str(uuid.uuid4()) + "." + file_extension
        # 使用 secure_filename 来确保生成的文件名是安全的
        secure_random_filenameJPG = secure_filename(random_filenameJPG)

        if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], file_extension)):
            os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], file_extension))

        # 保存文件到指定目录
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_extension, secure_random_filenameJPG))
        return jsonify({'message': 'File uploaded successfully', 'filename': secure_random_filenameJPG}), 200


@app.route('/api/download', methods=['GET'])
def download():
    filepath = request.args.get('filepath')
    base, ext = os.path.splitext(filepath)
    # return send_from_directory(filepath, "stego" + ext, as_attachment=True)
    return send_file(filepath, as_attachment=True, download_name='stego' + ext)


@app.route("/api/getStatistics", methods=["GET"])
def getStatistics():
    # 从查询字符串中获取参数
    userId = request.args.get('userId')
    days = int(request.args.get('days', 7))  # 默认值为 7

    print(userId, days)

    userType = 0

    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        
        query = "SELECT * FROM user WHERE userId=?"
        params = [userId]  # 初始化参数列表，至少包含一个参数

        cur.execute(query, params)  # 执行查询
        user = cur.fetchone()  # 获取查询结果的第一行
        
        if user:
            # 如果查询到了用户，userType字段是第二列（索引为1）
            if user[1] == 0:
                userType = 0
            elif user[1] == 1:
                userType = 1
        else:
            print("未找到用户")
        

    # 连接到数据库
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        
        query = "SELECT recordTime, COUNT(*) as count FROM record WHERE recordTime BETWEEN ? AND ?"

        
        # 获取当前日期，并调整8小时的时间偏移
        today = datetime.now() + timedelta(hours=32)
        today = today.date()  # 重置时间为0点0分0秒
        start_date = today - timedelta(days=days)
        
        # 格式化日期为 'YYYY-MM-DD' 格式
        today_str = today.strftime('%Y-%m-%d')
        start_date_str = start_date.strftime('%Y-%m-%d')

        print(today_str, start_date_str)

        params = [start_date_str, today_str]  # 初始化参数列表，至少包含一个参数

        if userType == 0:
            query += " AND recordUser = ?"
            params.append(userId)  # 添加 recordType 参数

        query += " GROUP BY recordTime ORDER BY recordTime ASC"

        records = cur.execute(query, tuple(params))  # 使用 tuple 确保参数是正确的类型

        # 获取查询结果
        records = cur.fetchall()

        print(records)

        # 创建一个字典来存储每天的计数
        daily_counts = defaultdict(int)

        # 遍历查询结果，累加每天的计数
        for recordTime, count in records:
            date_part = recordTime.split(' ')[0]  # 获取日期部分
            daily_counts[date_part] += count

        print(daily_counts)

        # 创建一个包含当前日期前7天日期的列表
        date_range = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(days, -1, -1)]

        # 初始化结果列表，所有天的计数初始为0
        result_list = [0] * days

        # 填充结果列表，使用查询到的计数
        for i, date in enumerate(date_range):
            result_list[days - i - 1] = daily_counts.get(date, 0)

        result_list.reverse()
        print(result_list)

        return jsonify(result_list)
    

@app.route("/api/getStatisticsType", methods=["GET"])
def getStatisticsType():
    # 从查询字符串中获取参数
    userId = request.args.get('userId')

    print(userId)

    userType = 0

    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        
        query = "SELECT * FROM user WHERE userId=?"
        params = [userId]  # 初始化参数列表，至少包含一个参数

        cur.execute(query, params)  # 执行查询
        user = cur.fetchone()  # 获取查询结果的第一行
        
        if user:
            # 如果查询到了用户，userType字段是第二列（索引为1）
            if user[1] == 0:
                userType = 0
            elif user[1] == 1:
                userType = 1
        else:
            print("未找到用户")

    # 连接到数据库
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        
        query = "SELECT recordType, COUNT(*) as count FROM record"

        params = []  # 初始化参数列表，至少包含一个参数

        if userType == 0:
            query += " WHERE recordUser = ?"
            params.append(userId)  # 添加 recordType 参数

        query += " GROUP BY recordType ORDER BY recordTime ASC"

        records = cur.execute(query, tuple(params))  # 使用 tuple 确保参数是正确的类型
        
        # 获取查询结果
        records = cur.fetchall()

        print(records)

        # 创建一个字典来存储每天的计数
        daily_counts = defaultdict(int)

        # 遍历查询结果，累加每天的计数
        for recordType, count in records:
            daily_counts[recordType] += count

        print(daily_counts)

        formatted_data = []

        # 遍历 daily_counts 字典
        for date, count in daily_counts.items():

            type_name = find_recordType(date)  # 确保日期是字符串格式

            # 为每个日期创建一个字典，并添加到列表中
            formatted_data.append({
                'value': count,
                'name': type_name  # 确保日期是字符串格式
            })

        print(formatted_data)

        return jsonify(formatted_data)


@app.route("/api/getHistory", methods=["GET"])
def getHistory():
    # 从查询字符串中获取参数
    userId = request.args.get('userId')
    recordTime = request.args.get('time')
    recordType = request.args.get('type')
    currentPage = int(request.args.get('currentPage', 1))  # 默认为第一页
    pageSize = int(request.args.get('pageSize', 10))  # 默认每页10条

    print(recordTime, recordType)
    print(userId, currentPage, pageSize)

    userType = 0

    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        
        query = "SELECT * FROM user WHERE userId=?"
        params = [userId]  # 初始化参数列表，至少包含一个参数

        cur.execute(query, params)  # 执行查询
        user = cur.fetchone()  # 获取查询结果的第一行
        
        if user:
            # 如果查询到了用户，userType字段是第二列（索引为1）
            if user[1] == 0:
                userType = 0
            elif user[1] == 1:
                userType = 1
        else:
            print("未找到用户")


    # 连接到数据库
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()

        query = "SELECT * FROM record"
        query += " INNER JOIN user ON record.recordUser = user.userId"  # 联接 
        params = []  # 初始化参数列表，至少包含一个参数

        if userType == 0:
            if len(params) == 0:
                query += " WHERE recordUser=?"
            else:
                query += " AND recordUser=?"
            params.append(userId)

        if recordTime is not None:
            # 将字符串转换为datetime对象
            utc_dt = datetime.strptime(recordTime, "%Y-%m-%dT%H:%M:%S.%fZ")

            # 将UTC时间转换为UTC时区的datetime对象
            utc_dt = pytz.utc.localize(utc_dt)

            # 定义东八区时区
            china_timezone = pytz.timezone('Asia/Shanghai')

            # 将UTC时间转换为东八区时间
            china_dt = utc_dt.astimezone(china_timezone)

            # 格式化为数据库中DATETIME类型的日期部分
            formatted_date = china_dt.strftime("%Y-%m-%d")

            print(formatted_date)

            # # 添加对当天记录的查询条件
            # query += " AND DATE(recordTime)>=?"
            # params.append(formatted_date + " 00:00:00")  # 添加 recordTime 开始日期参数

            # # 添加对当天记录的查询条件
            # query += " AND DATE(recordTime)<=?"
            # params.append(formatted_date + " 23:59:59")  # 添加 recordTime 结束日期参数

            if len(params) == 0:
                query += " WHERE DATE(recordTime)=?"
            else:
                query += " AND DATE(recordTime)=?"
            params.append(formatted_date)  # 添加 recordTime 参数
            # query += " AND recordTime=?"
            # params.append(recordTime)  # 添加 recordTime 参数

        if recordType is not None:
            if len(params) == 0:
                query += " WHERE recordType=?"
            else:
                query += " AND recordType=?"
            params.append(recordType)  # 添加 recordType 参数

        query += " ORDER BY recordTime DESC"

        # 添加分页查询的SQL语句
        offset = (currentPage - 1) * pageSize
        query += " LIMIT ? OFFSET ?"
        params.extend([pageSize, offset])

        print(query)


        records = cur.execute(query, tuple(params))  # 使用 tuple 确保参数是正确的类型

        rows = cur.fetchall()  # 获取所有记录

        # 将记录转换为列表或字典
        data = []
        for row in rows:
            data.append(dict(record=row))  # 假设每行数据是一个元组，将其转换为字典

        head = []

        if userType == 0:
            # 定义 head 部分
            head = [
                # {'key': 'recordId', 'name': '记录ID'},
                # {'key': 'recordUser', 'name': '用户ID'},
                {'key': 'recordType', 'name': '任务类型'},
                {'key': 'recordTime', 'name': '记录时间'},
                {'key': 'recordRes', 'name': '任务结果'},
                {'key': 'recordRemark', 'name': '任务描述'}
            ]
        elif userType == 1:
            # 定义 head 部分
            head = [
                # {'key': 'recordId', 'name': '记录ID'},
                {'key': 'recordUser', 'name': '用户'},
                {'key': 'recordType', 'name': '任务类型'},
                {'key': 'recordTime', 'name': '记录时间'},
                {'key': 'recordRes', 'name': '任务结果'},
                {'key': 'recordRemark', 'name': '任务描述'}
            ]

        # 转换 body 部分
        body = []
        for item in data:
            record = item['record']

            print("record:")
            print(record)

            recordItem_type = find_recordType(int(record[2]))
            recordItem_res = find_recordRes(int(record[4]))
            recordItem_operation = find_recordOperation(int(record[4]))


            lines = record[5].splitlines()
            recordItem_remark = lines[-1] if lines else record[5]

            if userType == 0:

                body.append({
                    # 'recordId': record[0],
                    # 'recordUser': record[1],
                    'recordType': recordItem_type,
                    'recordTime': record[3],
                    'recordRes': recordItem_res,
                    'recordRemark': recordItem_remark,
                    "operation": recordItem_operation
                    # 'other': record[6]  # 如果需要，也可以添加其他信息
                })

            elif userType == 1:

                body.append({
                    # 'recordId': record[0],
                    'recordUser': record[9],
                    'recordType': recordItem_type,
                    'recordTime': record[3],
                    'recordRes': recordItem_res,
                    'recordRemark': recordItem_remark,
                    "operation": recordItem_operation
                    # 'other': record[6]  # 如果需要，也可以添加其他信息
                })


        formatted_data = {
            'head': head,
            'body': body
        }

        print(formatted_data)

        return jsonify(formatted_data)  # 将数据序列化为 JSON 并返回

    # # 连接到数据库
    # with sqlite3.connect("database.db") as con:
    #     cur = con.cursor()
        
    #     query = "SELECT * FROM record WHERE recordUser=?"
    #     params = [userId]  # 初始化参数列表，至少包含一个参数

    #     if recordTime is not None:
    #         # 将字符串转换为datetime对象
    #         utc_dt = datetime.strptime(recordTime, "%Y-%m-%dT%H:%M:%S.%fZ")

    #         # 将UTC时间转换为UTC时区的datetime对象
    #         utc_dt = pytz.utc.localize(utc_dt)

    #         # 定义东八区时区
    #         china_timezone = pytz.timezone('Asia/Shanghai')

    #         # 将UTC时间转换为东八区时间
    #         china_dt = utc_dt.astimezone(china_timezone)

    #         # 格式化为数据库中DATETIME类型的日期部分
    #         formatted_date = china_dt.strftime("%Y-%m-%d")

    #         print(formatted_date)

    #         # # 添加对当天记录的查询条件
    #         # query += " AND DATE(recordTime)>=?"
    #         # params.append(formatted_date + " 00:00:00")  # 添加 recordTime 开始日期参数

    #         # # 添加对当天记录的查询条件
    #         # query += " AND DATE(recordTime)<=?"
    #         # params.append(formatted_date + " 23:59:59")  # 添加 recordTime 结束日期参数

    #         query += " AND DATE(recordTime)=?"
    #         params.append(formatted_date)  # 添加 recordTime 参数
    #         # query += " AND recordTime=?"
    #         # params.append(recordTime)  # 添加 recordTime 参数

    #     if recordType is not None:
    #         query += " AND recordType=?"
    #         params.append(recordType)  # 添加 recordType 参数

    #     query += " ORDER BY recordTime DESC"

    #     # 添加分页查询的SQL语句
    #     offset = (currentPage - 1) * pageSize
    #     query += " LIMIT ? OFFSET ?"
    #     params.extend([pageSize, offset])


    #     records = cur.execute(query, tuple(params))  # 使用 tuple 确保参数是正确的类型

    #     rows = cur.fetchall()  # 获取所有记录

    #     print(records)

    #     # 将记录转换为列表或字典
    #     data = []
    #     for row in rows:
    #         data.append(dict(record=row))  # 假设每行数据是一个元组，将其转换为字典

    #     print(data)

    #     # 定义 head 部分
    #     head = [
    #         # {'key': 'recordId', 'name': '记录ID'},
    #         # {'key': 'recordUser', 'name': '用户ID'},
    #         {'key': 'recordType', 'name': '任务类型'},
    #         {'key': 'recordTime', 'name': '记录时间'},
    #         {'key': 'recordRes', 'name': '任务结果'},
    #         {'key': 'recordRemark', 'name': '任务描述'}
    #     ]

    #     # 转换 body 部分
    #     body = []
    #     for item in data:
    #         record = item['record']

    #         recordItem_type = find_recordType(int(record[2]))
    #         recordItem_res = find_recordRes(int(record[4]))
    #         recordItem_operation = find_recordOperation(int(record[4]))


    #         lines = record[5].splitlines()
    #         recordItem_remark = lines[-1] if lines else record[5]

    #         body.append({
    #             # 'recordId': record[0],
    #             # 'recordUser': record[1],
    #             'recordType': recordItem_type,
    #             'recordTime': record[3],
    #             'recordRes': recordItem_res,
    #             'recordRemark': recordItem_remark,
    #             "operation": recordItem_operation
    #             # 'other': record[6]  # 如果需要，也可以添加其他信息
    #         })


    #     formatted_data = {
    #         'head': head,
    #         'body': body
    #     }

    #     print(formatted_data)

    #     return jsonify(formatted_data)  # 将数据序列化为 JSON 并返回


@app.route("/api/getHistoryCount", methods=["GET"])
def getHistoryCount():
    # 从查询字符串中获取参数
    userId = request.args.get('userId')
    recordTime = request.args.get('time')
    recordType = request.args.get('type')

    print(recordTime, recordType)

    userType = 0

    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        
        query = "SELECT * FROM user WHERE userId=?"
        params = [userId]  # 初始化参数列表，至少包含一个参数

        cur.execute(query, params)  # 执行查询
        user = cur.fetchone()  # 获取查询结果的第一行
        
        if user:
            # 如果查询到了用户，userType字段是第二列（索引为1）
            if user[1] == 0:
                userType = 0
            elif user[1] == 1:
                userType = 1
        else:
            print("未找到用户")


    # 连接到数据库
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()

        query = "SELECT COUNT(*) FROM record"
        params = []  # 初始化参数列表，至少包含一个参数

        
        if userType == 0:
            if len(params) == 0:
                query += " WHERE recordUser=?"
            else:
                query += " AND recordUser=?"
            params.append(userId)
        

        if recordTime is not None:
            # 将字符串转换为datetime对象
            utc_dt = datetime.strptime(recordTime, "%Y-%m-%dT%H:%M:%S.%fZ")

            # 将UTC时间转换为UTC时区的datetime对象
            utc_dt = pytz.utc.localize(utc_dt)

            # 定义东八区时区
            china_timezone = pytz.timezone('Asia/Shanghai')

            # 将UTC时间转换为东八区时间
            china_dt = utc_dt.astimezone(china_timezone)

            # 格式化为数据库中DATETIME类型的日期部分
            formatted_date = china_dt.strftime("%Y-%m-%d")

            print(formatted_date)

            # # 添加对当天记录的查询条件
            # query += " AND DATE(recordTime)>=?"
            # params.append(formatted_date + " 00:00:00")  # 添加 recordTime 开始日期参数

            # # 添加对当天记录的查询条件
            # query += " AND DATE(recordTime)<=?"
            # params.append(formatted_date + " 23:59:59")  # 添加 recordTime 结束日期参数

            if len(params) == 0:
                query += " WHERE DATE(recordTime)=?"
            else:
                query += " AND DATE(recordTime)=?"
            params.append(formatted_date)  # 添加 recordTime 参数

            # query += " AND recordTime=?"
            # params.append(recordTime)  # 添加 recordTime 参数

        if recordType is not None:
            if len(params) == 0:
                query += " WHERE recordType=?"
            else:
                query += " AND recordType=?"
            params.append(recordType)  # 添加 recordType 参数

        query += " ORDER BY recordTime DESC"


        cur.execute(query, tuple(params))  # 使用 tuple 确保参数是正确的类型

        total_records = cur.fetchone()[0]


        print("total_records + ")
        print(total_records)

        return jsonify({'count': total_records})

    # # 连接到数据库
    # with sqlite3.connect("database.db") as con:
    #     cur = con.cursor()

    #     query = "SELECT COUNT(*) FROM record WHERE recordUser=?"
    #     params = [userId]  # 初始化参数列表，至少包含一个参数

    #     if recordTime is not None:
    #         # 将字符串转换为datetime对象
    #         utc_dt = datetime.strptime(recordTime, "%Y-%m-%dT%H:%M:%S.%fZ")

    #         # 将UTC时间转换为UTC时区的datetime对象
    #         utc_dt = pytz.utc.localize(utc_dt)

    #         # 定义东八区时区
    #         china_timezone = pytz.timezone('Asia/Shanghai')

    #         # 将UTC时间转换为东八区时间
    #         china_dt = utc_dt.astimezone(china_timezone)

    #         # 格式化为数据库中DATETIME类型的日期部分
    #         formatted_date = china_dt.strftime("%Y-%m-%d")

    #         print(formatted_date)

    #         # # 添加对当天记录的查询条件
    #         # query += " AND DATE(recordTime)>=?"
    #         # params.append(formatted_date + " 00:00:00")  # 添加 recordTime 开始日期参数

    #         # # 添加对当天记录的查询条件
    #         # query += " AND DATE(recordTime)<=?"
    #         # params.append(formatted_date + " 23:59:59")  # 添加 recordTime 结束日期参数

    #         query += " AND DATE(recordTime)=?"
    #         params.append(formatted_date)  # 添加 recordTime 参数
    #         # query += " AND recordTime=?"
    #         # params.append(recordTime)  # 添加 recordTime 参数

    #     if recordType is not None:
    #         query += " AND recordType=?"
    #         params.append(recordType)  # 添加 recordType 参数

    #     query += " ORDER BY recordTime DESC"


    #     cur.execute(query, tuple(params))  # 使用 tuple 确保参数是正确的类型

    #     total_records = cur.fetchone()[0]

    #     print(total_records)

    #     return jsonify({'count': total_records})
    

# 定义路由和视图函数
@app.route('/api/embedJPG', methods=['POST'])
def embedJPG():
    if request.method == "POST":
        fileNameJPG = request.json.get('fileNameJPG')
        fileNameTXT = request.json.get('fileNameTXT')
        userId = request.json.get('userId')
        method = request.json.get('method')
        method_int = int(method)

        # 使用示例
        virtualenv_path = '/root/anaconda3/envs/jpgstego'


        script_path = ""

        # 使用转换后的整数进行条件判断
        if method_int == 0:
            script_path = os.path.join(os.getcwd(), "stego", "img_stego", "long_embed_test.py")
        elif method_int == 1:
            # 如果不是0，执行其他操作
            script_path = os.path.join(os.getcwd(), "stego", "img_stego", "long_embed_gpu.py")




        coverJPG_path = os.path.join(os.getcwd(), "uploads", "jpg", fileNameJPG)  # 第一个参数
        inputTXT_path = os.path.join(os.getcwd(), "uploads", "txt", fileNameTXT)  # 第二个参数
        stegoJPG_path = os.path.join(os.getcwd(), "output", "jpg", fileNameJPG)  # 第一个参数

        print(coverJPG_path)
        print(inputTXT_path)
        print(stegoJPG_path)

        output, error = run_script_in_virtualenv(script_path, virtualenv_path, coverJPG_path, inputTXT_path, stegoJPG_path)


        print(output)
        print(error)


        # 获取当前本地时间
        local_time = datetime.now()

        # 增加8小时
        adjusted_time = local_time + timedelta(hours=8)

        # 格式化为字符串，符合SQLite的DATETIME格式
        adjusted_time_str = adjusted_time.strftime('%Y-%m-%d %H:%M:%S')



        if os.path.isfile(stegoJPG_path):
            print(f"文件 {stegoJPG_path} 存在。")

            
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                
                cur.execute("INSERT INTO record (recordUser, recordType, recordRes, recordRemark, recordTime) VALUES (?, ?, ?, ?, ?)", (userId, 1, 1, stegoJPG_path, adjusted_time_str))
                con.commit()
            
            con.close()

            return send_file(stegoJPG_path, as_attachment=True, download_name='stegoIMG.jpg')

        else:
            print(f"文件 {stegoJPG_path} 不存在。")


            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                
                cur.execute("INSERT INTO record (recordUser, recordType, recordRes, recordRemark, recordTime) VALUES (?, ?, ?, ?, ?)", (userId, 1, 0, error, adjusted_time_str))
                con.commit()
            
            con.close()

            # 使用 splitlines() 分割字符串为行列表
            lines = error.splitlines()

            # 获取最后一行
            last_line = lines[-1]

            return jsonify({'message': '信息提取失败，请确认上传文件\n' + last_line, 'msg': error}), 200


# 定义路由和视图函数
@app.route('/api/extractJPG', methods=['POST'])
def extractJPG():
    if request.method == "POST":
        fileNameJPG = request.json.get('fileNameJPG')
        userId = request.json.get('userId')
        method = request.json.get('method')
        method_int = int(method)

        # 使用示例
        virtualenv_path = '/root/anaconda3/envs/jpgstego'

        script_path = ""

        # 使用转换后的整数进行条件判断
        if method_int == 0:
            script_path = os.path.join(os.getcwd(), "stego", "img_stego", "long_extract_test.py")
        elif method_int == 1:
            # 如果不是0，执行其他操作
            script_path = os.path.join(os.getcwd(), "stego", "img_stego", "long_extract_gpu.py")


        stegoJPG_path = os.path.join(os.getcwd(), "uploads", "jpg", fileNameJPG)  # 第一个参数
        output_path = os.path.join(os.getcwd(), "output", "txt", fileNameJPG)  # 第一个参数

        # 分割路径和扩展名
        base, ext = os.path.splitext(output_path)

        # 替换扩展名为.txt
        outputTXT_path = base + '.txt'


        print(stegoJPG_path)
        print(outputTXT_path)

        output, error = run_script_in_virtualenv(script_path, virtualenv_path, stegoJPG_path, outputTXT_path)

        print(output)
        print(error)

        # 获取当前本地时间
        local_time = datetime.now()

        # 增加8小时
        adjusted_time = local_time + timedelta(hours=8)

        # 格式化为字符串，符合SQLite的DATETIME格式
        adjusted_time_str = adjusted_time.strftime('%Y-%m-%d %H:%M:%S')



        if os.path.isfile(outputTXT_path):
            print(f"文件 {outputTXT_path} 存在。")

            
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                
                cur.execute("INSERT INTO record (recordUser, recordType, recordRes, recordRemark, recordTime) VALUES (?, ?, ?, ?, ?)", (userId, 2, 1, outputTXT_path, adjusted_time_str))
                con.commit()
            
            con.close()

            return send_file(outputTXT_path, as_attachment=True, download_name='output.txt')


        else:
            print(f"文件 {outputTXT_path} 不存在。")

            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                
                cur.execute("INSERT INTO record (recordUser, recordType, recordRes, recordRemark, recordTime) VALUES (?, ?, ?, ?, ?)", (userId, 2, 0, error, adjusted_time_str))
                con.commit()
            
            con.close()

            # 使用 splitlines() 分割字符串为行列表
            lines = error.splitlines()

            # 获取最后一行
            last_line = lines[-1]

            return jsonify({'message': '信息提取失败，请确认上传文件\n' + last_line, 'msg': error}), 200



# 定义路由和视图函数
@app.route('/api/embedTXT', methods=['POST'])
def embedTXT():
    if request.method == "POST":
        fileNameTXT = request.json.get('fileNameTXT')
        fileNameTXT2 = request.json.get('fileNameTXT2')
        userId = request.json.get('userId')

        # 使用示例
        virtualenv_path = '/root/anaconda3/envs/projectZR'

        script_path = os.path.join(os.getcwd(), "stego", "StegaText", "embed.py")


        coverTXT_path = os.path.join(os.getcwd(), "uploads", "txt", fileNameTXT)  # 第一个参数
        inputTXT_path = os.path.join(os.getcwd(), "uploads", "txt", fileNameTXT2)  # 第二个参数
        stegoTXT_path = os.path.join(os.getcwd(), "output", "txt", fileNameTXT)  # 第一个参数

        print(coverTXT_path)
        print(inputTXT_path)
        print(stegoTXT_path)

        output, error = run_script_in_virtualenv(script_path, virtualenv_path, coverTXT_path, inputTXT_path, stegoTXT_path)


        print(output)
        print(error)

        # 获取当前本地时间
        local_time = datetime.now()

        # 增加8小时
        adjusted_time = local_time + timedelta(hours=8)

        # 格式化为字符串，符合SQLite的DATETIME格式
        adjusted_time_str = adjusted_time.strftime('%Y-%m-%d %H:%M:%S')

        if os.path.isfile(stegoTXT_path):
            print(f"文件 {stegoTXT_path} 存在。")

            
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                
                cur.execute("INSERT INTO record (recordUser, recordType, recordRes, recordRemark, recordTime) VALUES (?, ?, ?, ?, ?)", (userId, 3, 1, stegoTXT_path, adjusted_time_str))
                con.commit()
            
            con.close()

            return send_file(stegoTXT_path, as_attachment=True, download_name='stegoTXT.txt')

        else:
            print(f"文件 {stegoTXT_path} 不存在。")


            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                
                cur.execute("INSERT INTO record (recordUser, recordType, recordRes, recordRemark, recordTime) VALUES (?, ?, ?, ?, ?)", (userId, 3, 0, error, adjusted_time_str))
                con.commit()
            
            con.close()

            # 使用 splitlines() 分割字符串为行列表
            lines = error.splitlines()

            # 获取最后一行
            last_line = lines[-1]

            return jsonify({'message': '信息提取失败，请确认上传文件\n' + last_line, 'msg': error}), 200


# 定义路由和视图函数
@app.route('/api/extractTXT', methods=['POST'])
def extractTXT():
    if request.method == "POST":
        fileNameTXT = request.json.get('fileNameTXT')
        fileNameTXT2 = request.json.get('fileNameTXT2')
        userId = request.json.get('userId')

        # 使用示例
        virtualenv_path = '/root/anaconda3/envs/projectZR'

        script_path = os.path.join(os.getcwd(), "stego", "StegaText", "extract.py")

        originTXT_path = os.path.join(os.getcwd(), "uploads", "txt", fileNameTXT)  # 第一个参数
        stegoTXT_path = os.path.join(os.getcwd(), "uploads", "txt", fileNameTXT2)  # 第一个参数
        output_path = os.path.join(os.getcwd(), "output", "txt", fileNameTXT)  # 第一个参数


        print(originTXT_path)
        print(stegoTXT_path)

        output, error = run_script_in_virtualenv(script_path, virtualenv_path, originTXT_path, stegoTXT_path, output_path)

        print(output)
        print(error)

        # 获取当前本地时间
        local_time = datetime.now()

        # 增加8小时
        adjusted_time = local_time + timedelta(hours=8)

        # 格式化为字符串，符合SQLite的DATETIME格式
        adjusted_time_str = adjusted_time.strftime('%Y-%m-%d %H:%M:%S')

        if os.path.isfile(output_path):
            print(f"文件 {output_path} 存在。")

            
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                
                cur.execute("INSERT INTO record (recordUser, recordType, recordRes, recordRemark, recordTime) VALUES (?, ?, ?, ?, ?)", (userId, 4, 1, output_path, adjusted_time_str))
                con.commit()
            
            con.close()

            return send_file(output_path, as_attachment=True, download_name='output.txt')


        else:
            print(f"文件 {output_path} 不存在。")

            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                
                cur.execute("INSERT INTO record (recordUser, recordType, recordRes, recordRemark, recordTime) VALUES (?, ?, ?, ?, ?)", (userId, 4, 0, error, adjusted_time_str))
                con.commit()
            
            con.close()

            # 使用 splitlines() 分割字符串为行列表
            lines = error.splitlines()

            # 获取最后一行
            last_line = lines[-1]

            return jsonify({'message': '信息提取失败，请确认上传文件\n' + last_line, 'msg': error}), 200



# 定义路由和视图函数
@app.route('/api/embedWAVDL', methods=['POST'])
def embedWAVDL():
    if request.method == "POST":
        fileNameWAV = request.json.get('fileNameWAV')
        fileNameTXT = request.json.get('fileNameTXT')
        userId = request.json.get('userId')

        # 使用示例
        virtualenv_path = '/root/anaconda3/envs/blind'


        script_path = os.path.join(os.getcwd(), "stego", "wav_deeplearning", "src", "embed.py")


        coverWAV_path = os.path.join(os.getcwd(), "uploads", "wav", fileNameWAV)  # 第一个参数
        inputTXT_path = os.path.join(os.getcwd(), "uploads", "txt", fileNameTXT)  # 第二个参数
        stegoWAV_path = os.path.join(os.getcwd(), "output", "wav", fileNameWAV)  # 第一个参数

        print(coverWAV_path)
        print(inputTXT_path)
        print(stegoWAV_path)

        output, error = run_script_in_virtualenv(script_path, virtualenv_path, coverWAV_path, inputTXT_path, stegoWAV_path)


        print(output)
        print(error)

        # 获取当前本地时间
        local_time = datetime.now()

        # 增加8小时
        adjusted_time = local_time + timedelta(hours=8)

        # 格式化为字符串，符合SQLite的DATETIME格式
        adjusted_time_str = adjusted_time.strftime('%Y-%m-%d %H:%M:%S')

        if os.path.isfile(stegoWAV_path):
            print(f"文件 {stegoWAV_path} 存在。")

            
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                
                cur.execute("INSERT INTO record (recordUser, recordType, recordRes, recordRemark, recordTime) VALUES (?, ?, ?, ?, ?)", (userId, 5, 1, stegoWAV_path, adjusted_time_str))
                con.commit()
            
            con.close()

            return send_file(stegoWAV_path, as_attachment=True, download_name='stegoWAV.wav')

        else:
            print(f"文件 {stegoWAV_path} 不存在。")


            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                
                cur.execute("INSERT INTO record (recordUser, recordType, recordRes, recordRemark, recordTime) VALUES (?, ?, ?, ?, ?)", (userId, 5, 0, error, adjusted_time_str))
                con.commit()
            
            con.close()

            last_line = ""

            if '\n' in error:
                lines = error.splitlines()
                last_line = lines[-1] if lines else error
            else:
                last_line = output

            return jsonify({'message': '信息提取失败，请确认上传文件\n' + last_line, 'msg': error}), 200


# 定义路由和视图函数
@app.route('/api/extractWAVDL', methods=['POST'])
def extractWAVDL():
    if request.method == "POST":
        fileNameWAV = request.json.get('fileNameWAV')
        userId = request.json.get('userId')

        # 使用示例
        virtualenv_path = '/root/anaconda3/envs/blind'

        script_path = os.path.join(os.getcwd(), "stego", "wav_deeplearning", "src", "extract.py")


        stegoWAV_path = os.path.join(os.getcwd(), "uploads", "wav", fileNameWAV)  # 第一个参数
        output_path = os.path.join(os.getcwd(), "output", "txt", fileNameWAV)  # 第一个参数

        # 分割路径和扩展名
        base, ext = os.path.splitext(output_path)

        # 替换扩展名为.txt
        outputTXT_path = base + '.txt'


        print(stegoWAV_path)
        print(outputTXT_path)

        output, error = run_script_in_virtualenv(script_path, virtualenv_path, stegoWAV_path, base)

        print(output)
        print(error)

        # 获取当前本地时间
        local_time = datetime.now()

        # 增加8小时
        adjusted_time = local_time + timedelta(hours=8)

        # 格式化为字符串，符合SQLite的DATETIME格式
        adjusted_time_str = adjusted_time.strftime('%Y-%m-%d %H:%M:%S')


        if os.path.isfile(outputTXT_path):
            print(f"文件 {outputTXT_path} 存在。")

            
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                
                cur.execute("INSERT INTO record (recordUser, recordType, recordRes, recordRemark, recordTime) VALUES (?, ?, ?, ?, ?)", (userId, 6, 1, outputTXT_path, adjusted_time_str))
                con.commit()
            
            con.close()

            return send_file(outputTXT_path, as_attachment=True, download_name='output.txt')


        else:
            print(f"文件 {outputTXT_path} 不存在。")

            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                
                cur.execute("INSERT INTO record (recordUser, recordType, recordRes, recordRemark, recordTime) VALUES (?, ?, ?, ?, ?)", (userId, 6, 0, error, adjusted_time_str))
                con.commit()
            
            con.close()

            last_line = ""

            if '\n' in error:
                lines = error.splitlines()
                last_line = lines[-1] if lines else error
            else:
                last_line = output

            return jsonify({'message': '信息提取失败，请确认上传文件\n' + last_line, 'msg': error}), 200



# 定义路由和视图函数
@app.route('/api/embedAVIDL', methods=['POST'])
def embedAVIDL():
    if request.method == "POST":
        fileNameAVI = request.json.get('fileNameAVI')
        fileNameTXT = request.json.get('fileNameTXT')
        userId = request.json.get('userId')
        method = request.json.get('method')
        method_int = int(method)

        print(method)

        # 使用示例
        virtualenv_path = '/root/anaconda3'

        script_path = ''

        # 使用转换后的整数进行条件判断
        if method_int == 0:
            script_path = os.path.join(os.getcwd(), "stego", "RivaGAN-neurips", "test_embed.py")
        elif method_int == 1:
            # 如果不是0，执行其他操作
            script_path = os.path.join(os.getcwd(), "stego", "RivaGAN-neurips", "test_embed_gpu.py")


        coverAVI_path = os.path.join(os.getcwd(), "uploads", "avi", fileNameAVI)  # 第一个参数
        inputTXT_path = os.path.join(os.getcwd(), "uploads", "txt", fileNameTXT)  # 第二个参数
        stegoAVI_path = os.path.join(os.getcwd(), "output", "avi", fileNameAVI)  # 第一个参数

        print(coverAVI_path)
        print(inputTXT_path)
        print(stegoAVI_path)

        output, error = run_script_in_virtualenv(script_path, virtualenv_path, coverAVI_path, inputTXT_path, stegoAVI_path)


        print(output)
        print(error)

        # 获取当前本地时间
        local_time = datetime.now()

        # 增加8小时
        adjusted_time = local_time + timedelta(hours=8)

        # 格式化为字符串，符合SQLite的DATETIME格式
        adjusted_time_str = adjusted_time.strftime('%Y-%m-%d %H:%M:%S')

        if os.path.isfile(stegoAVI_path):
            print(f"文件 {stegoAVI_path} 存在。")

            
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                
                cur.execute("INSERT INTO record (recordUser, recordType, recordRes, recordRemark, recordTime) VALUES (?, ?, ?, ?, ?)", (userId, 7, 1, stegoAVI_path, adjusted_time_str))
                con.commit()
            
            con.close()

            return send_file(stegoAVI_path, as_attachment=True, download_name='stegoAVI.avi')

        else:
            print(f"文件 {stegoAVI_path} 不存在。")


            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                
                cur.execute("INSERT INTO record (recordUser, recordType, recordRes, recordRemark, recordTime) VALUES (?, ?, ?, ?, ?)", (userId, 7, 0, error, adjusted_time_str))
                con.commit()
            
            con.close()

            last_line = ""

            if '\n' in error:
                lines = error.splitlines()
                last_line = lines[-1] if lines else error
            else:
                last_line = output

            return jsonify({'message': '信息提取失败，请确认上传文件\n' + last_line, 'msg': error}), 200



# 定义路由和视图函数
@app.route('/api/extractAVIDL', methods=['POST'])
def extractAVIDL():
    if request.method == "POST":
        fileNameAVI = request.json.get('fileNameAVI')
        userId = request.json.get('userId')
        method = request.json.get('method')
        method_int = int(method)

        # 使用示例
        virtualenv_path = '/root/anaconda3'

        script_path = ''

        # 使用转换后的整数进行条件判断
        if method_int == 0:
            script_path = os.path.join(os.getcwd(), "stego", "RivaGAN-neurips", "test_extract.py")
        elif method_int == 1:
            # 如果不是0，执行其他操作
            script_path = os.path.join(os.getcwd(), "stego", "RivaGAN-neurips", "test_extract_gpu.py")


        stegoAVI_path = os.path.join(os.getcwd(), "uploads", "avi", fileNameAVI)  # 第一个参数
        output_path = os.path.join(os.getcwd(), "output", "txt", fileNameAVI)  # 第一个参数

        # 分割路径和扩展名
        base, ext = os.path.splitext(output_path)

        # 替换扩展名为.txt
        outputTXT_path = base + '.txt'



        print(stegoAVI_path)
        print(outputTXT_path)

        output, error = run_script_in_virtualenv(script_path, virtualenv_path, stegoAVI_path, outputTXT_path)

        print(output)
        print(error)

        # 获取当前本地时间
        local_time = datetime.now()

        # 增加8小时
        adjusted_time = local_time + timedelta(hours=8)

        # 格式化为字符串，符合SQLite的DATETIME格式
        adjusted_time_str = adjusted_time.strftime('%Y-%m-%d %H:%M:%S')


        if os.path.isfile(outputTXT_path):
            print(f"文件 {outputTXT_path} 存在。")

            
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                
                cur.execute("INSERT INTO record (recordUser, recordType, recordRes, recordRemark, recordTime) VALUES (?, ?, ?, ?, ?)", (userId, 8, 1, outputTXT_path, adjusted_time_str))
                con.commit()
            
            con.close()

            return send_file(outputTXT_path, as_attachment=True, download_name='output.txt')


        else:
            print(f"文件 {outputTXT_path} 不存在。")

            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                
                cur.execute("INSERT INTO record (recordUser, recordType, recordRes, recordRemark, recordTime) VALUES (?, ?, ?, ?, ?)", (userId, 8, 0, error, adjusted_time_str))
                con.commit()
            
            con.close()

            last_line = ""

            if '\n' in error:
                lines = error.splitlines()
                last_line = lines[-1] if lines else error
            else:
                last_line = output

            return jsonify({'message': '信息提取失败，请确认上传文件\n' + last_line, 'msg': error}), 200


# 定义路由和视图函数
@app.route('/api/embedWAV', methods=['POST'])
def embedWAV():
    if request.method == "POST":
        fileNameWAV = request.json.get('fileNameWAV')
        fileNameTXT = request.json.get('fileNameTXT')
        userId = request.json.get('userId')

        # 使用示例
        virtualenv_path = '/root/anaconda3/envs/blind'


        script_path = os.path.join(os.getcwd(), "stego", "wav_linux", "embed.py")


        coverWAV_path = os.path.join(os.getcwd(), "uploads", "wav", fileNameWAV)  # 第一个参数
        inputTXT_path = os.path.join(os.getcwd(), "uploads", "txt", fileNameTXT)  # 第二个参数
        stegoWAV_path = os.path.join(os.getcwd(), "output", "wav", fileNameWAV)  # 第一个参数

        print(coverWAV_path)
        print(inputTXT_path)
        print(stegoWAV_path)

        output, error = run_script_in_virtualenv(script_path, virtualenv_path, coverWAV_path, inputTXT_path, stegoWAV_path)


        print(output)
        print(error)

        # 获取当前本地时间
        local_time = datetime.now()

        # 增加8小时
        adjusted_time = local_time + timedelta(hours=8)

        # 格式化为字符串，符合SQLite的DATETIME格式
        adjusted_time_str = adjusted_time.strftime('%Y-%m-%d %H:%M:%S')

        if os.path.isfile(stegoWAV_path):
            print(f"文件 {stegoWAV_path} 存在。")

            
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                
                cur.execute("INSERT INTO record (recordUser, recordType, recordRes, recordRemark, recordTime) VALUES (?, ?, ?, ?, ?)", (userId, 9, 1, stegoWAV_path, adjusted_time_str))
                con.commit()
            
            con.close()

            return send_file(stegoWAV_path, as_attachment=True, download_name='stegoWAV.wav')

        else:
            print(f"文件 {stegoWAV_path} 不存在。")


            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                
                cur.execute("INSERT INTO record (recordUser, recordType, recordRes, recordRemark, recordTime) VALUES (?, ?, ?, ?, ?)", (userId, 9, 0, error, adjusted_time_str))
                con.commit()
            
            con.close()

            last_line = ""

            if '\n' in error:
                lines = error.splitlines()
                last_line = lines[-1] if lines else error
            else:
                last_line = output

            return jsonify({'message': '信息提取失败，请确认上传文件\n' + last_line, 'msg': error}), 200


# 定义路由和视图函数
@app.route('/api/extractWAV', methods=['POST'])
def extractWAV():
    if request.method == "POST":
        fileNameWAV = request.json.get('fileNameWAV')
        userId = request.json.get('userId')

        # 使用示例
        virtualenv_path = '/root/anaconda3/envs/blind'

        script_path = os.path.join(os.getcwd(), "stego", "wav_linux", "extract.py")


        stegoWAV_path = os.path.join(os.getcwd(), "uploads", "wav", fileNameWAV)  # 第一个参数
        output_path = os.path.join(os.getcwd(), "output", "wav_so", fileNameWAV)  # 第一个参数

        # 分割路径和扩展名
        base, ext = os.path.splitext(output_path)

        # 替换扩展名为.txt
        outputTXT_path = base + '.txt'


        print(stegoWAV_path)
        print(outputTXT_path)

        output, error = run_script_in_virtualenv(script_path, virtualenv_path, stegoWAV_path, base)

        print(output)
        print(error)

        # 获取当前本地时间
        local_time = datetime.now()

        # 增加8小时
        adjusted_time = local_time + timedelta(hours=8)

        # 格式化为字符串，符合SQLite的DATETIME格式
        adjusted_time_str = adjusted_time.strftime('%Y-%m-%d %H:%M:%S')



        fm_base, fm_ext = os.path.splitext(fileNameWAV)

        # 使用示例
        directory = os.path.join(os.getcwd(), "output", "wav_so")  # 替换为你的目录路径
        filename_without_extension = fm_base  # 替换为你的文件名（不含后缀）
        full_path = find_file_with_extension(directory, filename_without_extension)


        print(full_path)

        if full_path:
            print(f"文件 {full_path} 存在。")

            
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                
                cur.execute("INSERT INTO record (recordUser, recordType, recordRes, recordRemark, recordTime) VALUES (?, ?, ?, ?, ?)", (userId, 10, 1, full_path, adjusted_time_str))
                con.commit()
            
            con.close()


            return send_file(full_path, as_attachment=True, download_name='output.txt')


        else:
            print(f"文件 {full_path} 不存在。")

            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                
                cur.execute("INSERT INTO record (recordUser, recordType, recordRes, recordRemark, recordTime) VALUES (?, ?, ?, ?, ?)", (userId, 10, 0, error, adjusted_time_str))
                con.commit()
            
            con.close()

            last_line = ""

            if '\n' in error:
                lines = error.splitlines()
                last_line = lines[-1] if lines else error
            else:
                last_line = output

            return jsonify({'message': '信息提取失败，请确认上传文件\n' + last_line, 'msg': error}), 200


# 定义路由和视图函数
@app.route('/api/embedWMA', methods=['POST'])
def embedWMA():
    if request.method == "POST":
        fileNameWMA = request.json.get('fileNameWMA')
        fileNameTXT = request.json.get('fileNameTXT')
        userId = request.json.get('userId')

        # 使用示例
        virtualenv_path = '/root/anaconda3/envs/blind'


        script_path = os.path.join(os.getcwd(), "stego", "wma", "embed.py")


        coverWMA_path = os.path.join(os.getcwd(), "uploads", "wma", fileNameWMA)  # 第一个参数
        inputTXT_path = os.path.join(os.getcwd(), "uploads", "txt", fileNameTXT)  # 第二个参数
        stegoWMA_path = os.path.join(os.getcwd(), "output", "wma", fileNameWMA)  # 第一个参数

        print(coverWMA_path)
        print(inputTXT_path)
        print(stegoWMA_path)

        


        output, error = run_script_in_virtualenv(script_path, virtualenv_path, coverWMA_path, inputTXT_path, stegoWMA_path)


        print(output)
        print(error)

        fm_base, fm_ext = os.path.splitext(stegoWMA_path)

        stegoWAV_path = fm_base + '.wav'

        # 获取当前本地时间
        local_time = datetime.now()

        # 增加8小时
        adjusted_time = local_time + timedelta(hours=8)

        # 格式化为字符串，符合SQLite的DATETIME格式
        adjusted_time_str = adjusted_time.strftime('%Y-%m-%d %H:%M:%S')

        if os.path.isfile(stegoWMA_path):
            print(f"文件 {stegoWMA_path} 存在。")


            
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                
                cur.execute("INSERT INTO record (recordUser, recordType, recordRes, recordRemark, recordTime) VALUES (?, ?, ?, ?, ?)", (userId, 11, 1, stegoWAV_path, adjusted_time_str))
                con.commit()
            
            con.close()

            # 创建一个 ZIP 文件
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w') as z:
                z.write(stegoWMA_path, 'stegoWMA.wma')
                z.write(stegoWAV_path, 'stegoWAV.wav')
            zip_buffer.seek(0)

            # return send_file(stegoWAV_path, as_attachment=True, download_name='stegoWAV.wav')
            return send_file(zip_buffer, as_attachment=True, download_name='stegoWMA.zip', mimetype='application/zip')

        else:
            print(f"文件 {stegoWAV_path} 不存在。")


            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                
                cur.execute("INSERT INTO record (recordUser, recordType, recordRes, recordRemark, recordTime) VALUES (?, ?, ?, ?, ?)", (userId, 11, 0, error, adjusted_time_str))
                con.commit()
            
            con.close()

            last_line = ""

            if '\n' in error:
                lines = error.splitlines()
                last_line = lines[-1] if lines else error
            else:
                last_line = output

            return jsonify({'message': '信息提取失败，请确认上传文件\n' + last_line, 'msg': error}), 200


# 定义路由和视图函数
@app.route('/api/extractWMA', methods=['POST'])
def extractWMA():
    if request.method == "POST":
        fileNameWAV = request.json.get('fileNameWAV')
        userId = request.json.get('userId')

        # 使用示例
        virtualenv_path = '/root/anaconda3/envs/blind'

        script_path = os.path.join(os.getcwd(), "stego", "wma", "extract.py")


        stegoWAV_path = os.path.join(os.getcwd(), "uploads", "wav", fileNameWAV)  # 第一个参数
        output_path = os.path.join(os.getcwd(), "output", "txt", fileNameWAV)  # 第一个参数

        # 分割路径和扩展名
        base, ext = os.path.splitext(output_path)

        # 替换扩展名为.txt
        outputTXT_path = base + '.txt'


        print(stegoWAV_path)
        print(outputTXT_path)

        output, error = run_script_in_virtualenv(script_path, virtualenv_path, stegoWAV_path, outputTXT_path)

        print(output)
        print(error)

        # 获取当前本地时间
        local_time = datetime.now()

        # 增加8小时
        adjusted_time = local_time + timedelta(hours=8)

        # 格式化为字符串，符合SQLite的DATETIME格式
        adjusted_time_str = adjusted_time.strftime('%Y-%m-%d %H:%M:%S')


        if os.path.isfile(outputTXT_path):
            print(f"文件 {outputTXT_path} 存在。")

            
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                
                cur.execute("INSERT INTO record (recordUser, recordType, recordRes, recordRemark, recordTime) VALUES (?, ?, ?, ?, ?)", (userId, 12, 1, outputTXT_path, adjusted_time_str))
                con.commit()
            
            con.close()


            return send_file(outputTXT_path, as_attachment=True, download_name='output.txt')


        else:
            print(f"文件 {outputTXT_path} 不存在。")

            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                
                cur.execute("INSERT INTO record (recordUser, recordType, recordRes, recordRemark, recordTime) VALUES (?, ?, ?, ?, ?)", (userId, 12, 0, error, adjusted_time_str))
                con.commit()
            
            con.close()

            last_line = ""

            if '\n' in error:
                lines = error.splitlines()
                last_line = lines[-1] if lines else error
            else:
                last_line = output

            return jsonify({'message': '信息提取失败，请确认上传文件\n' + last_line, 'msg': error}), 200


# 定义路由和视图函数
@app.route('/api/embedMID', methods=['POST'])
def embedMID():
    if request.method == "POST":
        fileNameMID = request.json.get('fileNameMID')
        fileNameTXT = request.json.get('fileNameTXT')
        userId = request.json.get('userId')

        # 使用示例
        virtualenv_path = '/root/anaconda3/envs/blind'


        script_path = os.path.join(os.getcwd(), "stego", "mid", "embed.py")


        coverMID_path = os.path.join(os.getcwd(), "uploads", "mid", fileNameMID)  # 第一个参数
        inputTXT_path = os.path.join(os.getcwd(), "uploads", "txt", fileNameTXT)  # 第二个参数
        stegoMID_path = os.path.join(os.getcwd(), "output", "mid", fileNameMID)  # 第一个参数

        print(coverMID_path)
        print(inputTXT_path)
        print(stegoMID_path)

        output, error = run_script_in_virtualenv(script_path, virtualenv_path, coverMID_path, inputTXT_path, stegoMID_path)


        print(output)
        print(error)

        # 获取当前本地时间
        local_time = datetime.now()

        # 增加8小时
        adjusted_time = local_time + timedelta(hours=8)

        # 格式化为字符串，符合SQLite的DATETIME格式
        adjusted_time_str = adjusted_time.strftime('%Y-%m-%d %H:%M:%S')

        if os.path.isfile(stegoMID_path):
            print(f"文件 {stegoMID_path} 存在。")

            
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                
                cur.execute("INSERT INTO record (recordUser, recordType, recordRes, recordRemark, recordTime) VALUES (?, ?, ?, ?, ?)", (userId, 13, 1, stegoMID_path, adjusted_time_str))
                con.commit()
            
            con.close()

            return send_file(stegoMID_path, as_attachment=True, download_name='stegoMID.mid')

        else:
            print(f"文件 {stegoMID_path} 不存在。")


            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                
                cur.execute("INSERT INTO record (recordUser, recordType, recordRes, recordRemark, recordTime) VALUES (?, ?, ?, ?, ?)", (userId, 13, 0, error, adjusted_time_str))
                con.commit()
            
            con.close()

            last_line = ""

            if '\n' in error:
                lines = error.splitlines()
                last_line = lines[-1] if lines else error
            else:
                last_line = output

            return jsonify({'message': '信息提取失败，请确认上传文件\n' + last_line, 'msg': error}), 200


# 定义路由和视图函数
@app.route('/api/extractMID', methods=['POST'])
def extractMID():
    if request.method == "POST":
        fileNameMID = request.json.get('fileNameMID')
        userId = request.json.get('userId')

        # 使用示例
        virtualenv_path = '/root/anaconda3/envs/blind'

        script_path = os.path.join(os.getcwd(), "stego", "mid", "extract.py")


        stegoWAV_path = os.path.join(os.getcwd(), "uploads", "mid", fileNameMID)  # 第一个参数
        output_path = os.path.join(os.getcwd(), "output", "txt", fileNameMID)  # 第一个参数

        # 分割路径和扩展名
        base, ext = os.path.splitext(output_path)

        # 替换扩展名为.txt
        outputTXT_path = base + '.txt'


        print(stegoWAV_path)
        print(outputTXT_path)


        output, error = run_script_in_virtualenv(script_path, virtualenv_path, stegoWAV_path, outputTXT_path)

        print(output)
        print(error)

        # 获取当前本地时间
        local_time = datetime.now()

        # 增加8小时
        adjusted_time = local_time + timedelta(hours=8)

        # 格式化为字符串，符合SQLite的DATETIME格式
        adjusted_time_str = adjusted_time.strftime('%Y-%m-%d %H:%M:%S')

        if os.path.isfile(outputTXT_path):
            print(f"文件 {outputTXT_path} 存在。")

            
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                
                cur.execute("INSERT INTO record (recordUser, recordType, recordRes, recordRemark, recordTime) VALUES (?, ?, ?, ?, ?)", (userId, 14, 1, outputTXT_path, adjusted_time_str))
                con.commit()
            
            con.close()


            return send_file(outputTXT_path, as_attachment=True, download_name='output.txt')


        else:
            print(f"文件 {outputTXT_path} 不存在。")

            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                
                cur.execute("INSERT INTO record (recordUser, recordType, recordRes, recordRemark, recordTime) VALUES (?, ?, ?, ?, ?)", (userId, 14, 0, error, adjusted_time_str))
                con.commit()
            
            con.close()

            last_line = ""

            if '\n' in error:
                lines = error.splitlines()
                last_line = lines[-1] if lines else error
            else:
                last_line = output

            return jsonify({'message': '信息提取失败，请确认上传文件\n' + last_line, 'msg': error}), 200

# 定义路由和视图函数
@app.route('/api/embedMP4', methods=['POST'])
def embedMP4():
    if request.method == "POST":
        fileNameMP4 = request.json.get('fileNameMP4')
        fileNameTXT = request.json.get('fileNameTXT')
        userId = request.json.get('userId')

        # 使用示例
        virtualenv_path = '/root/anaconda3/envs/blind'


        script_path = os.path.join(os.getcwd(), "stego", "mp4", "embed.py")


        coverMP4_path = os.path.join(os.getcwd(), "uploads", "mp4", fileNameMP4)  # 第一个参数
        inputTXT_path = os.path.join(os.getcwd(), "uploads", "txt", fileNameTXT)  # 第二个参数
        stegoMP4_path = os.path.join(os.getcwd(), "output", "mp4", fileNameMP4)  # 第一个参数

        print(coverMP4_path)
        print(inputTXT_path)
        print(stegoMP4_path)

        output, error = run_script_in_virtualenv(script_path, virtualenv_path, coverMP4_path, inputTXT_path, stegoMP4_path)


        print(output)
        print(error)

        # 获取当前本地时间
        local_time = datetime.now()

        # 增加8小时
        adjusted_time = local_time + timedelta(hours=8)

        # 格式化为字符串，符合SQLite的DATETIME格式
        adjusted_time_str = adjusted_time.strftime('%Y-%m-%d %H:%M:%S')

        if os.path.isfile(stegoMP4_path):
            print(f"文件 {stegoMP4_path} 存在。")

            
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                
                cur.execute("INSERT INTO record (recordUser, recordType, recordRes, recordRemark, recordTime) VALUES (?, ?, ?, ?, ?)", (userId, 15, 1, stegoMP4_path, adjusted_time_str))
                con.commit()
            
            con.close()

            return send_file(stegoMP4_path, as_attachment=True, download_name='stegoMP4.mp4')

        else:
            print(f"文件 {stegoMP4_path} 不存在。")


            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                
                cur.execute("INSERT INTO record (recordUser, recordType, recordRes, recordRemark, recordTime) VALUES (?, ?, ?, ?, ?)", (userId, 15, 0, error, adjusted_time_str))
                con.commit()
            
            con.close()

            last_line = ""

            if '\n' in error:
                lines = error.splitlines()
                last_line = lines[-1] if lines else error
            else:
                last_line = output

            return jsonify({'message': '信息提取失败，请确认上传文件\n' + last_line, 'msg': error}), 200


# 定义路由和视图函数
@app.route('/api/extractMP4', methods=['POST'])
def extractMP4():
    if request.method == "POST":
        fileNameMP4 = request.json.get('fileNameMP4')
        userId = request.json.get('userId')

        # 使用示例
        virtualenv_path = '/root/anaconda3/envs/blind'

        script_path = os.path.join(os.getcwd(), "stego", "mp4", "extract.py")


        stegoMP4_path = os.path.join(os.getcwd(), "uploads", "mp4", fileNameMP4)  # 第一个参数
        output_path = os.path.join(os.getcwd(), "output", "txt", fileNameMP4)  # 第一个参数


        # 分割路径和扩展名
        base, ext = os.path.splitext(output_path)

        # 替换扩展名为.txt
        outputTXT_path = base + '.txt'


        print(stegoMP4_path)
        print(outputTXT_path)

        output, error = run_script_in_virtualenv(script_path, virtualenv_path, stegoMP4_path, outputTXT_path)

        print(output)
        print(error)

        # 获取当前本地时间
        local_time = datetime.now()

        # 增加8小时
        adjusted_time = local_time + timedelta(hours=8)

        # 格式化为字符串，符合SQLite的DATETIME格式
        adjusted_time_str = adjusted_time.strftime('%Y-%m-%d %H:%M:%S')

        if os.path.isfile(outputTXT_path):
            print(f"文件 {outputTXT_path} 存在。")

            
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                
                cur.execute("INSERT INTO record (recordUser, recordType, recordRes, recordRemark, recordTime) VALUES (?, ?, ?, ?, ?)", (userId, 16, 1, outputTXT_path, adjusted_time_str))
                con.commit()
            
            con.close()


            return send_file(outputTXT_path, as_attachment=True, download_name='output.txt')


        else:
            print(f"文件 {outputTXT_path} 不存在。")

            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                
                cur.execute("INSERT INTO record (recordUser, recordType, recordRes, recordRemark, recordTime) VALUES (?, ?, ?, ?, ?)", (userId, 16, 0, error, adjusted_time_str))
                con.commit()
            
            con.close()

            last_line = ""

            if '\n' in error:
                lines = error.splitlines()
                last_line = lines[-1] if lines else error
            else:
                last_line = output

            return jsonify({'message': '信息提取失败，请确认上传文件\n' + last_line, 'msg': error}), 200


# 定义路由和视图函数
@app.route('/api/embedBMP', methods=['POST'])
def embedBMP():
    if request.method == "POST":
        fileNameBMP = request.json.get('fileNameBMP')
        fileNameTXT = request.json.get('fileNameTXT')
        userId = request.json.get('userId')

        # 使用示例
        virtualenv_path = '/root/anaconda3/envs/blind'


        script_path = os.path.join(os.getcwd(), "stego", "blind_watermark", "embed.py")


        coverBMP_path = os.path.join(os.getcwd(), "uploads", "bmp", fileNameBMP)  # 第一个参数
        inputTXT_path = os.path.join(os.getcwd(), "uploads", "txt", fileNameTXT)  # 第二个参数
        stegoBMP_path = os.path.join(os.getcwd(), "output", "bmp", fileNameBMP)  # 第一个参数

        print(coverBMP_path)
        print(inputTXT_path)
        print(stegoBMP_path)

        output, error = run_script_in_virtualenv(script_path, virtualenv_path, coverBMP_path, inputTXT_path, stegoBMP_path)


        print("output: " + output)
        print("error: " + error)


        # 获取当前本地时间
        local_time = datetime.now()

        # 增加8小时
        adjusted_time = local_time + timedelta(hours=8)

        # 格式化为字符串，符合SQLite的DATETIME格式
        adjusted_time_str = adjusted_time.strftime('%Y-%m-%d %H:%M:%S')

        if os.path.isfile(stegoBMP_path):
            print(f"文件 {stegoBMP_path} 存在。")

            
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                
                cur.execute("INSERT INTO record (recordUser, recordType, recordRes, recordRemark, recordTime) VALUES (?, ?, ?, ?, ?)", (userId, 17, 1, stegoBMP_path, adjusted_time_str))
                con.commit()
            
            con.close()

            lines = output.splitlines()
            last_line = lines[-1] if lines else output

            print("last_line: " + last_line)

            # 创建一个临时文件来存储 last_line 字符串
            with open('embedLen.txt', 'w') as f:
                f.write(last_line)
                f.close()


            # 创建一个 ZIP 文件
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w') as z:
                z.write(stegoBMP_path, 'stegoBMP.bmp')
                # 将 embedLen.txt 文件添加到 ZIP 中
                z.write('embedLen.txt', 'embedLen.txt')
            zip_buffer.seek(0)

            os.remove('embedLen.txt')

            # return send_file(stegoBMP_path, as_attachment=True, download_name='stegoBMP.bmp')
            return send_file(zip_buffer, as_attachment=True, download_name='stegoWMA.zip', mimetype='application/zip')

        else:
            print(f"文件 {stegoBMP_path} 不存在。")


            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                
                cur.execute("INSERT INTO record (recordUser, recordType, recordRes, recordRemark, recordTime) VALUES (?, ?, ?, ?, ?)", (userId, 17, 0, error, adjusted_time_str))
                con.commit()
            
            con.close()

            last_line = ""

            if '\n' in error:
                lines = error.splitlines()
                last_line = lines[-1] if lines else error
            else:
                last_line = output

            return jsonify({'message': '信息提取失败，请确认上传文件\n' + last_line, 'msg': error}), 200


# 定义路由和视图函数
@app.route('/api/extractBMP', methods=['POST'])
def extractBMP():
    if request.method == "POST":
        fileNameBMP = request.json.get('fileNameBMP')
        embedLen = request.json.get('embedLen')
        userId = request.json.get('userId')

        # 使用示例
        virtualenv_path = '/root/anaconda3/envs/blind'

        script_path = os.path.join(os.getcwd(), "stego", "blind_watermark", "extract.py")


        stegoBMP_path = os.path.join(os.getcwd(), "uploads", "bmp", fileNameBMP)  # 第一个参数
        output_path = os.path.join(os.getcwd(), "output", "txt", fileNameBMP)  # 第一个参数


        # 分割路径和扩展名
        base, ext = os.path.splitext(output_path)

        # 替换扩展名为.txt
        outputTXT_path = base + '.txt'


        print(stegoBMP_path)
        print(outputTXT_path)

        output, error = run_script_in_virtualenv(script_path, virtualenv_path, stegoBMP_path, embedLen, outputTXT_path)

        print("output: " + output)
        print("error: " + error)

        # 获取当前本地时间
        local_time = datetime.now()

        # 增加8小时
        adjusted_time = local_time + timedelta(hours=8)

        # 格式化为字符串，符合SQLite的DATETIME格式
        adjusted_time_str = adjusted_time.strftime('%Y-%m-%d %H:%M:%S')

        if os.path.isfile(outputTXT_path):
            print(f"文件 {outputTXT_path} 存在。")

            
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                
                cur.execute("INSERT INTO record (recordUser, recordType, recordRes, recordRemark, recordTime) VALUES (?, ?, ?, ?, ?)", (userId, 18, 1, outputTXT_path, adjusted_time_str))
                con.commit()
            
            con.close()

            return send_file(outputTXT_path, as_attachment=True, download_name='output.txt')


        else:
            print(f"文件 {outputTXT_path} 不存在。")

            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                
                cur.execute("INSERT INTO record (recordUser, recordType, recordRes, recordRemark, recordTime) VALUES (?, ?, ?, ?, ?)", (userId, 18, 0, error, adjusted_time_str))
                con.commit()
            
            con.close()

            last_line = ""

            if '\n' in error:
                lines = error.splitlines()
                last_line = lines[-1] if lines else error
            else:
                last_line = output

            return jsonify({'message': '信息提取失败，请确认上传文件\n' + last_line, 'msg': error}), 200








def run_script_in_virtualenv(script_path, virtualenv_path, *args):
    # 构建 subprocess 命令
    # 替换 '/path/to/virtualenv/bin/python' 为你的虚拟环境 Python 解释器路径
    python_executable = os.path.join(virtualenv_path, 'bin', 'python')
    command = [python_executable, script_path] + list(args)

    # 执行命令
    result = subprocess.run(command, capture_output=True, text=True)

    # 返回输出和错误信息
    return result.stdout, result.stderr








@app.route("/textStego/", methods=["POST", "GET"])
def textStego():
    if request.method == "GET":
        return render_template("text.html")

    elif request.method == "POST":
        data = request.json
        text = data.get('text')
        # text = request.form.get("text", type=str, default=None)

        result = textUtil.textJudge(text)

        data = {'result': result}
        return jsonify(data)

        # return render_template("text.html", textRes=result)
        # return redirect(url_for("index", textRes=result))

        
def is_grayscale(image_path):
    # 使用Pillow库打开图像
    with Image.open(image_path) as img:
        # 检查通道数
        return img.mode == 'L'
def convert_to_pgm(image_path):
    # 将图像转换为 PGM 格式并保存
    img = Image.open(image_path)
    pgm_path = image_path.replace(os.path.splitext(image_path)[1], '.pgm')
    img.convert('L').save(pgm_path)
    return pgm_path

@app.route('/pgmStego', methods=['POST'])
def pgmStego():
    if 'image' not in request.files:
        return jsonify({'result': '未上传文件'})
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'result': '未选择文件'})
    
    random_name = uuid.uuid4().hex + os.path.splitext(file.filename)[1]
    # filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], random_name)
    file.save(filepath)

    if is_grayscale(filepath):
        return jsonify({'result': "formatted_result"})
    else:
        error_message = '错误：只允许使用灰度图像。'
        return jsonify({'result': error_message})


    
    # # 在这里实现图像隐写分析的逻辑

    result = pgmUtil.pgmStego(filepath)

    
    

    

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    # app.run()
    app.run(host='0.0.0.0', port=5000)
