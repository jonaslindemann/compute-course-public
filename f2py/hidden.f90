! A[r,s] * B[s,t] = C[r,t]
subroutine matrix_multiply3(A,r,s,B,t,C)
    use iso_c_binding, only: c_double

    integer :: r, s, t
    !f2py intent(hide) :: r, s, t
    real(c_double), intent(in) :: A(r,s)
    real(c_double), intent(in) :: B(s,t)
    real(c_double), intent(out) :: C(r,t)

    C = matmul(A,B)
end subroutine matrix_multiply3

! n evenly spaced values between x0 and x1
subroutine linspace(x0, x1, n, x)
    use iso_c_binding, only: c_double

    real(c_double), intent(in) :: x0, x1
    integer, intent(in) :: n
    !f2py check(n > 1) :: n
    real(c_double), intent(out) :: x(n)
    integer :: i

    do i = 1, n
        x(i) = x0 + (x1 - x0) * (i - 1) / (n - 1)
    end do
end subroutine linspace
