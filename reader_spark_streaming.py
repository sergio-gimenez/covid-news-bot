
import findspark
findspark.init('/opt/spark')
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import SQLContext
from pyspark.sql.functions import desc
import time
from collections import namedtuple


# Create a local StreamingContext with two working thread and batch interval of 1 second
sc = SparkContext("local[2]", "NetworkWordCount")
ssc = StreamingContext(sc, 1)

# Create a DStream that will connect to hostname:port, like localhost:9999
# Firewalls might block this!
lines = ssc.socketTextStream("127.0.0.1", 5555)

# Split each line into words
words = lines.flatMap(lambda line: line.split(" "))

# Count each word in each batch
pairs = words.map(lambda word: (word, 1))
wordCounts = pairs.reduceByKey(lambda x, y: x + y)

# Print the first ten elements of each RDD generated in this DStream to the console
wordCounts.pprint()

ssc.start()  # Start the computation
ssc.awaitTermination()  # Wait for the computation to terminate

# Can only run this once. restart your kernel for any errors.
sc = SparkContext()

ssc = StreamingContext(sc, 10)
sqlContext = SQLContext(sc)

socket_stream = ssc.socketTextStream("127.0.0.1", 5555)

lines = socket_stream.window(20)

fields = ("tag", "count")
Tweet = namedtuple('Tweet', fields)

# Use Parenthesis for multiple lines or use \.
(lines.flatMap(lambda text: text.split(" "))  # Splits to a list
 .filter(lambda word: word.lower().startswith("#"))  # Checks for hashtag calls
 .map(lambda word: (word.lower(), 1))  # Lower cases the word
 .reduceByKey(lambda a, b: a + b)  # Reduces
 .map(lambda rec: Tweet(rec[0], rec[1]))  # Stores in a Tweet Object
 .foreachRDD(lambda rdd: rdd.toDF().sort(desc("count"))  # Sorts Them in a DF
             .limit(10).registerTempTable("tweets")))  # Registers to a table.

ssc.start()
time.sleep(10)
ssc.stop()
