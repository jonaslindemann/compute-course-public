program ex8

    implicit none

    integer, parameter :: rk = selected_real_kind(15,300)

    real(rk) :: a(10,20), b(10,20)
    real(rk) :: v(5)
    integer  :: i, c

    real(rk) :: ex1(10,20)
    real(rk) :: ex2(5)
    real(rk) :: ex3(5)
    logical  :: ex4(10,20)

    a = 20.0_rk
    a(1,1) = 2.0_rk

    b = 2.0_rk
    v = 2.0_rk

    ex1 = a/b
    ex2 = v + 2.0_rk
    ex3 = 5/v + a(1:5,5)
    ex4 = a.eq.b

end program ex8
