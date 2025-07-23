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
	infrared0 - mode
	spectrograph1 - mode
	groundstation0 - direction
	groundstation1 - direction
	star2 - direction
	star3 - direction
	star4 - direction
	phenomenon5 - direction
	phenomenon6 - direction
	planet7 - direction
)
(:init
	(supports instrument0 infrared0)
	(supports instrument0 spectrograph1)
	(calibration_target instrument0 groundstation0)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 planet7)
	(supports instrument1 spectrograph1)
	(supports instrument1 infrared0)
	(calibration_target instrument1 groundstation0)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 phenomenon5)
	(supports instrument2 spectrograph1)
	(supports instrument2 infrared0)
	(calibration_target instrument2 groundstation1)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star2)
	(supports instrument3 infrared0)
	(supports instrument3 spectrograph1)
	(calibration_target instrument3 star2)
	(on_board instrument3 satellite3)
	(power_avail satellite3)
	(pointing satellite3 planet7)
)
(:goal (and
	(pointing satellite0 star3)
	(pointing satellite1 groundstation0)
	(pointing satellite3 phenomenon6)
	(have_image star3 infrared0)
	(have_image star4 infrared0)
	(have_image phenomenon5 infrared0)
	(have_image phenomenon6 spectrograph1)
	(have_image planet7 spectrograph1)
))

)
