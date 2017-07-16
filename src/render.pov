#include "colors.inc"
camera {orthographic location <722070.0, 11200, 4659465.0> right <7240, 0, 0> up <0.0, 2524.9999999999995, 2525.0> look_at <722070.0, 1200, 4669465.0>}
light_source {<722070.0, 0, 4669465.0> + <5000, 8000, 0> color White }
height_field {png "../PNG/MDT05-0286-H30-LIDAR.png" smooth scale <5761*5, 4000, 4001*5> translate <704400, 0, 4652400> + <-2.5, 0, -2.5>
texture{pigment{image_map{jpeg "../PNOA/pnoa_2012_286_3_1.jpg/pnoa_2012_286_3_1.jpg" once}} scale <7240, 5050, 1> rotate x*90 translate <718450.0, 0, 4666940.0> + <-0.25, 0, -0.25>}
finish { ambient 0.2 diffuse 0.8 roughness 0.05 }}