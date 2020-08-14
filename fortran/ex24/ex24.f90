program ex24

    use utils

    implicit none

    real(rk) :: A(10,10)
    real(rk) :: B(10,10)
    real(rk) :: C(10,10)
    real(rk) :: v1(3)
    real(rk) :: v2(3)
    real(rk) :: dp

    call initRand()
    call randMat(A, -1.0_rk, 1.0_rk)
    call randMat(B, -1.0_rk, 1.0_rk)
    call printMatrix(A, 'A')
    call printMatrix(B, 'B')

    C = matmul(A, B)

    call printMatrix(C, 'C')

    v1 = (/1.0, 0.0, 0.0/)
    v2 = (/0.0, 1.0, 0.0/)
    dp = dot_product(v1, v2)

    print*, dp


end program ex24
