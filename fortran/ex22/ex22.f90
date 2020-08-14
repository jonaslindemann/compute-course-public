program ex22

    use utils

    implicit none

    real(rk) :: A(5,10)
    integer :: i, j

    do i=1,5
        do j=1,10
            A(i,j) = (i-1)*10+j
        end do
    end do

    call printMatrix(A, 'A')
    call printMatrix(A(1:2,5:10), 'A2')
    call printVector(A(1,5:10), 'a2')
    call printMatrix(A(:,5:10), 'A3')
    call printMatrix(A((/1,3/),(/2,4/)), 'A4')

end program ex22
