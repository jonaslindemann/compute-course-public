subroutine simple(a,b,c)
    use iso_c_binding, only: c_double

    real(c_double), intent(in) :: a, b
    real(c_double), intent(out) :: c

    c = a + b

end subroutine simple
