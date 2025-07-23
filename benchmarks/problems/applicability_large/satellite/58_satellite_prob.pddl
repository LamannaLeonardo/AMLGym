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
	satellite3 - satellite
	instrument7 - instrument
	satellite4 - satellite
	instrument8 - instrument
	instrument9 - instrument
	instrument10 - instrument
	satellite5 - satellite
	instrument11 - instrument
	instrument12 - instrument
	satellite6 - satellite
	instrument13 - instrument
	instrument14 - instrument
	instrument15 - instrument
	thermograph2 - mode
	thermograph3 - mode
	image1 - mode
	infrared0 - mode
	image4 - mode
	star4 - direction
	groundstation0 - direction
	groundstation3 - direction
	groundstation1 - direction
	star5 - direction
	star2 - direction
	phenomenon6 - direction
	phenomenon7 - direction
	planet8 - direction
	planet9 - direction
	planet10 - direction
	phenomenon11 - direction
	planet12 - direction
	phenomenon13 - direction
)
(:init
	(supports instrument0 image1)
	(calibration_target instrument0 groundstation1)
	(calibration_target instrument0 star5)
	(supports instrument1 thermograph2)
	(supports instrument1 image1)
	(calibration_target instrument1 groundstation3)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 planet12)
	(supports instrument2 thermograph3)
	(calibration_target instrument2 groundstation0)
	(supports instrument3 thermograph3)
	(supports instrument3 image1)
	(supports instrument3 infrared0)
	(calibration_target instrument3 groundstation0)
	(supports instrument4 infrared0)
	(supports instrument4 image1)
	(calibration_target instrument4 star5)
	(calibration_target instrument4 groundstation1)
	(on_board instrument2 satellite1)
	(on_board instrument3 satellite1)
	(on_board instrument4 satellite1)
	(power_avail satellite1)
	(pointing satellite1 phenomenon13)
	(supports instrument5 infrared0)
	(supports instrument5 image4)
	(supports instrument5 thermograph3)
	(calibration_target instrument5 star2)
	(supports instrument6 image4)
	(calibration_target instrument6 groundstation3)
	(calibration_target instrument6 groundstation0)
	(on_board instrument5 satellite2)
	(on_board instrument6 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star2)
	(supports instrument7 image4)
	(calibration_target instrument7 groundstation0)
	(on_board instrument7 satellite3)
	(power_avail satellite3)
	(pointing satellite3 groundstation1)
	(supports instrument8 image1)
	(calibration_target instrument8 groundstation1)
	(supports instrument9 thermograph2)
	(supports instrument9 image1)
	(calibration_target instrument9 star5)
	(calibration_target instrument9 groundstation1)
	(supports instrument10 thermograph2)
	(calibration_target instrument10 star5)
	(on_board instrument8 satellite4)
	(on_board instrument9 satellite4)
	(on_board instrument10 satellite4)
	(power_avail satellite4)
	(pointing satellite4 planet9)
	(supports instrument11 infrared0)
	(supports instrument11 image1)
	(calibration_target instrument11 star5)
	(supports instrument12 image4)
	(supports instrument12 image1)
	(calibration_target instrument12 star2)
	(calibration_target instrument12 star5)
	(on_board instrument11 satellite5)
	(on_board instrument12 satellite5)
	(power_avail satellite5)
	(pointing satellite5 planet8)
	(supports instrument13 thermograph3)
	(calibration_target instrument13 groundstation1)
	(calibration_target instrument13 groundstation0)
	(supports instrument14 image4)
	(supports instrument14 thermograph3)
	(calibration_target instrument14 groundstation1)
	(calibration_target instrument14 groundstation3)
	(supports instrument15 image4)
	(supports instrument15 thermograph2)
	(supports instrument15 image1)
	(calibration_target instrument15 star2)
	(calibration_target instrument15 star5)
	(on_board instrument13 satellite6)
	(on_board instrument14 satellite6)
	(on_board instrument15 satellite6)
	(power_avail satellite6)
	(pointing satellite6 planet8)
)
(:goal (and
	(pointing satellite0 phenomenon13)
	(pointing satellite4 phenomenon6)
	(have_image phenomenon6 image1)
	(have_image phenomenon7 thermograph3)
	(have_image planet8 thermograph3)
	(have_image planet9 infrared0)
	(have_image planet10 thermograph2)
	(have_image phenomenon11 image4)
	(have_image planet12 image4)
	(have_image phenomenon13 thermograph2)
))

)
