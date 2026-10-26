! Scale an array in place and return it
subroutine scale(x, n, factor)
    use iso_c_binding, only: c_double

    integer :: n
    real(c_double), intent(inout) :: x(n)
    real(c_double), intent(in) :: factor
    !f2py intent(in,out) :: x

    x = x * factor
end subroutine scale

! Add one to every element of an integer array
subroutine count_up(counts, n)
    use iso_c_binding, only: c_int

    integer :: n
    integer(c_int), intent(inout) :: counts(n)

    counts = counts + 1
end subroutine count_up
