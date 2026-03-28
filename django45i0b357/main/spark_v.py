import csv
import multiprocessing
import os
import json
from pathlib import Path
import paramiko
from hdfs import InsecureClient
from pyspark import SparkConf
import mysql.connector
from pyspark.sql import SparkSession

from util.configread import config_read

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
hadoop_client = InsecureClient('http://hadoop1:9870', user='root')
dbtype, host, port, user, passwd, dbName, charset, hasHadoop = config_read(os.path.join(parent_directory,"config.ini"))
# 配置Hadoop主节点的信息
master_host = "hadoop1"
master_user = "root"
master_password = "123456"

def upload_csv():
    mysql_conn = mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=passwd,
        database=dbName.replace(" ", "").strip()
    )
    cursor = mysql_conn.cursor()
    cursor.execute("SELECT * FROM ncsecondhandhouse")
    ncsecondhandhouse_column_info = cursor.fetchall()
    # 将数据写入 CSV 文件
    ncsecondhandhouse_path = os.path.join(parent_directory, "ncsecondhandhouse.csv")
    with open(ncsecondhandhouse_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # 写入表头
        writer.writerow([desc[0] for desc in cursor.description])
        # 写入数据行
        for row in ncsecondhandhouse_column_info:
            writer.writerow(row)
    # 上传映射文件
    ncsecondhandhouse_hdfs_csv_path = f'/input/ncsecondhandhouse.csv'
    ncsecondhandhouse_local_csv_path = os.path.join(parent_directory,"ncsecondhandhouse.csv")
    # 删除已有的数据
    if hadoop_client.status(ncsecondhandhouse_hdfs_csv_path, strict=False):
        hadoop_client.delete(ncsecondhandhouse_hdfs_csv_path, recursive=True)
    hadoop_client.upload(ncsecondhandhouse_hdfs_csv_path, ncsecondhandhouse_local_csv_path)
    # 上传group文件
    group_path = f'/input/spark_group.py'
    localgroup_path = os.path.join(parent_directory,"main","spark_group.py")
    # 删除已有的数据
    if not hadoop_client.status(group_path, strict=False):
        hadoop_client.upload(group_path, localgroup_path)
    # 上传value文件
    value_path = f'/input/spark_value.py'
    localvalue_path = os.path.join(parent_directory,"main","spark_value.py")
    # 删除已有的数据
    if not hadoop_client.status(value_path, strict=False):
        hadoop_client.upload(value_path, localvalue_path)

    cursor.close()
    mysql_conn.close()

# 执行分析命令
def send_cmd():

    job_commands = [
    f'''/export/server/spark/bin/spark-submit \
        --master spark://{master_host}:7077 \
        --conf "spark.pyspark.driver.python=/usr/local/bin/python3" \
        --conf "spark.pyspark.python=/usr/local/bin/python3" \
        hdfs://hadoop1:9820/input/spark_group.py \
        ncsecondhandhouse--orientation
    ''',
    f'''/export/server/spark/bin/spark-submit \
        --master spark://{master_host}:7077 \
        --conf "spark.pyspark.driver.python=/usr/local/bin/python3" \
        --conf "spark.pyspark.python=/usr/local/bin/python3" \
        hdfs://hadoop1:9820/input/spark_group.py \
        ncsecondhandhouse--plot
    ''',
    f'''/export/server/spark/bin/spark-submit \
        --master spark://{master_host}:7077 \
        --conf "spark.pyspark.driver.python=/usr/local/bin/python3" \
        --conf "spark.pyspark.python=/usr/local/bin/python3" \
        hdfs://hadoop1:9820/input/spark_group.py \
        ncsecondhandhouse--region
    ''',
    f'''/export/server/spark/bin/spark-submit \
        --master spark://{master_host}:7077 \
        --conf "spark.pyspark.driver.python=/usr/local/bin/python3" \
        --conf "spark.pyspark.python=/usr/local/bin/python3" \
        hdfs://hadoop1:9820/input/spark_group.py \
        ncsecondhandhouse--types
    ''',
    f'''/export/server/spark/bin/spark-submit \
        --master spark://{master_host}:7077 \
        --conf "spark.pyspark.driver.python=/usr/local/bin/python3" \
        --conf "spark.pyspark.python=/usr/local/bin/python3" \
        hdfs://hadoop1:9820/input/spark_value.py \
        ncsecondhandhouse--region--unitprice--
    ''',
    ]

    file_names=[]
    table_names=[]
    for job_command in job_commands:
        if job_command.__contains__("spark_group.py"):
            groups = job_command.split("hdfs://hadoop1:9820/input/spark_group.py")[1].split("--")
            filename = "group"+groups[1].strip().replace("\n","")
            table_name = groups[0].strip()
        else:
            values = job_command.split("hdfs://hadoop1:9820/input/spark_value.py")[1].split("--")
            yname = values[2].strip()
            if yname.__contains__(","):
                yname = ''.join(yname.split(","))
            date=""
            if len(values)>=4:
                date = values[3]
            filename = ("value" + values[1].strip()+yname.strip()+date.strip()).replace("\n","")
            table_name = values[0].strip()
        file_names.append(filename)
        table_names.append(table_name)
        run_spark_job_on_remote(job_command)

    for index,filename in enumerate(file_names):
        download_json(table_names[index],filename)

def download_json(tableName,filename):
    try:
        hdfs_output_path = f"/output/{tableName}/{filename}"
        local_output_path = os.path.join(parent_directory,f'{tableName}_{filename}.json')

        # 列出HDFS输出目录中的文件
        files = hadoop_client.list(hdfs_output_path)
        json_files = [f for f in files if f.startswith('part')]
        merged_data=[]
        if json_files:
            for json_file in json_files:
                hdfs_file_path = f"{hdfs_output_path}/{json_file}"
                try:
                    with hadoop_client.read(hdfs_file_path) as reader:
                        content = reader.read().decode('utf-8').strip()
                        if not content:
                            continue
                        for line in content.splitlines():
                            if line.strip():  # 忽略空行
                                merged_data.append(json.loads(line))
                except Exception as e:
                    print(f"e:{e}")
        print("merged_data:",merged_data)
        # 将合并后的数据写入本地文件
        with open(local_output_path, 'w', encoding='utf-8') as local_file:
            json.dump(merged_data, local_file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"e:{e}")

def run_spark_job_on_remote(job_command, tableName, filename):
    # 创建SSH客户端
    ssh = paramiko.SSHClient()
    try:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(master_host, username=master_user, password=master_password)
        stdin, stdout, stderr = ssh.exec_command(job_command)
        stdout.channel.recv_exit_status()
        output = stdout.read().decode()
        print(f"Output from :\n{output}")
    except Exception as e:
        print(f"e:{e}")
    finally:
        ssh.close()

#spark分析
def spark_analyze(request):
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "成功", "data": {}}
        try:
            upload_csv()
            send_cmd()
            return JsonResponse(msg, encoder=CustomJsonEncoder)
        except Exception as e:
            msg['code']=system_error_code
            msg['msg'] = f"发生错误：{e}"
            return JsonResponse(msg, encoder=CustomJsonEncoder)
