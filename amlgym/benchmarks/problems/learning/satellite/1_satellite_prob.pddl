(define (problem strips_sat_x_1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	satellite1 - satellite
	instrument1 - instrument
	satellite2 - satellite
	instrument2 - instrument
	spectrograph1 - mode
	infrared0 - mode
	star1 - direction
	groundstation0 - direction
	phenomenon2 - direction
	planet3 - direction
	star4 - direction
	phenomenon5 - direction
)
(:init
	(supports instrument0 infrared0)
	(supports instrument0 spectrograph1)
	(calibration_target instrument0 star1)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 groundstation0)
	(supports instrument1 infrared0)
	(supports instrument1 spectrograph1)
	(calibration_target instrument1 groundstation0)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 planet3)
	(supports instrument2 spectrograph1)
	(calibration_target instrument2 groundstation0)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star4)
)
(:goal (and
	(have_image phenomenon2 spectrograph1)
	(have_image planet3 spectrograph1)
	(have_image star4 spectrograph1)
	(have_image phenomenon5 infrared0)
))

)
