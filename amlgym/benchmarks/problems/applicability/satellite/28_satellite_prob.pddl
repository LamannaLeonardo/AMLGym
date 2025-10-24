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
	star1 - direction
	star0 - direction
	planet2 - direction
	phenomenon3 - direction
	planet4 - direction
	star5 - direction
)
(:init
	(supports instrument0 thermograph0)
	(calibration_target instrument0 star0)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 star1)
	(supports instrument1 thermograph1)
	(supports instrument1 thermograph0)
	(calibration_target instrument1 star0)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star1)
	(supports instrument2 thermograph0)
	(calibration_target instrument2 star0)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star5)
)
(:goal (and
	(pointing satellite1 phenomenon3)
	(have_image planet2 thermograph1)
	(have_image phenomenon3 thermograph0)
	(have_image planet4 thermograph1)
	(have_image star5 thermograph1)
))

)
