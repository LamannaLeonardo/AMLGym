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
	thermograph0 - mode
	thermograph1 - mode
	star0 - direction
	groundstation2 - direction
	groundstation1 - direction
	star3 - direction
	phenomenon4 - direction
	planet5 - direction
	star6 - direction
	planet7 - direction
)
(:init
	(supports instrument0 thermograph0)
	(supports instrument0 thermograph1)
	(calibration_target instrument0 groundstation1)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 star6)
	(supports instrument1 thermograph1)
	(calibration_target instrument1 star0)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 groundstation1)
	(supports instrument2 thermograph1)
	(supports instrument2 thermograph0)
	(calibration_target instrument2 groundstation2)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 planet7)
	(supports instrument3 thermograph1)
	(calibration_target instrument3 groundstation1)
	(on_board instrument3 satellite3)
	(power_avail satellite3)
	(pointing satellite3 planet7)
)
(:goal (and
	(pointing satellite2 star0)
	(have_image star3 thermograph1)
	(have_image phenomenon4 thermograph1)
	(have_image planet5 thermograph0)
	(have_image star6 thermograph1)
	(have_image planet7 thermograph0)
))

)
