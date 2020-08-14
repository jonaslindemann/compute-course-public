program ex3

    implicit none

    integer :: A(16)
    integer :: B(8,2)
    integer :: C(2,8)

    integer  :: i, j

    do i = 1, 16
        A(i) = i
    end do

    B = reshape(A, (/8, 2/))
    C = reshape(A, (/2, 8/))

end program ex3
