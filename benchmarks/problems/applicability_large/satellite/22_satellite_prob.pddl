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
	image0 - mode
	star1 - direction
	star2 - direction
	star0 - direction
	star3 - direction
	planet4 - direction
	star5 - direction
	phenomenon6 - direction
	star7 - direction
)
(:init
	(supports instrument0 image0)
	(supports instrument0 thermograph1)
	(calibration_target instrument0 star0)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 star1)
	(supports instrument1 image0)
	(calibration_target instrument1 star2)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star0)
	(supports instrument2 thermograph1)
	(calibration_target instrument2 star0)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star5)
	(supports instrument3 thermograph1)
	(supports instrument3 image0)
	(calibration_target instrument3 star0)
	(on_board instrument3 satellite3)
	(power_avail satellite3)
	(pointing satellite3 planet4)
)
(:goal (and
	(pointing satellite0 star1)
	(pointing satellite1 star1)
	(have_image star3 thermograph1)
	(have_image planet4 thermograph1)
	(have_image star5 thermograph1)
	(have_image phenomenon6 thermograph1)
	(have_image star7 thermograph1)
))

)
