(define (problem strips_sat_x_1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	satellite1 - satellite
	instrument1 - instrument
	satellite2 - satellite
	instrument2 - instrument
	infrared0 - mode
	image1 - mode
	groundstation1 - direction
	groundstation0 - direction
	phenomenon2 - direction
	phenomenon3 - direction
	planet4 - direction
	phenomenon5 - direction
)
(:init
	(supports instrument0 infrared0)
	(supports instrument0 image1)
	(calibration_target instrument0 groundstation1)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 phenomenon3)
	(supports instrument1 image1)
	(calibration_target instrument1 groundstation0)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 planet4)
	(supports instrument2 image1)
	(supports instrument2 infrared0)
	(calibration_target instrument2 groundstation0)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 phenomenon5)
)
(:goal (and
	(pointing satellite0 phenomenon5)
	(have_image phenomenon2 image1)
	(have_image phenomenon3 image1)
	(have_image planet4 image1)
	(have_image phenomenon5 image1)
))

)
