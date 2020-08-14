# Exercise 1 - Handling command line arguments and formatting

Implement a script that takes the following input from the command line

    python ex1.py 1.0 2.0 3.0 4.0

and the program writes out

    sin(1)=0.841471
    sin(2)=0.909297
    sin(3)=0.14112
    sin(4)=-0.756802

 a) Use a loop to traverse the values and print out the expression. The list of arguments can be retrieved using sys.argv[1:]
 b) Use a while statement to traverse the argument list
 c) Implement a different function

# Exersise 2 - Reading and writing to files

Create a file, input.dat, with the following content:

    1.0 2.0
    3.0 4.0
    5.0 6.0
    7.0 8.0
    9.0 10.0

Write a python script that reads these values into a list, table. The list should contain rows, in which each row is a list. Values should be stored as floating point values.

The script should also interate over the table and calculate the sum of each row to, output.dat.

Tips: Floating point conversion can be done using the function float(x), where x is a string.

# Exercise 3 - Implement a function in Python for calculating mean and variance (using lists)

Implement the following formulas in a Python function:

![alt text](formula.png "Mean and variance")

The function should return both mean value and variance using the return statement.

    mean, variance = myfunction(....)

Create a test program that creates a list of 200 random numbers, which is passed to the function.

Random numbers can be created with the function random.random(...), see the following example.

    import random as rd
    random_value = rd.random()  

# Exercise 4 - Implement a function in Python for calculating mean and variance (using numpy)

Implement the following formulas in a Python function:

![alt text](formula.png "Mean and variance")

The function should implement the sums using builtin Numpy functions. No loops required. The function should return both mean value and variance using the return statement.

    mean, variance = myfunction(....)

Create a test program that creates a vector of 200 random numbers, which is passed to the function.

Random arrays can be created with the function numpy.random.rand(...), see the following examples.

    import numpy as np
    values = np.random.rand(200)
    
# Exercise 5

Do exercises 1.1-1.5 and 2.1-2.3 at http://math.illinois.edu/~shahkar2/cbmg/numpy-exercises.html

# Exercise 6 - Reading binary files from disk

In this exercise you need to read elevation data from a binary file data/colorado_elev.vit. The file contains a file header of 268 bytes. After the header the elevation data is stored as unsigned bytes (ubyte in NumPy). The elevation data is stored in a 400 x 400 grid. 

You need to open the file as a binary file with the open command ("rb" as open action property), so that you get a file pointer. The file pointer object has a command seek() which can be used to move the file pointer to a specific location in the file. The following example shows how the file pointer is moved 500 bytes:

    fp.seek(500, os.SEEK_SET)
    
You need to add

    import os 
    
in your import section. 

Display the elevation data using the plt.imshow(...) function in matplotlib. Add a colorbar to the plot.
