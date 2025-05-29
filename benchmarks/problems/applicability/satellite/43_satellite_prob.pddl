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
	star2 - direction
	phenomenon3 - direction
	star4 - direction
	phenomenon5 - direction
)
(:init
	(supports instrument0 image1)
	(supports instrument0 infrared0)
	(calibration_target instrument0 groundstation1)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 phenomenon5)
	(supports instrument1 image1)
	(supports instrument1 infrared0)
	(calibration_target instrument1 groundstation0)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star2)
	(supports instrument2 image1)
	(calibration_target instrument2 groundstation0)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 groundstation0)
)
(:goal (and
	(pointing satellite0 phenomenon3)
	(pointing satellite1 phenomenon5)
	(have_image star2 infrared0)
	(have_image phenomenon3 image1)
	(have_image star4 infrared0)
	(have_image phenomenon5 image1)
))

)
