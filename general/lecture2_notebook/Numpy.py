
# coding: utf-8

# # Numpy
# 
# * Python extensions for manipulating large sets of objects organised in a grid-like fashion
#   * Vectors
#   * Matrices
#   * etc...
# * Normal Python datastructures too slow
# 

# # Using numpy

# In[2]:

import numpy as np


# # Array objects
# 
# * Homogeneous collection of large numbers of numbers
#   * Numbers of the same type
#   * Array objects must be full
#   * Size immutable
#   * Numbers can change
# * size = total number of elements in the array (Does not change)
# * shape = number of dimensions
# 

# # Array objects
# 
# * rank = len(shape)
# * typecode = single character identifying the element kind
#   * Number format (i, d etc)
#   * Character
#   * Python reference
# * itemsize = number 8-bit bytes representing a single element
# 

# # Creating arrays from scratch

# Creating arrays with explicit type codes:

# In[4]:

a = np.array([1, 2, 5], float)
print(a)


# In[3]:

b = np.array([5, 4, 3], int)
print(b)


# When creating arrays without type codes, Python will figure out and select type from the provided data.

# In[4]:

c = np.array([1.0, 1.5, 3.0])
print(c)


# In[5]:

d = np.array([1,2,3,4,5,6])
print(d)


# # Multidimensional arrays

# In[6]:

a = np.array([[1,2],[3,4]])
print(a)


# In[7]:

b = np.array([[1,2,3,4],[5,6,7,8]], float)
print(b)


# The shape of the array can be queried using the shape attribute:

# In[8]:

print(a.shape)


# In[10]:

print(b.shape)
r, c = b.shape
print(r, c)


# # Reshaping arrays

# In[11]:

a = np.array([[1,2],[3,4]])
print(a)


# In[12]:

a_flat = np.reshape(a, [4,])
print(a_flat)


# In[13]:

a_flat = np.reshape(a, [1,4])
print(a_flat)


# In[14]:

a_flat = np.reshape(a, [4,1])
print(a_flat)


# In[15]:

b = np.array([[1,2,3,4],[5,6,7,8]], float)
print(b)


# In[16]:

b_shaped = np.reshape(b, [8,])
print(b_shaped)


# In[17]:

b_shaped = np.reshape(b, [4,2])
print(b_shaped)


# **Please note** this is not the same as:

# In[18]:

b_trans = np.transpose(b)
print(b_trans)


# # Growing an array

# In[19]:

a = np.array([1,2])
print(a)


# In[20]:

b = np.array([a,a])
print(b)


# In[21]:

base = np.array([[1,2],[3,4]])
print(base)


# In[22]:

big = np.resize(base, [9,9])
print(big)


# In[23]:

big = np.resize(base, [4,4])
print(big)


# In[24]:

big = np.resize(base, [4,2])
print(big)


# # Arrays on the fly

# In[25]:

a = np.zeros([4,4])
print(a)


# In[26]:

b = np.ones([5,10], float)
print(b)


# In[27]:

a = np.arange(10)
print(a)


# In[28]:

b = np.reshape(np.arange(100), [10,10])
print(b)


# In[29]:

a = np.arange(0,10)
print(a)


# In[30]:

a = np.arange(-10,10)
print(a)


# In[31]:

a = np.arange(-10,10,2)
print(a)


# There are different ways of creating arrays with specific numbers. However, it is important to do it in the correct way. First the slow way:

# In[32]:

a = np.array([[42]*5]*5)
print(a)


# First creating a zero array and then adding 42 is much faster:

# In[35]:

a = np.zeros([5,5])+42
print(a)


# Identity arrays can also be created using the identity() function.

# In[38]:

i = np.identity(10)
print(i)


# # Creating arrays with a linear variation

# In[39]:

x = np.linspace(0,1.0,10)
print(x)


# In[40]:

x = np.linspace(0,1.0,20)
print(x)


# # Operating on arrays

# Most python operators can be used with arrays. The following examples shows how it can be used.

# In[41]:

a = np.array([[1,2],[3,4]])
print(a)


# Element wise addition.

# In[42]:

print(a+3)


# Element wise multiplication

# In[43]:

print(a*3)


# It is also possible to use normal mathematical functions with arrays.

# In[44]:

print(np.sin(a))


# Element wise negation using the - operator.

# In[45]:

print(-a)


# Arrays of the same number of elements can also be added together.

# In[46]:

print(a+a)


# Adding differently sized arrays is also possible. Values from the smaller array is continously added to the larger array as shown in this example:

# In[47]:

a = np.array([1,2,3])
b = np.ones([5,3])
print(a)
print(b)


# In[48]:

print(a+b)


# # Getting and setting values

# Retrieving a single value:

# In[49]:

a = np.arange(10)
print(a)


# In[52]:

print(a[0])


