# General
* When you need to cast a sequence to a specific type
```python
a = map(int, input().split())
# map with sequence unpacking
a,b,c,d,e = map(bin,input().split())
# double map with sequence unpacking
a,b,c = map(bin,map(int,input().split()))
# same thing but with the same number of characters in a more readable fashion
a,b,c = map(lambda e:bin(int(e)),input())
```

* To use a shorter name for a function that is often use
```python
i=input
i()
# or
import math
f=math.factorial
f(10)
```
* To read input and print its value 
```python
while 1:print(input())
```
# Sequence


* When you want to print the content of a sequence without performing a join()
```python
sequence = ["a","b","c","d","e"]
print(*sequence) # => a b c d e
# equivalent 
print(" ".join(sequence))
```

* When you want to add all elements in a list without two inputs has to be read but the first and you want to add it to a list 
```python
# eg:
n = int(input())
l = [input() for i in range(n)]
# shorter !!
l = [input() for _ in[1] * int(input())]
```

* When you want to print the items in a list but first the ones that at even index, and after the one at odd index 
```python
print(*seq[::2]+seq[1::2],sep='\n')
```

* To map several inputs in a row
```python
a=map(int,(input()+" "+input()).split())
# 
```
* To count number of times a set of specific character appears in a string
```python
a=map(input().count,"ABCD")
# 
```
# Math
* To round a float without using math.ceil function
```python
x = 1.24
# (x%1>0) is evaluate to True if x has a decimal value. 
# Adding True to an int is the same as adding 1
# When casting to int, you get the integer part
int(x+(x%1>0)) # = int(1.24 + 1) => 2
```
* To sum values of n numbers from 1 to n
```python
n = 9
s = sum(range(n))
# or shorter version
s = (n+1)*(n/2)
```

# Comparison
 
* When you want to compare a value against a range
```python
if 2 < value < 10:
    ...
```
