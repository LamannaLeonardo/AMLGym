(define (problem strips_sat_x_1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	satellite1 - satellite
	instrument1 - instrument
	satellite2 - satellite
	instrument2 - instrument
	image1 - mode
	thermograph0 - mode
	groundstation0 - direction
	groundstation1 - direction
	star2 - direction
	star3 - direction
	phenomenon4 - direction
	planet5 - direction
)
(:init
	(supports instrument0 thermograph0)
	(calibration_target instrument0 groundstation1)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 planet5)
	(supports instrument1 image1)
	(calibration_target instrument1 groundstation0)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 groundstation1)
	(supports instrument2 image1)
	(supports instrument2 thermograph0)
	(calibration_target instrument2 groundstation1)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 planet5)
)
(:goal (and
	(pointing satellite1 groundstation0)
	(pointing satellite2 phenomenon4)
	(have_image star2 image1)
	(have_image star3 thermograph0)
	(have_image phenomenon4 image1)
	(have_image planet5 thermograph0)
))

)
