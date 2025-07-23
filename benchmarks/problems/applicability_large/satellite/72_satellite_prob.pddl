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
	image1 - mode
	star1 - direction
	star0 - direction
	groundstation2 - direction
	planet3 - direction
	planet4 - direction
	star5 - direction
	planet6 - direction
	phenomenon7 - direction
)
(:init
	(supports instrument0 thermograph0)
	(calibration_target instrument0 star0)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 star0)
	(supports instrument1 thermograph0)
	(supports instrument1 image1)
	(calibration_target instrument1 groundstation2)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 planet6)
	(supports instrument2 image1)
	(calibration_target instrument2 star0)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 planet3)
	(supports instrument3 image1)
	(calibration_target instrument3 groundstation2)
	(on_board instrument3 satellite3)
	(power_avail satellite3)
	(pointing satellite3 groundstation2)
)
(:goal (and
	(pointing satellite0 phenomenon7)
	(pointing satellite1 star5)
	(have_image planet3 thermograph0)
	(have_image planet4 thermograph0)
	(have_image star5 image1)
	(have_image planet6 thermograph0)
	(have_image phenomenon7 thermograph0)
))

)
