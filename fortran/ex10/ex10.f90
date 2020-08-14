program ex10

    use utils

    implicit none

    real(rk) :: r
    integer  :: v

    call initRand()
    call randVal(r, 0.0_rk, 1.0_rk)

    v = nint(50.0_rk - 100.0_rk * r)

    print*, v

    select case (v)
    case (:-20)
        print*, "v <= -1"
    case (0)
        print*, "v == 0"
    case (20:)
        print*, "v >=1"
    case default
        print*, "v is in the default range"
    end select

end program ex10
