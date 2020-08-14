subroutine mysub(a, B, C)

    integer, parameter :: rk = selected_real_kind(15,300)

    integer :: a
    real(rk) :: B(10,20)
    real(rk) :: C(30)

    a = 42
    B = 42.0_rk
    C = 84.0_rk

end subroutine mysub
