# Loading the Python environment

In the course we will be using the Ananconda Python environment. This environment is loaded on Aurora using the following module commands:

    $ module load anaconda3

Verify that the correct version of Python has been loaded:

    $ python -V
    Python 3.6.1 :: Anaconda 4.4.0 (64-bit)

# Cloning the course material

The material that we are going to use in this course can be cloned from git using the following command:

    $ git clone https://github.com/jonaslindemann/sese-course-public.git
    Cloning into 'sese-course-public'...
    remote: Counting objects: 60, done.
    remote: Compressing objects: 100% (42/42), done.
    remote: Total 60 (delta 10), reused 60 (delta 10), pack-reused 0
    Unpacking objects: 100% (60/60), done.

# Starting Spyder - IDE

The development environment we will be using is Spyder. Spider is started from the command line using the following commands:

    spyder &

This should bring up a graphical IDE for Python.

# Starting a Jupyter Notebook session

Change into the course directory:

    $ cd sese-course-public
    $ jupyter-notebook .
    
This will start a new jupyter session and open a browser window.
    
