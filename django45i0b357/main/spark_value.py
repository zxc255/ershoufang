# 创建SparkSession
import json
import sys

from py4j.java_gateway import java_import
from pyspark.sql import SparkSession

# 获取通过命令行传递的参数
if len(sys.argv) > 1:
    args = sys.argv[1]
else:
    args = None

table_name = args.split("--")[0].strip()
x_name = args.split("--")[1].strip()
y_name = args.split("--")[2].strip()
date = args.split("--")[3].strip()

spark = SparkSession.builder \
    .appName(f"{table_name}_{x_name}_{y_name}_value") \
    .config("spark.master", "spark://hadoop1:7077") \
    .getOrCreate()
sc = spark.sparkContext

# 读取HDFS上的CSV文件
data_rdd = sc.textFile(f"hdfs://hadoop1:9820/input/{table_name}.csv")

# 获取表头并提取列索引
header = data_rdd.first()
header_columns = header.split(",")
x_index = header_columns.index(x_name)
y_index = header_columns.index(y_name)
status_index = header_columns.index("status") if table_name == "orders" else None

# 过滤数据
if table_name == "orders":
    filtered_rdd = data_rdd.filter(lambda row: row != header and row.split(",")[status_index] in ["已支付", "已发货", "已完成"])
else:
    filtered_rdd = data_rdd.filter(lambda row: row != header)

print(filtered_rdd.collect())  # 查看过滤后的数据
# 处理日期分组
def extract_date(row, date_type):
    cols = row.split(",")
    date_value = cols[x_index]
    if date_type == "date":
        return date_value.split(" ")[0]  # 只取日期部分
    elif date_type == "month":
        return date_value[:7]  # 年-月
    elif date_type == "year":
        return date_value[:4]  # 年
    return cols[x_index]

# 生成键值对 (日期值, y值)
result_rdd = (
    filtered_rdd
    .map(lambda row: (extract_date(row, date), float(row.split(",")[y_index]) if row.split(",")[y_index] else 0))
)
print(result_rdd.collect())  # 查看键值对生成结果
# 按键聚合总和
aggregated_rdd = result_rdd.reduceByKey(lambda a, b: a + b)

print(aggregated_rdd.collect())  # 查看聚合结果
# 将结果转换为字典格式


result_dict_rdd = aggregated_rdd.map(lambda x: json.dumps({x_name: x[0], "total": round(x[1], 2)}))

java_import(sc._jvm, "org.apache.hadoop.fs.FileSystem")
java_import(sc._jvm, "org.apache.hadoop.conf.Configuration")
hadoop_conf = sc._jvm.Configuration()
fs = sc._jvm.FileSystem.get(hadoop_conf)
output_path = f"hdfs://hadoop1:9820/output/{table_name}/value{x_name}{y_name}{date}"
if fs.exists(sc._jvm.org.apache.hadoop.fs.Path(output_path)):
    fs.delete(sc._jvm.org.apache.hadoop.fs.Path(output_path), True)
# 保存结果为 JSON 格式到 HDFS
try:
    result_dict_rdd.saveAsTextFile(output_path)
except Exception as e:
    print(f"An error occurred: {e}")

sc.stop()
