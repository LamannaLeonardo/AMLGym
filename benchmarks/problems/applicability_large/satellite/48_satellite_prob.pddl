(define (problem strips_sat_x_1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	satellite1 - satellite
	instrument2 - instrument
	instrument3 - instrument
	instrument4 - instrument
	satellite2 - satellite
	instrument5 - instrument
	instrument6 - instrument
	instrument7 - instrument
	satellite3 - satellite
	instrument8 - instrument
	instrument9 - instrument
	satellite4 - satellite
	instrument10 - instrument
	instrument11 - instrument
	satellite5 - satellite
	instrument12 - instrument
	instrument13 - instrument
	satellite6 - satellite
	instrument14 - instrument
	instrument15 - instrument
	thermograph2 - mode
	infrared3 - mode
	infrared1 - mode
	infrared0 - mode
	image4 - mode
	groundstation1 - direction
	star0 - direction
	star5 - direction
	star2 - direction
	star3 - direction
	star4 - direction
	planet6 - direction
	planet7 - direction
	star8 - direction
	planet9 - direction
	star10 - direction
	star11 - direction
	planet12 - direction
	star13 - direction
)
(:init
	(supports instrument0 infrared1)
	(supports instrument0 image4)
	(supports instrument0 infrared3)
	(calibration_target instrument0 star3)
	(supports instrument1 infrared0)
	(calibration_target instrument1 star0)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 planet9)
	(supports instrument2 image4)
	(supports instrument2 infrared3)
	(calibration_target instrument2 groundstation1)
	(calibration_target instrument2 star0)
	(supports instrument3 thermograph2)
	(supports instrument3 infrared1)
	(calibration_target instrument3 groundstation1)
	(calibration_target instrument3 star2)
	(supports instrument4 infrared1)
	(supports instrument4 infrared3)
	(supports instrument4 thermograph2)
	(calibration_target instrument4 star3)
	(calibration_target instrument4 groundstation1)
	(on_board instrument2 satellite1)
	(on_board instrument3 satellite1)
	(on_board instrument4 satellite1)
	(power_avail satellite1)
	(pointing satellite1 planet6)
	(supports instrument5 image4)
	(calibration_target instrument5 star0)
	(calibration_target instrument5 star5)
	(supports instrument6 infrared3)
	(supports instrument6 thermograph2)
	(supports instrument6 infrared1)
	(calibration_target instrument6 star3)
	(supports instrument7 image4)
	(calibration_target instrument7 groundstation1)
	(on_board instrument5 satellite2)
	(on_board instrument6 satellite2)
	(on_board instrument7 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star0)
	(supports instrument8 infrared1)
	(supports instrument8 thermograph2)
	(calibration_target instrument8 star2)
	(supports instrument9 infrared0)
	(supports instrument9 infrared1)
	(calibration_target instrument9 star0)
	(calibration_target instrument9 star4)
	(on_board instrument8 satellite3)
	(on_board instrument9 satellite3)
	(power_avail satellite3)
	(pointing satellite3 groundstation1)
	(supports instrument10 infrared1)
	(calibration_target instrument10 groundstation1)
	(calibration_target instrument10 star4)
	(supports instrument11 image4)
	(supports instrument11 infrared3)
	(supports instrument11 thermograph2)
	(calibration_target instrument11 star0)
	(calibration_target instrument11 star2)
	(on_board instrument10 satellite4)
	(on_board instrument11 satellite4)
	(power_avail satellite4)
	(pointing satellite4 planet7)
	(supports instrument12 infrared3)
	(calibration_target instrument12 star4)
	(calibration_target instrument12 star0)
	(supports instrument13 thermograph2)
	(supports instrument13 infrared1)
	(calibration_target instrument13 star4)
	(calibration_target instrument13 star5)
	(on_board instrument12 satellite5)
	(on_board instrument13 satellite5)
	(power_avail satellite5)
	(pointing satellite5 star0)
	(supports instrument14 image4)
	(calibration_target instrument14 star3)
	(calibration_target instrument14 star2)
	(supports instrument15 image4)
	(supports instrument15 infrared1)
	(calibration_target instrument15 star4)
	(on_board instrument14 satellite6)
	(on_board instrument15 satellite6)
	(power_avail satellite6)
	(pointing satellite6 star11)
)
(:goal (and
	(pointing satellite1 star13)
	(pointing satellite3 planet7)
	(pointing satellite5 star13)
	(pointing satellite6 planet7)
	(have_image planet6 image4)
	(have_image planet7 thermograph2)
	(have_image star8 image4)
	(have_image planet9 thermograph2)
	(have_image star10 image4)
	(have_image star11 infrared0)
	(have_image planet12 infrared3)
	(have_image star13 infrared3)
))

)
