(define (problem strips_sat_x_1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	satellite1 - satellite
	instrument1 - instrument
	satellite2 - satellite
	instrument2 - instrument
	satellite3 - satellite
	instrument3 - instrument
	thermograph1 - mode
	infrared0 - mode
	star1 - direction
	star0 - direction
	star2 - direction
	phenomenon3 - direction
	star4 - direction
	star5 - direction
	star6 - direction
	star7 - direction
)
(:init
	(supports instrument0 infrared0)
	(supports instrument0 thermograph1)
	(calibration_target instrument0 star2)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 star4)
	(supports instrument1 thermograph1)
	(calibration_target instrument1 star0)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star1)
	(supports instrument2 infrared0)
	(calibration_target instrument2 star2)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star1)
	(supports instrument3 infrared0)
	(calibration_target instrument3 star2)
	(on_board instrument3 satellite3)
	(power_avail satellite3)
	(pointing satellite3 star7)
)
(:goal (and
	(pointing satellite0 star5)
	(pointing satellite1 star2)
	(have_image phenomenon3 thermograph1)
	(have_image star4 thermograph1)
	(have_image star5 infrared0)
	(have_image star6 infrared0)
	(have_image star7 thermograph1)
))

)
