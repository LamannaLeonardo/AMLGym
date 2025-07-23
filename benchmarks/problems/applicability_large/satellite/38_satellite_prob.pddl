(define (problem strips_sat_x_1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	satellite1 - satellite
	instrument1 - instrument
	instrument2 - instrument
	satellite2 - satellite
	instrument3 - instrument
	satellite3 - satellite
	instrument4 - instrument
	instrument5 - instrument
	instrument6 - instrument
	satellite4 - satellite
	instrument7 - instrument
	instrument8 - instrument
	instrument9 - instrument
	satellite5 - satellite
	instrument10 - instrument
	instrument11 - instrument
	instrument12 - instrument
	satellite6 - satellite
	instrument13 - instrument
	instrument14 - instrument
	instrument15 - instrument
	infrared1 - mode
	infrared0 - mode
	infrared4 - mode
	thermograph3 - mode
	spectrograph2 - mode
	groundstation3 - direction
	groundstation1 - direction
	star0 - direction
	star4 - direction
	star5 - direction
	star2 - direction
	phenomenon6 - direction
	planet7 - direction
	phenomenon8 - direction
	planet9 - direction
	planet10 - direction
	phenomenon11 - direction
	phenomenon12 - direction
	phenomenon13 - direction
)
(:init
	(supports instrument0 spectrograph2)
	(supports instrument0 infrared0)
	(calibration_target instrument0 groundstation1)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 groundstation1)
	(supports instrument1 infrared0)
	(supports instrument1 infrared4)
	(calibration_target instrument1 star2)
	(calibration_target instrument1 star0)
	(supports instrument2 infrared0)
	(supports instrument2 thermograph3)
	(calibration_target instrument2 groundstation3)
	(calibration_target instrument2 star5)
	(on_board instrument1 satellite1)
	(on_board instrument2 satellite1)
	(power_avail satellite1)
	(pointing satellite1 phenomenon6)
	(supports instrument3 infrared0)
	(calibration_target instrument3 star0)
	(on_board instrument3 satellite2)
	(power_avail satellite2)
	(pointing satellite2 planet10)
	(supports instrument4 infrared0)
	(supports instrument4 thermograph3)
	(supports instrument4 infrared4)
	(calibration_target instrument4 groundstation3)
	(supports instrument5 infrared0)
	(calibration_target instrument5 star5)
	(supports instrument6 infrared1)
	(supports instrument6 spectrograph2)
	(supports instrument6 infrared0)
	(calibration_target instrument6 star4)
	(calibration_target instrument6 star2)
	(on_board instrument4 satellite3)
	(on_board instrument5 satellite3)
	(on_board instrument6 satellite3)
	(power_avail satellite3)
	(pointing satellite3 groundstation3)
	(supports instrument7 spectrograph2)
	(supports instrument7 infrared0)
	(calibration_target instrument7 star5)
	(supports instrument8 spectrograph2)
	(supports instrument8 infrared4)
	(supports instrument8 infrared0)
	(calibration_target instrument8 groundstation1)
	(supports instrument9 infrared1)
	(supports instrument9 spectrograph2)
	(calibration_target instrument9 star2)
	(calibration_target instrument9 groundstation1)
	(on_board instrument7 satellite4)
	(on_board instrument8 satellite4)
	(on_board instrument9 satellite4)
	(power_avail satellite4)
	(pointing satellite4 planet7)
	(supports instrument10 infrared4)
	(calibration_target instrument10 star5)
	(calibration_target instrument10 star0)
	(supports instrument11 spectrograph2)
	(supports instrument11 infrared1)
	(supports instrument11 infrared0)
	(calibration_target instrument11 star4)
	(calibration_target instrument11 star0)
	(supports instrument12 thermograph3)
	(supports instrument12 infrared4)
	(calibration_target instrument12 star5)
	(on_board instrument10 satellite5)
	(on_board instrument11 satellite5)
	(on_board instrument12 satellite5)
	(power_avail satellite5)
	(pointing satellite5 star0)
	(supports instrument13 infrared4)
	(calibration_target instrument13 star0)
	(supports instrument14 infrared4)
	(supports instrument14 infrared1)
	(calibration_target instrument14 star4)
	(supports instrument15 infrared0)
	(supports instrument15 infrared1)
	(supports instrument15 spectrograph2)
	(calibration_target instrument15 star2)
	(calibration_target instrument15 star5)
	(on_board instrument13 satellite6)
	(on_board instrument14 satellite6)
	(on_board instrument15 satellite6)
	(power_avail satellite6)
	(pointing satellite6 groundstation3)
)
(:goal (and
	(pointing satellite0 planet9)
	(pointing satellite1 star5)
	(pointing satellite5 phenomenon12)
	(have_image phenomenon6 infrared0)
	(have_image planet7 infrared1)
	(have_image phenomenon8 spectrograph2)
	(have_image planet9 infrared4)
	(have_image planet10 thermograph3)
	(have_image phenomenon11 infrared1)
	(have_image phenomenon12 thermograph3)
	(have_image phenomenon13 infrared4)
))

)
