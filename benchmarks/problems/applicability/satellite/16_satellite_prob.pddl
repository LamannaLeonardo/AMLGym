(define (problem strips_sat_x_1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	satellite1 - satellite
	instrument1 - instrument
	satellite2 - satellite
	instrument2 - instrument
	thermograph1 - mode
	infrared0 - mode
	star1 - direction
	star0 - direction
	planet2 - direction
	planet3 - direction
	star4 - direction
	planet5 - direction
)
(:init
	(supports instrument0 infrared0)
	(supports instrument0 thermograph1)
	(calibration_target instrument0 star1)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 planet5)
	(supports instrument1 thermograph1)
	(supports instrument1 infrared0)
	(calibration_target instrument1 star1)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star0)
	(supports instrument2 infrared0)
	(supports instrument2 thermograph1)
	(calibration_target instrument2 star0)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 planet3)
)
(:goal (and
	(pointing satellite1 planet3)
	(pointing satellite2 star4)
	(have_image planet2 infrared0)
	(have_image planet3 infrared0)
	(have_image star4 thermograph1)
	(have_image planet5 infrared0)
))

)
