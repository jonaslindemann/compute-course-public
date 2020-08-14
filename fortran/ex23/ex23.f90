program ex23

    use utils

    implicit none

    real(rk) :: A(5,10)
    real(rk) :: B(5,10)
    integer :: i, j

    call initRand()
    call randMat(A, -1.0_rk, 1.0_rk)
    call printMatrix(A, 'A')

    B = cos(A)

    call printMatrix(B, 'B')

end program ex23
