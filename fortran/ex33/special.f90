module special

use utils

interface func
    module procedure ifunc, rfunc
end interface

contains

integer function ifunc(x)

    integer, intent(in) :: x
    ifunc = x * 42

end function ifunc

real(rk) function rfunc(x)

    real(rk), intent(in) :: x
    rfunc = x / 42.0_rk

end function rfunc

end module special
