module beam_model

    use iso_c_binding, only: c_double
    implicit none

    ! Beam parameters, same default values as in beam/beam_model.py

    real(c_double) :: a = 1.0_c_double      ! Distance from left support to load
    real(c_double) :: b = 2.0_c_double      ! Distance from load to right support
    real(c_double) :: P = 1000.0_c_double   ! Point load
    real(c_double) :: E = 2.1e9_c_double    ! Modulus of elasticity
    real(c_double) :: I = 0.1_c_double*0.1_c_double**3/12.0_c_double ! Moment of inertia

contains

! Deflections v(x)
subroutine deflections(x, v)
    real(c_double), intent(in) :: x(:)
    real(c_double), intent(out) :: v(size(x))
    real(c_double) :: L

    L = a + b

    where (x < a)
        v = (P*b*L/(6*E*I))*((1-b**2/L**2)*x - x**3/L**2)
    elsewhere
        v = (P*a/(6*E*I))*(-a**2+(2*L+a**2/L)*x - 3*x**2+x**3/L)
    end where
end subroutine deflections

! Shear forces V(x)
subroutine shear_forces(x, V)
    real(c_double), intent(in) :: x(:)
    real(c_double), intent(out) :: V(size(x))
    real(c_double) :: L

    L = a + b

    where (x < a)
        V = P*b/L
    elsewhere
        V = -P*a/L
    end where
end subroutine shear_forces

! Moments M(x)
subroutine moments(x, M)
    real(c_double), intent(in) :: x(:)
    real(c_double), intent(out) :: M(size(x))
    real(c_double) :: L

    L = a + b

    where (x < a)
        M = -P*b*x/L
    elsewhere
        M = -P*a*(L-x)/L
    end where
end subroutine moments

end module beam_model
