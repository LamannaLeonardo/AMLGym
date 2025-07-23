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
	satellite5 - satellite
	instrument8 - instrument
	infrared0 - mode
	thermograph3 - mode
	image1 - mode
	spectrograph2 - mode
	groundstation2 - direction
	star1 - direction
	star4 - direction
	star0 - direction
	star3 - direction
	phenomenon5 - direction
	star6 - direction
	planet7 - direction
	phenomenon8 - direction
	phenomenon9 - direction
	phenomenon10 - direction
	phenomenon11 - direction
)
(:init
	(supports instrument0 thermograph3)
	(supports instrument0 infrared0)
	(calibration_target instrument0 star4)
	(supports instrument1 spectrograph2)
	(supports instrument1 image1)
	(supports instrument1 infrared0)
	(calibration_target instrument1 star3)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 phenomenon5)
	(supports instrument2 infrared0)
	(supports instrument2 spectrograph2)
	(supports instrument2 image1)
	(calibration_target instrument2 star3)
	(supports instrument3 infrared0)
	(supports instrument3 spectrograph2)
	(calibration_target instrument3 star1)
	(on_board instrument2 satellite1)
	(on_board instrument3 satellite1)
	(power_avail satellite1)
	(pointing satellite1 phenomenon11)
	(supports instrument4 infrared0)
	(supports instrument4 thermograph3)
	(calibration_target instrument4 star1)
	(on_board instrument4 satellite2)
	(power_avail satellite2)
	(pointing satellite2 phenomenon11)
	(supports instrument5 image1)
	(calibration_target instrument5 star1)
	(supports instrument6 image1)
	(calibration_target instrument6 star4)
	(on_board instrument5 satellite3)
	(on_board instrument6 satellite3)
	(power_avail satellite3)
	(pointing satellite3 groundstation2)
	(supports instrument7 spectrograph2)
	(supports instrument7 thermograph3)
	(supports instrument7 infrared0)
	(calibration_target instrument7 star0)
	(on_board instrument7 satellite4)
	(power_avail satellite4)
	(pointing satellite4 phenomenon11)
	(supports instrument8 spectrograph2)
	(supports instrument8 image1)
	(supports instrument8 thermograph3)
	(calibration_target instrument8 star3)
	(on_board instrument8 satellite5)
	(power_avail satellite5)
	(pointing satellite5 planet7)
)
(:goal (and
	(pointing satellite1 phenomenon8)
	(pointing satellite3 star3)
	(pointing satellite4 star1)
	(have_image phenomenon5 spectrograph2)
	(have_image star6 thermograph3)
	(have_image planet7 spectrograph2)
	(have_image phenomenon8 spectrograph2)
	(have_image phenomenon9 thermograph3)
	(have_image phenomenon10 thermograph3)
	(have_image phenomenon11 image1)
))

)
