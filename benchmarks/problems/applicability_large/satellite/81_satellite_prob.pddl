(define (problem strips_sat_x_1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	satellite1 - satellite
	instrument1 - instrument
	satellite2 - satellite
	instrument2 - instrument
	spectrograph0 - mode
	thermograph1 - mode
	groundstation0 - direction
	groundstation1 - direction
	star2 - direction
	phenomenon3 - direction
	phenomenon4 - direction
	planet5 - direction
)
(:init
	(supports instrument0 thermograph1)
	(supports instrument0 spectrograph0)
	(calibration_target instrument0 groundstation0)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 groundstation1)
	(supports instrument1 thermograph1)
	(calibration_target instrument1 groundstation0)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 phenomenon3)
	(supports instrument2 spectrograph0)
	(supports instrument2 thermograph1)
	(calibration_target instrument2 groundstation1)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 phenomenon4)
)
(:goal (and
	(have_image star2 spectrograph0)
	(have_image phenomenon3 spectrograph0)
	(have_image phenomenon4 thermograph1)
	(have_image planet5 thermograph1)
))

)