# Retrieving a range of values:

# In[53]:

print(a[1:5])


# Please note that the range index is defined as [start:stop] and does not include the *stop* index.

# You can get all values of a list except the last one by using -1 as the last index.

# In[58]:

print(a[:-1])


# Using other negative numbers will retrieve other ranges:

# In[59]:

print(a[:-2])


# It is also possible to use arange() and reshape to create arrays with increasing numbers:

# In[60]:

a = np.arange(16)+1
print(a)


# In[61]:

b = np.reshape(a, [4,4])
print(b)


# It is also possible to retrieve rows and columns:

# In[62]:

print(b[0]) # row 0 of b


# In[63]:

print(b[:,1]) # column 1 of b


# In[64]:

print(b[-1]) # last row of b


# In[65]:

print(b[:,-2]) # column 2 of b


# In[66]:

print(b)


# Values can be assigned using index notation as well:

# In[67]:

b[0,0] = 42
print(b)


# Lists and arrays can be intermixed and used in assignments. Assign a row using the following statement:

# In[68]:

b[1] = [42,42,42,42]
print(b)


# Columns can be assigned in the same fashion:

# In[69]:

b[:,2] = [42,42,42,42]
print(b)


# # Slicing

# In[70]:

a = np.reshape(np.arange(16)+1,[4,4])
print(a)


# In[71]:

print(a[:,:])


# In[72]:

print(a[:,1])


# In[73]:

print(a[1,:])


# # Ufuncs

# * Operates elementwise on arrays
# * Available as callable objects (functions)
# * Can operate on Python sequences
# * Can take output arguments
# * Have special methods

# In[74]:

a = np.arange(10)
print(a)


# In[ ]:

print(np.add(a,a))


# In[ ]:

print(a+a)


# In[ ]:

print(np.sin(a))


# In[ ]:

print(add(a, range(10)))


# Ufuncs are often faster, but source code will be harder to read. Sometimes using a ufunc can eliminate a unecessary copying of large arrays. The following example shows how a ufunc is used to avoid this.

# In[75]:

a = np.arange(10)
a = a * 10 # This will make a copy of a
print(a)


# Again with a ufunc.

# In[76]:

a = np.arange(10)
np.multiply(a,10,a)
print(a)


# ## The add.reduce function (A quicker sum)

# add.reduce() can be used to sum (reduce) an array.

# In[ ]:

a = np.arange(10)
print(a)


# In[ ]:

print(np.add.reduce(a))


# This is faster than:

# In[ ]:

print(a.sum())


# ## add.accumulate

# In[ ]:

a = np.arange(10)
print(a)


# In[ ]:

print(np.add.accumulate(a))


# ## transpose
# 
# To do a matrix-transpos of an array, the transpose() function can be used.

# In[ ]:

a = np.reshape(np.arange(16), [4,4])
print(a)


# In[ ]:

print(np.transpose(a))


# ## diagonal() and trace() functions

# In[77]:

a = np.reshape(np.arange(16), [4,4])
print(a)


# In[78]:

print(np.diagonal(a))


# In[79]:

print(np.trace(a))


# It is also possible to do traces left and right of the diagonal, by adding a parameter to the trace() function.

# In[80]:

print(np.trace(a,1))


# In[81]:

print(np.trace(a,-1))


# ## Matrix multiplication
# 
# The * operator on array is equivalent to an elementwise multiplication of matrices. If you want to do a matrix multiplication on arrays, .dot() method or the @-operator can be used.

# In[82]:

a = np.reshape(np.arange(16), [4,4])
print(a)


# In[83]:

print(a.dot(a))


# # Exempel 1

# In[84]:

import math
import numpy as np

x = np.linspace(0.0, 2.0*math.pi, 20)
y = np.sin(x)

print(x)
print(y)


# # Exempel 2

# In[85]:

import pylab as pl


# In[86]:

get_ipython().magic('matplotlib inline')


# In[88]:

x = np.linspace(0.0, 2.0*math.pi, 20)
y = np.sin(x)

pl.plot(x,y)


# # Matrices in Numpy
# 
# Arrays in Numpy are a generic array storage type and in itself not aware of any matrix operations. If this is desired Numpy provides an array derived type matrix, which provides this functionality. Some examples are illustrated below:

# In[89]:

A = np.matrix( [[1,2,3],[11,12,13],[21,22,23]])
x = np.matrix( [[1],[2],[3]] )
y = np.matrix( [[1,2,3]] )
print(A)


# In[90]:

print(x)


# In[91]:

print(y)


# In[92]:

print(A.T) # Matrix transpose


# In[93]:

print(A*x) # Matrix mulitply A * x


# In[94]:

print(A.I) # Matrix inverse


# In[95]:

print(np.linalg.solve(A,x)) # Solve A * y = x


# In[ ]:



