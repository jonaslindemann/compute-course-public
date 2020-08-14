program ex18

    implicit none

    integer, parameter :: rk = selected_real_kind(15,300)

    real(rk), allocatable :: f(:)
    real(rk), dimension(:,:), allocatable :: K

    allocate(f(20))
    allocate(K(20,20))

    K = 42.0_rk
    f = 84.0_rk

    deallocate(f)
    deallocate(K)

end program ex18
