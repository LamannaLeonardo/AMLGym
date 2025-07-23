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
	image2 - mode
	spectrograph1 - mode
	star0 - direction
	star2 - direction
	groundstation1 - direction
	star3 - direction
	phenomenon4 - direction
	phenomenon5 - direction
	phenomenon6 - direction
	planet7 - direction
)
(:init
	(supports instrument0 spectrograph1)
	(supports instrument0 image2)
	(calibration_target instrument0 star2)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 star3)
	(supports instrument1 image2)
	(supports instrument1 thermograph0)
	(supports instrument1 spectrograph1)
	(calibration_target instrument1 star2)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 groundstation1)
	(supports instrument2 thermograph0)
	(calibration_target instrument2 groundstation1)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star0)
	(supports instrument3 spectrograph1)
	(calibration_target instrument3 groundstation1)
	(on_board instrument3 satellite3)
	(power_avail satellite3)
	(pointing satellite3 phenomenon6)
)
(:goal (and
	(pointing satellite2 planet7)
	(have_image star3 spectrograph1)
	(have_image phenomenon4 thermograph0)
	(have_image phenomenon5 thermograph0)
	(have_image phenomenon6 spectrograph1)
	(have_image planet7 spectrograph1)
))

)
