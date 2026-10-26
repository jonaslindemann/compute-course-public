! C = A * B using the Fortran intrinsic matmul
subroutine fortran_matmul(A, r, s, B, t, C)
    use iso_c_binding, only: c_double

    integer :: r, s, t
    !f2py intent(hide) :: r, s, t
    real(c_double), intent(in) :: A(r,s)
    real(c_double), intent(in) :: B(s,t)
    real(c_double), intent(out) :: C(r,t)

    C = matmul(A,B)
end subroutine fortran_matmul
