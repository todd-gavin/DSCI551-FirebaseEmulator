# more details: https://pypi.org/project/dill/
import dill as pickle

l = [1, 2, 3, 4]

l1 = filter(lambda x: x % 2 == 0, l)
m = map(lambda x: x * 2, l1)

# serialize m into byte stream s
s = pickle.dumps(m)

# transmitting s over network ...

# deserialize s into an object m
m1 = pickle.loads(s)
list(m1)


