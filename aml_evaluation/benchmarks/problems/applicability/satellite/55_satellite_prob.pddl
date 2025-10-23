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
	groundstation1 - direction
	star0 - direction
	phenomenon2 - direction
	star3 - direction
	phenomenon4 - direction
	phenomenon5 - direction
)
(:init
	(supports instrument0 thermograph0)
	(supports instrument0 image1)
	(calibration_target instrument0 groundstation1)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 phenomenon2)
	(supports instrument1 thermograph0)
	(supports instrument1 image1)
	(calibration_target instrument1 star0)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 groundstation1)
	(supports instrument2 image1)
	(supports instrument2 thermograph0)
	(calibration_target instrument2 star0)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star3)
)
(:goal (and
	(pointing satellite0 star3)
	(pointing satellite2 groundstation1)
	(have_image phenomenon2 thermograph0)
	(have_image star3 thermograph0)
	(have_image phenomenon4 thermograph0)
	(have_image phenomenon5 image1)
))

)
