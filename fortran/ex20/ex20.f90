program ex20

    use utils

    implicit none

    real(rk), allocatable :: A(:,:)
    real(rk), allocatable :: B(:,:)
    integer :: i, j

    allocate(A(20,20), B(20,20))

    call initRand()
    call randMat(A, 0.0_rk, 1.0_rk)
    call randMat(B, 0.0_rk, 1.0_rk)

    do i=1,20
        A(i,i) = 2.0_rk * B(i,i)
    end do

    forall(i=1:20) A(i,i) = 2.0_rk * B(i,i)

    forall(i=1:20, j=1:20) A(i,j) = i + j

    forall(i=1:20, j=1:20, A(i,j)/=0.0_rk)
        B(i,j) = 1.0/A(i,j)
    end forall

    deallocate(A, B)

end program ex20
