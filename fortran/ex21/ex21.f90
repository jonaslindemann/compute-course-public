program ex21

    implicit none

    integer, parameter :: rk = selected_real_kind(15,300)

    real(rk), allocatable :: A(:,:)
    real(rk), allocatable :: B(:,:)
    integer :: i, j

    allocate(A(20,20), B(20,20))

    A = 42.0_rk
    B = 84.0_rk

    call swap(A, B)

    deallocate(A, B)

contains

elemental subroutine swap(a, b)
    real(rk), intent(out) :: a, b
    real(rk) :: work

    work = a
    a = b
    b = work

end subroutine swap

end program ex21
