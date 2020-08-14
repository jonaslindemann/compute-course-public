module particle_data

    use particle_defs
    use particle_utils

    implicit none

    type particle_system
        integer(ik) :: n_particles
        real(rk) :: v0
        real(rk) :: rmin
        real(rk) :: rmax
        real(rk) :: dt
        real(rk), allocatable :: pos(:,:)
        real(rk), allocatable :: vel(:,:)
        real(rk), allocatable :: r(:)
    end type particle_system

contains

    subroutine allocate_particle_system(psys, n)
        
        ! TODO:
        ! Allocate the pos, vel and r arrays
        ! Initialise the other variables in the particle system

        integer(ik), intent(in) :: n
        type(particle_system) :: psys

        
    end subroutine allocate_particle_system

    subroutine deallocate_particle_system(psys)
        
        ! TODO:
        ! Deallocate the pos, vel and r arrays
        ! Set the n_particles variable in psys to -1

        type(particle_system) :: psys

    end subroutine deallocate_particle_system

    subroutine init_particle_system(psys)
        
        ! TODO:
        ! Set the initial values in the particle system
        ! 
        ! Random number generator can be initialised with 
        !
        !     call init_random_seed()
        !
        ! Random number can be generated using the following subroutine
        !
        !     call random_number(v)
        !
        ! You can pass an entire array to this functionas well.

        type(particle_system), intent(inout) :: psys
        
    end subroutine init_particle_system

    subroutine print_particle_system(psys)
        
        ! Pretty print the particle system

        type(particle_system), intent(inout) :: psys
        integer(ik) :: i

        print *, 'Max particle x coord = ', maxval(psys % pos(:, 1))
        print *, 'Min particle x coord = ', minval(psys % pos(:, 1))
        print *, 'Max particle y coord = ', maxval(psys % pos(:, 2))
        print *, 'Min particle y coord = ', minval(psys % pos(:, 2))

        !write(*,*) '----- Particle postion - velocity -----------------------------'
        !do i=1,psys%n_particles
        !   write(*,'(2F12.5,A5,2F12.5)') psys%pos(i,:), '-', psys%vel(i,:)
        !end do

        !write(*,*) '----- Particle size -------------------------------------------'
        !do i=1,psys%n_particles
        !        write(*,'(F12.5)') psys%r(i)
        !end do


    end subroutine print_particle_system

    subroutine write_particle_sizes(psys)
        
        ! Append particle sizes to particle state file (particle.state)

        type(particle_system), intent(inout) :: psys
        integer(ik) :: i

        open(unit = 15, file = 'particle.state', access = 'APPEND')
        write(15, '(I10)') psys % n_particles
        do i = 1, psys % n_particles
            write(15, '(2F12.5)') psys % r(i)
        end do
        close(unit = 15)

    end subroutine write_particle_sizes

    subroutine write_particle_positions(psys)
        
        ! Append current position to particle state file (particle.state)

        type(particle_system), intent(inout) :: psys
        integer(ik) :: i

        open(unit = 15, file = 'particle.state', access = 'APPEND')
        write(15, '(I10)') psys % n_particles
        do i = 1, psys % n_particles
            write(15, '(2F12.5)') psys % pos(i,:)
        end do
        close(unit = 15)

    end subroutine write_particle_positions

end module particle_data