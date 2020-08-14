program ex29

    use utils

    implicit none

    real(rk) :: A(8,8)

    call initRand()
    call randMat(A, 0.0_rk, 100.0_rk)

    call printArray(A)


contains

subroutine printArray(A)

    real(rk), dimension(:,:) :: A
    integer :: rows, cols, i, j
    character(255) :: fmt

    rows = size(A,1)
    cols = size(A,2)

    write(fmt, '(A,I1,A)') '(',cols, 'G8.3)'

    do i=1,rows
            print fmt, (A(i,j), j=1,cols)
    end do

end subroutine printArray

end program ex29
