program c_interop

    use iso_c_binding

    implicit none

    real(c_double) :: c

    interface
        subroutine myfunc(a, b, c) bind(C, name="myfunc")
          use iso_c_binding
          integer(c_int), value :: a
          real(c_double), value :: b
          real(c_double) :: c
        end subroutine myfunc
    end interface

    c = 42.0_c_double

    call myfunc(1, 2.0_c_double, c)

end program c_interop
