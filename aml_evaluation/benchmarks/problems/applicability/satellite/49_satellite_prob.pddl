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
	infrared0 - mode
	star1 - direction
	star0 - direction
	star2 - direction
	star3 - direction
	star4 - direction
	star5 - direction
)
(:init
	(supports instrument0 infrared1)
	(supports instrument0 infrared0)
	(calibration_target instrument0 star0)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 star5)
	(supports instrument1 infrared0)
	(supports instrument1 infrared1)
	(calibration_target instrument1 star1)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star4)
	(supports instrument2 infrared1)
	(supports instrument2 infrared0)
	(calibration_target instrument2 star0)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star2)
)
(:goal (and
	(pointing satellite2 star5)
	(have_image star2 infrared0)
	(have_image star3 infrared0)
	(have_image star4 infrared1)
	(have_image star5 infrared1)
))

)
