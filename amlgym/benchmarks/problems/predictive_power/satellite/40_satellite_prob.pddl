(define (problem strips_sat_x_1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	satellite1 - satellite
	instrument1 - instrument
	satellite2 - satellite
	instrument2 - instrument
	image0 - mode
	spectrograph1 - mode
	star0 - direction
	groundstation1 - direction
	planet2 - direction
	star3 - direction
	star4 - direction
	phenomenon5 - direction
)
(:init
	(supports instrument0 image0)
	(calibration_target instrument0 groundstation1)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 star3)
	(supports instrument1 image0)
	(calibration_target instrument1 groundstation1)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star4)
	(supports instrument2 spectrograph1)
	(supports instrument2 image0)
	(calibration_target instrument2 groundstation1)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 planet2)
)
(:goal (and
	(pointing satellite0 star4)
	(pointing satellite1 star4)
	(pointing satellite2 star4)
	(have_image planet2 image0)
	(have_image star3 image0)
	(have_image star4 spectrograph1)
	(have_image phenomenon5 image0)
))

)
