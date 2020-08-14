program ex16

    implicit none

    integer, parameter :: rk = selected_real_kind(15,300)

    interface
            subroutine mysub(a, B, C)
                    integer, parameter :: rk = selected_real_kind(15,300)
                    integer :: a
                    real(rk) :: B(:,:)
                    real(rk) :: C(:)
            end subroutine mysub
    end interface

    integer :: a
    real(rk) :: B(10,20)
    real(rk) :: C(30)

    call mysub(a, B, C)

end program ex16
