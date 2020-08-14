program particles

    use particle_defs
    use particle_data
    use particle_sim

    implicit none

    type(particle_system) :: psys
    integer(rk) :: i
    
    ! TODO: Allocate and initialise particle system    

    call write_particle_sizes(psys)
    
    ! TODO: Perform particle simulation 
    ! do ...
    !    call check_collision(psys)
    !    ...
    !    call write_particle_positions(psys)
    ! end 

    call print_particle_system(psys)

    ! TODO: Deallocate particle system

end program particles