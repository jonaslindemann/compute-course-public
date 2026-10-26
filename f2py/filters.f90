module filters

    use iso_c_binding, only: c_double
    !$ use omp_lib
    implicit none

contains

! Mean value of the kernel_size x kernel_size window around each pixel
subroutine mean_filter(image, kernel_size, filtered_image)
    real(c_double), intent(in) :: image(:,:)
    integer, intent(in) :: kernel_size
    real(c_double), intent(inout) :: filtered_image(:,:)
    integer :: row, col, i, j, rows, cols, half
    integer :: row_start, row_end, col_start, col_end
    real(c_double) :: sum_value

    rows = size(image, 1)
    cols = size(image, 2)
    half = kernel_size/2

    ! The columns are divided between the threads. The innermost loops
    ! run over the rows, which are stored after each other in memory.

    !$omp parallel do private(row, i, j, row_start, row_end, col_start, col_end, sum_value)
    do col = 1, cols
        col_start = max(1, col - half)
        col_end = min(cols, col + half)
        do row = 1, rows
            row_start = max(1, row - half)
            row_end = min(rows, row + half)

            sum_value = 0.0_c_double
            do j = col_start, col_end
                do i = row_start, row_end
                    sum_value = sum_value + image(i, j)
                end do
            end do

            filtered_image(row, col) = sum_value / ((row_end - row_start + 1)*(col_end - col_start + 1))
        end do
    end do
    !$omp end parallel do

end subroutine mean_filter

! Set the number of OpenMP threads (does nothing without OpenMP)
subroutine set_num_threads(n)
    integer, intent(in) :: n

    !$ call omp_set_num_threads(n)
end subroutine set_num_threads

! Maximum number of OpenMP threads (1 without OpenMP)
subroutine get_max_threads(n)
    integer, intent(out) :: n

    n = 1
    !$ n = omp_get_max_threads()
end subroutine get_max_threads

end module filters
