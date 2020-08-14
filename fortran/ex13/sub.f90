subroutine mysub(a, B, br, bc, C, cr)

    integer, parameter :: rk = selected_real_kind(15,300)

    integer :: a
    integer :: br, bc, cr
    real(rk) :: B(br,bc)
    real(rk) :: C(cr)

    a = 42
    B = 42.0_rk
    C = 84.0_rk

end subroutine mysub
