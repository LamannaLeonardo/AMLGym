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
	spectrograph2 - mode
	thermograph0 - mode
	spectrograph1 - mode
	star0 - direction
	star1 - direction
	groundstation2 - direction
	phenomenon3 - direction
	phenomenon4 - direction
	star5 - direction
	star6 - direction
	phenomenon7 - direction
)
(:init
	(supports instrument0 spectrograph1)
	(supports instrument0 spectrograph2)
	(supports instrument0 thermograph0)
	(calibration_target instrument0 star1)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 star6)
	(supports instrument1 thermograph0)
	(supports instrument1 spectrograph2)
	(calibration_target instrument1 star1)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star5)
	(supports instrument2 thermograph0)
	(calibration_target instrument2 groundstation2)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star6)
	(supports instrument3 spectrograph2)
	(calibration_target instrument3 groundstation2)
	(on_board instrument3 satellite3)
	(power_avail satellite3)
	(pointing satellite3 groundstation2)
)
(:goal (and
	(pointing satellite2 groundstation2)
	(have_image phenomenon3 spectrograph1)
	(have_image phenomenon4 thermograph0)
	(have_image star5 thermograph0)
	(have_image star6 thermograph0)
	(have_image phenomenon7 spectrograph1)
))

)
