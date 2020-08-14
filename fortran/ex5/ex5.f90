program ex5

    implicit none

    integer, parameter :: rk = selected_real_kind(15,300)

    real(rk) :: A(20,20)
    real(rk) :: B(20,20)
    real(rk) :: C(20,20)
    integer  :: i, j

    A(10,:) = 1.0_rk
    A(:,10) = 2.0_rk
    
    B = 0.0_rk
    
    do i=1,20
        do j=1,20
            C(i,j) = 42.0_rk
        end do
    end do

end program ex5
