module functions

    use utils

    implicit none

contains

real(rk) function myfunc1(x)

    real(rk), intent(in) :: x

    myfunc1 = sin(x)

end function myfunc1

real(rk) function myfunc2(x)

    real(rk), intent(in) :: x

    myfunc2 = sqrt(x)

end function myfunc2

end module functions
