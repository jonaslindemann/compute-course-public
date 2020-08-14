module mymod

integer, parameter :: rk = selected_real_kind(15,300)

contains

subroutine mysub(a, B, C)

    integer :: a
    real(rk) :: B(:,:)
    real(rk) :: C(:)

    print*, size(B,1)
    print*, size(B,2)
    print*, size(C,1)

    a = 42
    B = 42.0_rk
    C = 84.0_rk

end subroutine mysub

end module mymod
