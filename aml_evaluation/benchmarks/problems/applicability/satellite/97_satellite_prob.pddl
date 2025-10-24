(define (problem strips_sat_x_1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	satellite1 - satellite
	instrument1 - instrument
	satellite2 - satellite
	instrument2 - instrument
	infrared1 - mode
	image0 - mode
	star0 - direction
	groundstation1 - direction
	phenomenon2 - direction
	star3 - direction
	star4 - direction
	phenomenon5 - direction
)
(:init
	(supports instrument0 infrared1)
	(supports instrument0 image0)
	(calibration_target instrument0 star0)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 phenomenon2)
	(supports instrument1 infrared1)
	(calibration_target instrument1 groundstation1)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 phenomenon5)
	(supports instrument2 infrared1)
	(supports instrument2 image0)
	(calibration_target instrument2 groundstation1)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 phenomenon5)
)
(:goal (and
	(pointing satellite0 star4)
	(have_image phenomenon2 image0)
	(have_image star3 infrared1)
	(have_image star4 image0)
	(have_image phenomenon5 infrared1)
))

)
