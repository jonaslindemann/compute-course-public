module matrix

    use iso_c_binding, only: c_double

contains

! A[r,s] * B[s,t] = C[r,t]
subroutine matrix_multiply(A,r,s,B,t,C)
    integer :: r, s, t
    real(c_double), intent(in) :: A(r,s)
    real(c_double), intent(in) :: B(s,t)
    real(c_double), intent(out) :: C(r,t)

    C = matmul(A,B)
end subroutine matrix_multiply

! A[r,s] * B[s,t] = C[r,t]
subroutine matrix_multiply2(A,r,s,B,t,C)
    integer :: r, s, t
    real(c_double), intent(in) :: A(r,s)
    real(c_double), intent(in) :: B(s,t)
    real(c_double), intent(inout) :: C(r,t)

    C = matmul(A,B)
end subroutine matrix_multiply2

end module matrix
