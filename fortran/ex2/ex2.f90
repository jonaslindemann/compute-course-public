program ex2

    use iso_fortran_env

    implicit none

    integer, parameter :: rk = selected_real_kind(15,300)
    integer, parameter :: ik = selected_real_kind(6)

    real(kind=rk) :: x
    real(rk) :: y
    real(real64) :: z

    integer(kind=ik) :: i
    integer(ik) :: j
    integer(int32) :: k

    print*, rk
    print*, ik
    print*, real64
    print*, int32

end program ex2
