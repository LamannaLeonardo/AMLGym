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
	star1 - direction
	planet2 - direction
	planet3 - direction
	phenomenon4 - direction
	planet5 - direction
)
(:init
	(supports instrument0 spectrograph0)
	(calibration_target instrument0 star1)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 star1)
	(supports instrument1 thermograph1)
	(supports instrument1 spectrograph0)
	(calibration_target instrument1 star1)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star1)
	(supports instrument2 spectrograph0)
	(calibration_target instrument2 star1)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star1)
)
(:goal (and
	(pointing satellite0 planet3)
	(have_image planet2 thermograph1)
	(have_image planet3 spectrograph0)
	(have_image phenomenon4 spectrograph0)
	(have_image planet5 spectrograph0)
))

)
