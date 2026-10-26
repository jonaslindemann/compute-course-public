module stats
    use iso_c_binding, only: c_double
    implicit none

contains

! Scale x to zero mean and unit standard deviation
subroutine normalize(x, y)
    real(c_double), intent(in) :: x(:)
    real(c_double), intent(out) :: y(size(x))
    real(c_double) :: mean, std

    mean = sum(x) / size(x)
    std = sqrt(sum((x - mean)**2) / size(x))
    y = (x - mean) / std
end subroutine normalize

! Mean value of each column of A
subroutine column_means(A, means)
    real(c_double), intent(in) :: A(:,:)
    real(c_double), intent(out) :: means(size(A,2))

    means = sum(A, dim=1) / size(A,1)
end subroutine column_means

end module stats
