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
	image2 - mode
	thermograph1 - mode
	spectrograph0 - mode
	star0 - direction
	groundstation2 - direction
	star1 - direction
	planet3 - direction
	phenomenon4 - direction
	star5 - direction
	phenomenon6 - direction
	star7 - direction
)
(:init
	(supports instrument0 image2)
	(calibration_target instrument0 groundstation2)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 star7)
	(supports instrument1 image2)
	(supports instrument1 spectrograph0)
	(calibration_target instrument1 groundstation2)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star5)
	(supports instrument2 thermograph1)
	(calibration_target instrument2 star1)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 planet3)
	(supports instrument3 image2)
	(calibration_target instrument3 star1)
	(on_board instrument3 satellite3)
	(power_avail satellite3)
	(pointing satellite3 star5)
)
(:goal (and
	(pointing satellite0 phenomenon4)
	(pointing satellite2 phenomenon4)
	(have_image planet3 thermograph1)
	(have_image phenomenon4 image2)
	(have_image star5 thermograph1)
	(have_image phenomenon6 thermograph1)
	(have_image star7 spectrograph0)
))

)
