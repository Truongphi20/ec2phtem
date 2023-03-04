import pandas as pd
import statistics
import numpy as np

# a = pd.DataFrame(((1,2,3),(1,3,5),(2,3,1),(3,1,1),(2,1,1)), columns=["a","b","c"])
# a = a.set_index("a")
# print(a)

# b = a.loc[:,"b"].groupby("a").agg(lambda x: sum(x))
# print(b)

# c = a.groupby("a").agg(lambda x: statistics.mean(x))
# print(c)

frame = pd.DataFrame({"a": [1, 2, 2, 3], "b": ["2", "3"] * 2, "c": ["2", "1", "1","3"]})
print(frame)

print(frame.info())
# print([i for i in frame.columns.tolist()if i != "c"])
frame = frame.apply(pd.to_numeric)
print(frame.info())

# frame1 = frame.groupby([i for i in frame.columns.tolist() if i != "c"]).agg(lambda x: statistics.mean(x)).reset_index()
# print(frame1)