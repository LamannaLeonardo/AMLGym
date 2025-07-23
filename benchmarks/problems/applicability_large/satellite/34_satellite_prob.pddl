(define (problem strips_sat_x_1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	satellite1 - satellite
	instrument2 - instrument
	instrument3 - instrument
	satellite2 - satellite
	instrument4 - instrument
	satellite3 - satellite
	instrument5 - instrument
	instrument6 - instrument
	satellite4 - satellite
	instrument7 - instrument
	instrument8 - instrument
	spectrograph2 - mode
	infrared0 - mode
	image1 - mode
	star2 - direction
	groundstation1 - direction
	star3 - direction
	groundstation0 - direction
	phenomenon4 - direction
	phenomenon5 - direction
	planet6 - direction
	planet7 - direction
	phenomenon8 - direction
	star9 - direction
)
(:init
	(supports instrument0 image1)
	(supports instrument0 spectrograph2)
	(calibration_target instrument0 groundstation0)
	(supports instrument1 image1)
	(supports instrument1 spectrograph2)
	(supports instrument1 infrared0)
	(calibration_target instrument1 star3)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 star2)
	(supports instrument2 image1)
	(supports instrument2 spectrograph2)
	(supports instrument2 infrared0)
	(calibration_target instrument2 groundstation0)
	(supports instrument3 spectrograph2)
	(supports instrument3 infrared0)
	(calibration_target instrument3 groundstation1)
	(on_board instrument2 satellite1)
	(on_board instrument3 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star2)
	(supports instrument4 infrared0)
	(supports instrument4 spectrograph2)
	(supports instrument4 image1)
	(calibration_target instrument4 star3)
	(on_board instrument4 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star2)
	(supports instrument5 spectrograph2)
	(calibration_target instrument5 groundstation1)
	(supports instrument6 spectrograph2)
	(supports instrument6 image1)
	(supports instrument6 infrared0)
	(calibration_target instrument6 star3)
	(on_board instrument5 satellite3)
	(on_board instrument6 satellite3)
	(power_avail satellite3)
	(pointing satellite3 planet6)
	(supports instrument7 infrared0)
	(calibration_target instrument7 groundstation0)
	(supports instrument8 infrared0)
	(calibration_target instrument8 groundstation0)
	(on_board instrument7 satellite4)
	(on_board instrument8 satellite4)
	(power_avail satellite4)
	(pointing satellite4 star3)
)
(:goal (and
	(pointing satellite1 planet6)
	(pointing satellite3 phenomenon8)
	(pointing satellite4 phenomenon4)
	(have_image phenomenon4 infrared0)
	(have_image phenomenon5 image1)
	(have_image planet6 spectrograph2)
	(have_image planet7 image1)
	(have_image phenomenon8 infrared0)
	(have_image star9 infrared0)
))

)
