program overloading

    use utils
    use special

    implicit none

    integer :: a = 42
    real(rk) :: b = 42.0_8

    a = func(a)
    b = func(b)

    print *, a
    print *, b

end program overloading
