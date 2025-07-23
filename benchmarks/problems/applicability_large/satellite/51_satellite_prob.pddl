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
	thermograph1 - mode
	groundstation1 - direction
	star0 - direction
	planet2 - direction
	star3 - direction
	planet4 - direction
	star5 - direction
)
(:init
	(supports instrument0 infrared0)
	(calibration_target instrument0 groundstation1)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 planet4)
	(supports instrument1 infrared0)
	(calibration_target instrument1 groundstation1)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 groundstation1)
	(supports instrument2 infrared0)
	(supports instrument2 thermograph1)
	(calibration_target instrument2 star0)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star0)
)
(:goal (and
	(have_image planet2 infrared0)
	(have_image star3 infrared0)
	(have_image planet4 thermograph1)
	(have_image star5 infrared0)
))

)
