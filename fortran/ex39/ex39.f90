program allocatable_function

    use utils

    implicit none

    type particles_type
        real(rk), allocatable :: pos(:,:)
        real(rk), allocatable :: vel(:,:)
        real(rk), allocatable :: mass(:)
    end type particles_type

    type(particles_type) :: particles

    call initParticles(particles, 1000)

    print*, shape(particles % pos)
    print*, shape(particles % vel)
    print*, shape(particles % mass)

    call deallocateParticles(particles)

contains

subroutine initParticles(particles, n)

    type(particles_type), intent(inout) :: particles
    integer, intent(in) :: n

    allocate(particles % pos(3,n))
    allocate(particles % vel(3,n))
    allocate(particles % mass(n))

end subroutine initParticles

subroutine deallocateParticles(particles)

    type(particles_type), intent(inout) :: particles

    deallocate(particles % pos)
    deallocate(particles % vel)
    deallocate(particles % mass)

end subroutine deallocateParticles

end program allocatable_function
