module particle_sim

    use particle_defs
    use particle_data
    use vector_operations

    implicit none

contains

    subroutine update_particle_system(psys, dtin)
        
        ! Update positions of particle system
        
        type(particle_system), intent(inout) :: psys
        real(rk), intent(in), optional :: dtin
        real(rk) :: dt

        if (present(dtin)) then
            dt = dtin
        else
            dt = psys % rmin/(3.0_rk * psys % v0)
        end if

        ! Perform update here

    end subroutine update_particle_system

    subroutine check_boundary(psys)
        
        ! Check for boundary collision
        
        type(particle_system), intent(inout) :: psys
        integer(ik) :: i

    end subroutine check_boundary

    subroutine check_collision(psys)
        
        ! Check for particle collisions and update if neccesary
        
        type(particle_system), intent(inout) :: psys
        
    end subroutine check_collision

end module particle_sim
