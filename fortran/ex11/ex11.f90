program ex11

    implicit none

    integer, parameter :: rk = selected_real_kind(15,300)

    integer :: i

    do i = 1, 10
        print*, i
    end do

    print*, '----'

    do i = 2, 30, 4
        print*, i
        ! i = 3
    end do

    print*, '----'

    do i = 1, 1000

        if (i>50) then
            print*, 'i>50, exiting'
            exit
        else if (i<20) then
            print*, 'i<20, cycling'
            cycle
        end if

        print*, i

    end do

end program ex11
