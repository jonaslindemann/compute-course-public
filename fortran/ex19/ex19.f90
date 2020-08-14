program ex19

    use utils

    implicit none

    real(rk), allocatable :: A(:,:)
    real(rk), allocatable :: B(:,:)

    allocate(A(20,20), B(20,20))

    call initRand()
    call randMat(A, 0.0_rk, 1.0_rk)
    call randMat(B, 0.0_rk, 1.0_rk)

    where (A>0.8_rk) A = 0.8

    where (A<0.2_rk)
        A = 0.2_rk
    end where

    where (B<0.5_rk)
        B = 0.0_rk
    else where
        B = 1.0_rk
    end where

    deallocate(A, B)

end program ex19
