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
	spectrograph1 - mode
	star1 - direction
	star0 - direction
	star2 - direction
	phenomenon3 - direction
	star4 - direction
	phenomenon5 - direction
	phenomenon6 - direction
	planet7 - direction
)
(:init
	(supports instrument0 spectrograph0)
	(calibration_target instrument0 star1)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 planet7)
	(supports instrument1 spectrograph1)
	(calibration_target instrument1 star0)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star0)
	(supports instrument2 spectrograph0)
	(calibration_target instrument2 star0)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star2)
	(supports instrument3 spectrograph0)
	(calibration_target instrument3 star2)
	(on_board instrument3 satellite3)
	(power_avail satellite3)
	(pointing satellite3 phenomenon6)
)
(:goal (and
	(have_image phenomenon3 spectrograph0)
	(have_image star4 spectrograph0)
	(have_image phenomenon5 spectrograph1)
	(have_image phenomenon6 spectrograph1)
	(have_image planet7 spectrograph0)
))

)
