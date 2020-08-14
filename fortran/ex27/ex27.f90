program ex26

    use utils
    use iso_fortran_env

    implicit none

    real(rk) :: a(5)
    integer :: i

    read(*,*) a(1), a(2), a(3), a(4), a(5)
    read(input_unit, *) (a(i), i=1,5)
    write(*,*) (a(i), i=1,5)
    write(output_unit, *) (a(i), i=1,5)

    call printVector(a, 'a')

end program ex26
