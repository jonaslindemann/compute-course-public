program ex17

    implicit none

    integer, parameter :: rk = selected_real_kind(15,300)

    real(rk) :: A(10,20)

    call mysub(A)

contains

subroutine mysub(A)

    real(rk) :: A(:,:)
    real(rk) :: B(size(A,2), size(A,1))

    print*, size(A,1)
    print*, size(A,2)
    print*, size(B,1)
    print*, size(B,2)

    A = 42.0_rk
    B = 84.0_rk

end subroutine mysub

end program ex17
