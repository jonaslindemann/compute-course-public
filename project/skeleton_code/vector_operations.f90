module vector_operations

	use particle_defs
	
	implicit none

	type vector
		real(8) :: c(2)
	end type vector
	
	interface operator(+)
		module procedure vector_plus_vector
	end interface

	interface operator(-)
		module procedure vector_minus_vector
	end interface
	
	interface operator(.dot.) 
		module procedure vector_dot_vector
	end interface

contains

subroutine zero(v)
	type(vector), intent(inout) :: v
	
	v % c = 0.0_rk
	
end subroutine zero

function len(v) result (l)
	type(vector), intent(in) :: v
	real(rk) :: l
	
	l = sqrt(v % c(1)**2 + v % c(2)**2)

end function len

subroutine inormalize(v)
	type(vector), intent(inout) :: v
	
	v % c = v % c / len(v)
	
end subroutine inormalize

function normalize(v) result (vout)
	type(vector), intent(in) :: v
	type(vector) :: vout
	
	vout % c = v % c / len(v)
	
end function normalize

function vector_dot_vector(v1, v2) result (dot)
  type(vector), intent(in) :: v1, v2
  real(8) :: dot
  
  dot = dot_product(v1 % c, v2 % c)
  
end function vector_dot_vector

type(vector) function vector_plus_vector(v1, v2)

	type(vector), intent(in) :: v1, v2
	vector_plus_vector % c = v1 % c + v2 % c
	
end function vector_plus_vector

type(vector) function vector_minus_vector(v1, v2)

	type(vector), intent(in) :: v1, v2
	vector_minus_vector % c = v1 % c - v2 % c
	
end function vector_minus_vector

end module vector_operations