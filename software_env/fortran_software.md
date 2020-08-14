# Loading the Fortran environment

In the course we will be using the Ananconda Python environment. This environment is loaded on Aurora using the following module commands:

    $ module load foss/2017a
    $ module load CMake

Verify that the correct version of Python has been loaded:

    $ gfortran --version
    GNU Fortran (GCC) 6.3.0

# Cloning the course material

The material that we are going to use in this course can be cloned from git using the following command:

    $ git clone https://github.com/jonaslindemann/sese-course-public.git
    Cloning into 'sese-course-public'...
    remote: Counting objects: 60, done.
    remote: Compressing objects: 100% (42/42), done.
    remote: Total 60 (delta 10), reused 60 (delta 10), pack-reused 0
    Unpacking objects: 100% (60/60), done.
    

# Building Fortran software

## Using CMake

Create a new directory for your project:

    $ mkdir mycode
    $ cd mycode
    
Create a CMakeLists.txt file in this with the following content:

    cmake_minimum_required(VERSION 2.8)
    project(mycode)
    enable_language(Fortran)
    add_executable(myapp mycode.f90)

The name of the project is not the same as the executable but is used when generating project files for development environments. 

Your directory should now have the followingh content:

    $ ls
    CMakeLists.txt  mycode.f90
    
To build your code, first create a build directory:

    $ mkdir build
    $ cd build
    
Configure your build (The define is needed to pull the correct compiler version):

    $ cmake -DCMAKE_Fortran_COMPILER=/sw/easybuild/software/Core/GCCcore/6.3.0/bin/gfortran ..

Build it:

    $ make
    
In the build directory there should now be a binary, myapp, which can be executed with:

    $ ./myapp
    
