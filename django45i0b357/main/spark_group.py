# 创建SparkSession
import json
import sys

from py4j.java_gateway import java_import
from pyspark import SparkConf, SparkContext

# 获取通过命令行传递的参数
if len(sys.argv) > 1:
    args = sys.argv[1]
else:
    args = None

table_name = args.split("--")[0].strip()
column_name = args.split("--")[1].strip()

# 创建SparkConf和SparkContext
conf = SparkConf().setAppName(f"{table_name}_{column_name}_group").setMaster("spark://hadoop1:7077")
sc = SparkContext(conf=conf)

# 读取HDFS上的CSV文件
data_rdd = sc.textFile(f"hdfs://hadoop1:9820/input/{table_name}.csv")

# 获取表头并提取列索引
header = data_rdd.first()
header_columns = header.split(",")
column_index = header_columns.index(column_name)

# 处理数据，过滤表头，统计分组
counts_rdd = (
    data_rdd
    .filter(lambda row: row != header)  # 过滤掉表头
    .map(lambda row: row.split(","))  # 将行分割为列表
    .map(lambda cols: (cols[column_index], 1))  # 创建键值对 (column_value, 1)
    .reduceByKey(lambda a, b: a + b)  # 按照键求和
)

# 转换为所需格式并保存为JSON文件
result_rdd = counts_rdd.map(lambda x: json.dumps({column_name: x[0], "total": x[1]}))
java_import(sc._jvm, "org.apache.hadoop.fs.FileSystem")
java_import(sc._jvm, "org.apache.hadoop.conf.Configuration")
hadoop_conf = sc._jvm.Configuration()
fs = sc._jvm.FileSystem.get(hadoop_conf)
output_path = f"hdfs://hadoop1:9820/output/{table_name}/group{column_name}"
if fs.exists(sc._jvm.org.apache.hadoop.fs.Path(output_path)):
    fs.delete(sc._jvm.org.apache.hadoop.fs.Path(output_path), True)
result_rdd.saveAsTextFile(output_path)
sc.stop()
