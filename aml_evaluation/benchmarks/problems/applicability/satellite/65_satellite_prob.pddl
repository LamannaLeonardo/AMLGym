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
	spectrograph0 - mode
	thermograph1 - mode
	groundstation1 - direction
	star0 - direction
	groundstation2 - direction
	planet3 - direction
	planet4 - direction
	star5 - direction
	phenomenon6 - direction
	phenomenon7 - direction
)
(:init
	(supports instrument0 spectrograph0)
	(supports instrument0 thermograph1)
	(calibration_target instrument0 groundstation2)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 groundstation2)
	(supports instrument1 thermograph1)
	(supports instrument1 spectrograph0)
	(calibration_target instrument1 groundstation1)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star0)
	(supports instrument2 spectrograph0)
	(supports instrument2 thermograph1)
	(calibration_target instrument2 star0)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star5)
	(supports instrument3 thermograph1)
	(supports instrument3 spectrograph0)
	(calibration_target instrument3 groundstation2)
	(on_board instrument3 satellite3)
	(power_avail satellite3)
	(pointing satellite3 groundstation1)
)
(:goal (and
	(pointing satellite0 groundstation1)
	(pointing satellite3 phenomenon7)
	(have_image planet3 thermograph1)
	(have_image planet4 spectrograph0)
	(have_image star5 spectrograph0)
	(have_image phenomenon6 thermograph1)
	(have_image phenomenon7 thermograph1)
))

)
