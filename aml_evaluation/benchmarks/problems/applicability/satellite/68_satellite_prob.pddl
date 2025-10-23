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
	spectrograph1 - mode
	star2 - direction
	groundstation0 - direction
	groundstation1 - direction
	phenomenon3 - direction
	phenomenon4 - direction
	planet5 - direction
	star6 - direction
	star7 - direction
)
(:init
	(supports instrument0 spectrograph1)
	(supports instrument0 thermograph0)
	(calibration_target instrument0 groundstation0)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 groundstation0)
	(supports instrument1 thermograph0)
	(supports instrument1 spectrograph1)
	(calibration_target instrument1 groundstation0)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 planet5)
	(supports instrument2 spectrograph1)
	(supports instrument2 thermograph0)
	(calibration_target instrument2 groundstation0)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star2)
	(supports instrument3 spectrograph1)
	(calibration_target instrument3 groundstation1)
	(on_board instrument3 satellite3)
	(power_avail satellite3)
	(pointing satellite3 star2)
)
(:goal (and
	(pointing satellite1 star7)
	(have_image phenomenon3 thermograph0)
	(have_image phenomenon4 spectrograph1)
	(have_image planet5 thermograph0)
	(have_image star6 spectrograph1)
	(have_image star7 thermograph0)
))

)
