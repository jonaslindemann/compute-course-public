program ex7

    implicit none

    integer, parameter :: rk = selected_real_kind(15,300)

    real(rk) :: a
    real(rk) :: b
    integer  :: i, c

    a = 0.5_rk
    i = 5
    b = a*i
    c = a*i

    print*, b
    print*, c

end program ex7
