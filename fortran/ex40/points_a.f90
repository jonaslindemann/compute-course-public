submodule (points) points_a
contains

real module function point_dist(a,b) result(dist)
        type(point), intent(in) :: a, b
        real :: dist
        dist = sqrt((a%x-b%x)**2+(a%y-b%y)**2)
end function point_dist

end submodule points_a
