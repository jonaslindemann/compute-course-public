module utils

implicit none

integer, parameter :: rk = selected_real_kind(15,300)

contains

subroutine printMatrix(A, name)

    real(rk), intent(in) :: A(:,:)
    character(*), intent(in), optional :: name
    integer :: rows, cols, slen
    integer :: i, j
    character(255) :: fmt
    character(255) :: sfmt

    rows = size(A,1)
    cols = size(A,2)
    slen = len_trim(name)

    if (slen<10) then
        write(sfmt, '(A,I1,A)') '(TL1,A,A',slen,',A,I3,A,I3,A)'
    else if (slen<100) then
        write(sfmt, '(A,I2,A)') '(TL1,A,A',slen,',A,I3,A,I3,A)'
    else
        write(sfmt, '(A,I3,A)') '(TL1,A,A',slen,',A,I3,A,I3,A)'
    end if

    if (cols<10) then
        write(fmt, '(A,I1,A)') '(', cols, 'G10.3)'
    else if (cols<100) then
        write(fmt, '(A,I2,A)') '(', cols, 'G10.3)'
    else
        write(fmt, '(A,I3,A)') '(', cols, 'G10.3)'
    end if

    write(*,'(TL1,A)') '-------------------------------------'
    if (present(name)) then
        write(*,sfmt) 'Matrix ',trim(name),' (',rows, ' x ', cols, ')'
    else
        write(*,'(TL1,A,I3,A,I3,A)') 'Matrix (',rows, ' x ', cols, ')'
    end if
    write(*,'(TL1,A)') '-------------------------------------'


    do i=1,rows
        write(*,fmt) (A(i,j), j=1,cols)
    end do

    write(*,'(TL1,A)') '-------------------------------------'

end subroutine printMatrix

subroutine printVector(A, name)

    real(rk), intent(in) :: a(:)
    character(*), intent(in), optional :: name
    integer :: cols, slen
    integer :: i
    character(255) :: fmt
    character(255) :: sfmt

    cols = size(A,1)
    slen = len_trim(name)

    if (slen<10) then
        write(sfmt, '(A,I1,A)') '(TL1,A,A',slen,',A,I3,A)'
    else if (slen<100) then
        write(sfmt, '(A,I2,A)') '(TL1,A,A',slen,',A,I3,A)'
    else
        write(sfmt, '(A,I3,A)') '(TL1,A,A',slen,',A,I3,A)'
    end if

    if (cols<10) then
        write(fmt, '(A,I1,A)') '(', cols, 'G10.3)'
    else if (cols<100) then
        write(fmt, '(A,I2,A)') '(', cols, 'G10.3)'
    else
        write(fmt, '(A,I3,A)') '(', cols, 'G10.3)'
    end if

    write(*,'(TL1,A)') '-------------------------------------'
    if (present(name)) then
        write(*,sfmt) 'Vector ',trim(name),' (',cols,')'
    else
        write(*,'(TL1,A,I3,A)') 'Vector (',cols,')'
    end if
    write(*,'(TL1,A)') '-------------------------------------'


    write(*,fmt) (a(i), i=1,cols)

    write(*,'(TL1,A)') '-------------------------------------'

end subroutine printVector

subroutine randMat(A, randMin, randMax)

    real(rk), intent(inout) :: A(:,:)
    real(rk), intent(in) :: randMin, randMax

    call random_number(A)

    !    min ---- max

    A = randMin + (randMax-randMin) * A

end subroutine randMat


subroutine initRand()
    integer :: values(1:8), k
    integer, dimension(:), allocatable :: seed
    real(8) :: r
    call date_and_time(values=values)
    call random_seed(size=k)
    allocate(seed(1:k))
    seed(:) = values(8)
    call random_seed(put=seed)
end subroutine

end module utils
