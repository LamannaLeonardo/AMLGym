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
	spectrograph0 - mode
	spectrograph2 - mode
	groundstation1 - direction
	groundstation2 - direction
	star0 - direction
	phenomenon3 - direction
	star4 - direction
	phenomenon5 - direction
	star6 - direction
	phenomenon7 - direction
)
(:init
	(supports instrument0 thermograph1)
	(supports instrument0 spectrograph0)
	(supports instrument0 spectrograph2)
	(calibration_target instrument0 groundstation2)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 phenomenon7)
	(supports instrument1 thermograph1)
	(supports instrument1 spectrograph0)
	(supports instrument1 spectrograph2)
	(calibration_target instrument1 star0)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star4)
	(supports instrument2 spectrograph0)
	(supports instrument2 thermograph1)
	(calibration_target instrument2 star0)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 groundstation2)
	(supports instrument3 spectrograph0)
	(calibration_target instrument3 star0)
	(on_board instrument3 satellite3)
	(power_avail satellite3)
	(pointing satellite3 groundstation2)
)
(:goal (and
	(pointing satellite1 groundstation2)
	(pointing satellite3 groundstation1)
	(have_image phenomenon3 spectrograph2)
	(have_image star4 thermograph1)
	(have_image phenomenon5 spectrograph0)
	(have_image star6 spectrograph0)
	(have_image phenomenon7 spectrograph2)
))

)
