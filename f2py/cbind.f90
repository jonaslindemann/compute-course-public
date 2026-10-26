module cbind

    use iso_c_binding, only: c_double, c_int
    implicit none

contains

! Scale the n values in x by factor. bind(C) gives the routine a
! C compatible interface with the name scale_array.
subroutine scale_array(x, n, factor) bind(C, name="scale_array")
    integer(c_int), value :: n
    real(c_double), intent(inout) :: x(n)
    real(c_double), value :: factor

    x = x * factor
end subroutine scale_array

end module cbind
