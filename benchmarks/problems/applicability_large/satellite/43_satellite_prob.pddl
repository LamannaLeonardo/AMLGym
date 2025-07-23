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
	image1 - mode
	spectrograph2 - mode
	star1 - direction
	groundstation0 - direction
	groundstation2 - direction
	planet3 - direction
	star4 - direction
	phenomenon5 - direction
	star6 - direction
	planet7 - direction
)
(:init
	(supports instrument0 spectrograph2)
	(supports instrument0 image1)
	(calibration_target instrument0 star1)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 phenomenon5)
	(supports instrument1 image1)
	(supports instrument1 infrared0)
	(supports instrument1 spectrograph2)
	(calibration_target instrument1 groundstation0)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 planet3)
	(supports instrument2 infrared0)
	(calibration_target instrument2 groundstation0)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 phenomenon5)
	(supports instrument3 spectrograph2)
	(supports instrument3 image1)
	(calibration_target instrument3 groundstation2)
	(on_board instrument3 satellite3)
	(power_avail satellite3)
	(pointing satellite3 star4)
)
(:goal (and
	(pointing satellite0 planet7)
	(pointing satellite1 groundstation0)
	(pointing satellite2 planet3)
	(pointing satellite3 planet3)
	(have_image planet3 spectrograph2)
	(have_image star4 infrared0)
	(have_image phenomenon5 spectrograph2)
	(have_image star6 image1)
	(have_image planet7 image1)
))

)
