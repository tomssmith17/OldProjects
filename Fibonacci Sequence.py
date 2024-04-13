### Fibonacci Sequence ###
# Sequence construction: first 2 terms are equal to 1, thereafter each term is
# the sum of the previous 2 terms. 

#function that returns the Nth term in the fibonacci sequence
#this version of the function repeats itself with the low fib values thus
#becoming much slower and resource intensive the larger the value of n.

def fibonacci(n):
    if n == 1:
        return 1
    elif n == 2:
        return 1
    elif n > 2:    #function calls itself so is a recursive function
        return fibonacci(n-1) + fibonacci(n-2)

for n in range(1, 6):
    print n, ":", fibonacci(n)



#Memoization: store the values for recent function calls so future calls
#do not have to repeat the work, aka cache values.

fibonacci_cache = {}
def fibV2(n):
    #If we have cached the value, then return it
    if n in fibonacci_cache:
        return fibonacci_cache[n]

    #Compute the Nth term
    if n == 1:
        value = 1
    elif n == 2:
        value = 1
    elif n > 2:
        value = fibV2(n-1) + fibV2(n-2)

    #Cache the value and return it
    fibonacci_cache[n] = value
    return value

for n in range(1, 501):
    print n, ":", fibV2(n)



"""
#Memoization V2, better method

from functools import lru_cache #think it is accessing python 2.7 version
                                #of functools which doesn't have lru_cache,
                                #not sure how to fix.

@lru_cache(maxsize = 1000) #default is 128 most recently used values are cached

def fibV3(n):
    #Check that the input is a positive integer
    if type(n) != int:
        raise TypeError("n must be a positive int")
    if n < 1:
        raise ValueError("n must be a positive int")


    #Compute the Nth term
    if n == 1:
        return 1
    elif n == 2:
        return 1
    elif n > 2:    
        return fibV3(n-1) + fibV3(n-2)

for n in range(1, 501):
    print n, ":", fibV3(n)
    #print fibV3(n+1) / fibV3(n) #ratio between consequtive terms, becomes golden ratio 1.61 ish

"""


#simple version
a, b = 0, 1
for i in xrange(0, 10):
    print a
    a, b = b, a + b


################################################################





