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
	thermograph0 - mode
	groundstation0 - direction
	groundstation1 - direction
	planet2 - direction
	phenomenon3 - direction
	star4 - direction
	star5 - direction
)
(:init
	(supports instrument0 thermograph1)
	(supports instrument0 thermograph0)
	(calibration_target instrument0 groundstation0)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 groundstation1)
	(supports instrument1 thermograph1)
	(supports instrument1 thermograph0)
	(calibration_target instrument1 groundstation1)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star4)
	(supports instrument2 thermograph0)
	(supports instrument2 thermograph1)
	(calibration_target instrument2 groundstation1)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 planet2)
)
(:goal (and
	(pointing satellite0 groundstation0)
	(have_image planet2 thermograph1)
	(have_image phenomenon3 thermograph1)
	(have_image star4 thermograph0)
	(have_image star5 thermograph1)
))

)
