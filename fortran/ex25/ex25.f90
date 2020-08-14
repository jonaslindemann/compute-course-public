program ex25

    use utils

    implicit none

    real(rk) :: A(10,10)
    logical  :: B(10,10)
    real(rk) :: v1(3)
    real(rk) :: v2(3)
    real(rk) :: dp

    call initRand()
    call randMat(A, -10.0_rk, 10.0_rk)

    B = .true.

    if (all(B) .eqv. .true.) then
        print*, 'All elements are true.'
    else
        print*, 'Not all elements are true'
    end if

    B = .false.

    if (any(B) .eqv. .true.) then
        print*, 'Some of the elements in B are true'
    else
        print*, 'None of the elements in B are true'
    end if

    B(5,5) = .true.

    if (any(B) .eqv. .true.) then
        print*, 'Some of the elements in B are true'
    else
        print*, 'None of the elements in B are true'
    end if

    print*, 'Max value in A = ', maxval(A)
    print*, 'Max value in A = ', minval(A)
    print*, 'Product of A   = ', product(A)
    print*, 'Sum of A       = ', sum(A)

end program ex25
