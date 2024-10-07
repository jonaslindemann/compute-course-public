module filters 
    use iso_c_binding

    implicit none
  
  contains
  
  subroutine mean_filter(image, kernel_size, filtered_image)
    use, intrinsic :: iso_c_binding, only: c_double
    implicit none
    real(c_double), intent(in) :: image(:,:)
    integer, intent(in) :: kernel_size
    real(c_double), intent(inout) :: filtered_image(:,:)
    integer :: y, x, i, j, height, width, y_start, y_end, x_start, x_end
    real(c_double) :: sum_value, divisor
    integer :: window_size
  
    height = size(image, 1)
    width = size(image, 2)
  
    ! Precompute divisor
    divisor = 1.0_c_double / (kernel_size * kernel_size)
  
     !$OMP PARALLEL DO PRIVATE(x, i, j, sum_value, y_start, y_end, x_start, x_end, window_size) SCHEDULE(static)
    do y = 1, height
      do x = 1, width
        ! Calculate window boundaries
        y_start = max(1, y - kernel_size/2)
        y_end = min(height, y + kernel_size/2)
        x_start = max(1, x - kernel_size/2)
        x_end = min(width, x + kernel_size/2)
  
        ! Calculate the sum value of the window
        sum_value = 0.0_c_double
        window_size = 0
        
        do j = y_start, y_end
          do i = x_start, x_end
            sum_value = sum_value + image(j, i)
            window_size = window_size + 1
          end do
        end do
  
        ! Assign the mean value to the corresponding pixel in the filtered image
        filtered_image(y, x) = sum_value / window_size
      end do
    end do
    !$OMP END PARALLEL DO
  
  end subroutine mean_filter  
  end module filters