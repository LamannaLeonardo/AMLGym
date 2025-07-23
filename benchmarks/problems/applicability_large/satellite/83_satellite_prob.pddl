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
	thermograph1 - mode
	infrared0 - mode
	groundstation2 - direction
	star1 - direction
	star0 - direction
	phenomenon3 - direction
	planet4 - direction
	planet5 - direction
	phenomenon6 - direction
	planet7 - direction
)
(:init
	(supports instrument0 infrared0)
	(supports instrument0 spectrograph2)
	(calibration_target instrument0 star1)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 groundstation2)
	(supports instrument1 thermograph1)
	(calibration_target instrument1 star1)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 planet5)
	(supports instrument2 spectrograph2)
	(supports instrument2 thermograph1)
	(calibration_target instrument2 star1)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 groundstation2)
	(supports instrument3 spectrograph2)
	(supports instrument3 thermograph1)
	(calibration_target instrument3 star0)
	(on_board instrument3 satellite3)
	(power_avail satellite3)
	(pointing satellite3 groundstation2)
)
(:goal (and
	(pointing satellite0 planet4)
	(pointing satellite1 planet7)
	(have_image phenomenon3 thermograph1)
	(have_image planet4 spectrograph2)
	(have_image planet5 infrared0)
	(have_image phenomenon6 thermograph1)
	(have_image planet7 thermograph1)
))

)
