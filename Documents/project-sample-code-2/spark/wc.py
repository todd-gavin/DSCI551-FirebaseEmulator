from pyspark import SparkContext
from operator import add

sc = SparkContext(appName="dsci551")

lines = sc.textFile('hello.txt')

counts = lines.flatMap(lambda x: x.split(' ')) \
            .map(lambda x: (x, 1)) \
            .reduceByKey(add)

output = counts.collect()

for v in output:
    print(v[0], v[1])
