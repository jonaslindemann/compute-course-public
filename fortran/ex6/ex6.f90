program ex6

    implicit none

    integer, parameter :: rk = selected_real_kind(15,300)

    real(rk) :: x, y
    real(rk) :: a, b, c

    x = 3.0_rk
    y = 4.0_rk

    print*, x**-y   ! --- Ok with some compilers
    print*, x**(-y) ! --- Correct expression

    a = 3.0_rk
    b = 2.0_rk
    c = 4.0_rk

    print*, -a+b+c
    print*, -a+b*c     ! --- Evaluates as ((-a)+(b*c))
    print*, (-a+b)*c
    print*, -(a+b)*c   ! --- Evaluates as -((a+b)*c)
    print*, -((a+b)*c)
    print*, a**b**c    ! --- Evaluates as a**(b**c)
    print*, a**(b**c)
    print*, (a**b)**c

    print*, 6/3
    print*, 8/3
    print*, -8/3

    print*, 2**3
    print*, 2**(-3)    ! --- = 1/(2**3)
    print*, 1/(2**3)
    print*, 2.0_rk**(-3.0_rk)

end program ex6
