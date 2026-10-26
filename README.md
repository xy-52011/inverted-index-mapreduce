# Inverted Index with Hadoop MapReduce

## 项目简介

本项目使用 Hadoop MapReduce 框架实现文档倒排索引（Inverted Index）。倒排索引是全文搜索引擎的核心数据结构，用于存储单词到文档位置的映射。

## 项目结构

```
inverted-index/
├── input/                          # 输入数据
│   ├── document01.txt ~ document10.txt  # 10个英文文档
│   └── stopwords.txt               # 英文停词表
├── src/main/java/com/sdu/invertedindex/
│   ├── InvertedIndexMapper.java    # Mapper：分词、过滤停词
│   ├── InvertedIndexCombiner.java  # Combiner：本地局部聚合
│   ├── InvertedIndexReducer.java   # Reducer：汇总倒排索引
│   └── InvertedIndexDriver.java    # Driver：作业配置与提交
├── output/
│   └── part-r-00000                # 倒排索引结果（本地验证）
├── local_inverted_index.py         # Python本地验证版本
├── pom.xml                         # Maven配置文件
└── README.md
```

## 输出格式

```
word  <document01.txt,count1>;<document02.txt,count2>;<total,totalcount>.
```

## 运行方式

### 1. 本地 Python 验证

```bash
python local_inverted_index.py
```

### 2. Hadoop 集群运行

```bash
# 上传数据到 HDFS
hdfs dfs -mkdir -p /user/invertedindex/input
hdfs dfs -put input/document*.txt /user/invertedindex/input/
hdfs dfs -put input/stopwords.txt /user/invertedindex/

# 打包
mvn clean package

# 提交 MapReduce 作业
hadoop jar target/inverted-index-1.0.jar \
  com.sdu.invertedindex.InvertedIndexDriver \
  /user/invertedindex/input \
  /user/invertedindex/stopwords.txt \
  /user/invertedindex/output

# 查看结果
hdfs dfs -cat /user/invertedindex/output/part-r-00000
```

## 实验统计

- 文档数量：10 个英文文档
- 索引单词数：680 个
- 单词-文档对：1006 个
