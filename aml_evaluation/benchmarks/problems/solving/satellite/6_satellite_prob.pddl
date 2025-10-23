(define (problem strips_sat_x_1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	satellite1 - satellite
	instrument2 - instrument
	satellite2 - satellite
	instrument3 - instrument
	satellite3 - satellite
	instrument4 - instrument
	instrument5 - instrument
	satellite4 - satellite
	instrument6 - instrument
	instrument7 - instrument
	satellite5 - satellite
	instrument8 - instrument
	instrument9 - instrument
	thermograph3 - mode
	spectrograph1 - mode
	spectrograph2 - mode
	infrared0 - mode
	star4 - direction
	star2 - direction
	star0 - direction
	groundstation1 - direction
	star3 - direction
	star5 - direction
	star6 - direction
	planet7 - direction
	phenomenon8 - direction
	phenomenon9 - direction
	star10 - direction
	phenomenon11 - direction
)
(:init
	(supports instrument0 thermograph3)
	(supports instrument0 spectrograph2)
	(supports instrument0 spectrograph1)
	(calibration_target instrument0 star0)
	(supports instrument1 thermograph3)
	(calibration_target instrument1 star4)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 planet7)
	(supports instrument2 thermograph3)
	(supports instrument2 infrared0)
	(calibration_target instrument2 groundstation1)
	(on_board instrument2 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star10)
	(supports instrument3 spectrograph1)
	(calibration_target instrument3 star2)
	(on_board instrument3 satellite2)
	(power_avail satellite2)
	(pointing satellite2 planet7)
	(supports instrument4 spectrograph2)
	(supports instrument4 spectrograph1)
	(supports instrument4 infrared0)
	(calibration_target instrument4 star3)
	(supports instrument5 infrared0)
	(supports instrument5 spectrograph2)
	(calibration_target instrument5 star0)
	(on_board instrument4 satellite3)
	(on_board instrument5 satellite3)
	(power_avail satellite3)
	(pointing satellite3 star6)
	(supports instrument6 spectrograph2)
	(calibration_target instrument6 star2)
	(supports instrument7 spectrograph2)
	(supports instrument7 infrared0)
	(supports instrument7 spectrograph1)
	(calibration_target instrument7 star0)
	(on_board instrument6 satellite4)
	(on_board instrument7 satellite4)
	(power_avail satellite4)
	(pointing satellite4 star6)
	(supports instrument8 spectrograph2)
	(supports instrument8 spectrograph1)
	(supports instrument8 thermograph3)
	(calibration_target instrument8 groundstation1)
	(supports instrument9 spectrograph2)
	(supports instrument9 infrared0)
	(calibration_target instrument9 star3)
	(on_board instrument8 satellite5)
	(on_board instrument9 satellite5)
	(power_avail satellite5)
	(pointing satellite5 phenomenon8)
)
(:goal (and
	(have_image star5 spectrograph2)
	(have_image star6 spectrograph1)
	(have_image planet7 spectrograph2)
	(have_image phenomenon8 spectrograph1)
	(have_image phenomenon9 thermograph3)
	(have_image star10 spectrograph1)
	(have_image phenomenon11 spectrograph1)
))

)
