program ex43

    implicit none

    character(255) :: homedir
    character(255) :: argument
    integer :: argc

    call get_environment_variable('HOME', homedir)

    print*, trim(homedir)

    argc = command_argument_count()
    print*, argc

    call get_command_argument(0, argument)

    print*, trim(argument)

end program ex43
