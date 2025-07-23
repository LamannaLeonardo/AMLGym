(define (problem strips_sat_x_1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	satellite1 - satellite
	instrument1 - instrument
	satellite2 - satellite
	instrument2 - instrument
	instrument3 - instrument
	satellite3 - satellite
	instrument4 - instrument
	instrument5 - instrument
	satellite4 - satellite
	instrument6 - instrument
	instrument7 - instrument
	spectrograph2 - mode
	infrared3 - mode
	infrared0 - mode
	image1 - mode
	groundstation2 - direction
	groundstation0 - direction
	star3 - direction
	groundstation1 - direction
	star4 - direction
	planet5 - direction
	phenomenon6 - direction
	planet7 - direction
	star8 - direction
	planet9 - direction
)
(:init
	(supports instrument0 infrared3)
	(supports instrument0 infrared0)
	(supports instrument0 spectrograph2)
	(calibration_target instrument0 star3)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 groundstation2)
	(supports instrument1 infrared3)
	(supports instrument1 image1)
	(supports instrument1 infrared0)
	(calibration_target instrument1 groundstation2)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star4)
	(supports instrument2 spectrograph2)
	(supports instrument2 infrared3)
	(calibration_target instrument2 groundstation2)
	(supports instrument3 infrared3)
	(supports instrument3 infrared0)
	(supports instrument3 image1)
	(calibration_target instrument3 groundstation0)
	(on_board instrument2 satellite2)
	(on_board instrument3 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star4)
	(supports instrument4 infrared3)
	(supports instrument4 image1)
	(calibration_target instrument4 star3)
	(supports instrument5 infrared3)
	(supports instrument5 infrared0)
	(supports instrument5 image1)
	(calibration_target instrument5 star3)
	(on_board instrument4 satellite3)
	(on_board instrument5 satellite3)
	(power_avail satellite3)
	(pointing satellite3 star4)
	(supports instrument6 image1)
	(calibration_target instrument6 star3)
	(supports instrument7 infrared0)
	(calibration_target instrument7 groundstation1)
	(on_board instrument6 satellite4)
	(on_board instrument7 satellite4)
	(power_avail satellite4)
	(pointing satellite4 star3)
)
(:goal (and
	(pointing satellite3 star8)
	(have_image star4 image1)
	(have_image planet5 image1)
	(have_image phenomenon6 infrared0)
	(have_image planet7 infrared3)
	(have_image star8 spectrograph2)
	(have_image planet9 infrared3)
))

)
