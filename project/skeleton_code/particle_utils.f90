module particle_utils

	use particle_defs

	implicit none

contains

subroutine init_random_seed

	integer :: values(1:8), k
	integer, dimension(:), allocatable :: seed
	real(8) :: r

	call date_and_time(values=values)

	call random_seed(size=k)
	allocate(seed(1:k))
	seed(:) = values(8)
	call random_seed(put=seed)

end subroutine init_random_seed

end module particle_utils