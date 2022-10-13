module beam_model

    implicit none

    integer, parameter :: rk = selected_real_kind(15,300)

    real(rk) :: a
    real(rk) :: b
    real(rk) :: L
    real(rk) :: P
    real(rk) :: E
    real(rk) :: I

contains

subroutine init() 

    a = 1.0
    b = 2.0
    L = a + b
    P = 1000
    E = 2.1e9
    I = 0.1*0.1**4/12.0

end subroutine

subroutine set_params(a_val, b_val, P_val, E_val, I_val)

    real(rk), intent(in) :: a_val
    real(rk), intent(in) :: b_val
    real(rk), intent(in) :: P_val
    real(rk), intent(in) :: E_val
    real(rk), intent(in) :: I_val

    a = a_val
    b = b_val
    L = a + b
    P = P_val
    E = E_val
    I = I_val

end subroutine set_params
    
subroutine get_params(a_val, b_val, P_val, E_val, I_val)

    real(rk), intent(out) :: a_val
    real(rk), intent(out) :: b_val
    real(rk), intent(out) :: P_val
    real(rk), intent(out) :: E_val
    real(rk), intent(out) :: I_val

    a_val = a
    b_val = b
    P_val = P
    E_val = E
    I_val = I

end subroutine get_params

subroutine deflections(x, result)

    real(rk), intent(in) :: x
    real(rk), intent(out) :: result
    
    if (x < a) then 
        result = (P*b*L/(6*E*I))*((1-b**2/L**2)*x - x**3/L**2)
    else
        result = (P*a/(6*E*I))*(-a**2+(2*L+a**2/L)*x - 3*x**2+x**3/L)
    end if

end subroutine 

subroutine shear_forces(x, result)
    
    real(rk), intent(in) :: x
    real(rk), intent(out) :: result

    if (x < a) then 
        result = P*b/L
    else
        result = -P*a/L
    end if

end subroutine 

subroutine moments(x, result)

    real(rk), intent(in) :: x
    real(rk), intent(out) :: result

    print*, P, b, x, L

    if (x < a) then 
        result = -P*b*x/L
    else
        result = -P*a*(L-x)/L
    end if

end subroutine

end module beam_model

