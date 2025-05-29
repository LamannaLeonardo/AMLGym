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
	infrared0 - mode
	thermograph1 - mode
	groundstation2 - direction
	star0 - direction
	star1 - direction
	phenomenon3 - direction
	planet4 - direction
	phenomenon5 - direction
	star6 - direction
	star7 - direction
)
(:init
	(supports instrument0 infrared0)
	(supports instrument0 thermograph1)
	(calibration_target instrument0 star0)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 groundstation2)
	(supports instrument1 infrared0)
	(calibration_target instrument1 groundstation2)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 planet4)
	(supports instrument2 infrared0)
	(supports instrument2 thermograph1)
	(calibration_target instrument2 star0)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star0)
	(supports instrument3 thermograph1)
	(supports instrument3 infrared0)
	(calibration_target instrument3 star1)
	(on_board instrument3 satellite3)
	(power_avail satellite3)
	(pointing satellite3 phenomenon3)
)
(:goal (and
	(have_image phenomenon3 thermograph1)
	(have_image planet4 thermograph1)
	(have_image phenomenon5 thermograph1)
	(have_image star6 infrared0)
	(have_image star7 infrared0)
))

)
