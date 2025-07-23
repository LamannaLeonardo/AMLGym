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
	instrument4 - instrument
	satellite3 - satellite
	instrument5 - instrument
	instrument6 - instrument
	instrument7 - instrument
	satellite4 - satellite
	instrument8 - instrument
	instrument9 - instrument
	satellite5 - satellite
	instrument10 - instrument
	instrument11 - instrument
	instrument12 - instrument
	satellite6 - satellite
	instrument13 - instrument
	instrument14 - instrument
	infrared2 - mode
	thermograph1 - mode
	image3 - mode
	image4 - mode
	infrared5 - mode
	infrared0 - mode
	star2 - direction
	star4 - direction
	groundstation1 - direction
	star0 - direction
	star5 - direction
	star3 - direction
	star6 - direction
	phenomenon7 - direction
	planet8 - direction
	phenomenon9 - direction
	planet10 - direction
	star11 - direction
	phenomenon12 - direction
	phenomenon13 - direction
)
(:init
	(supports instrument0 thermograph1)
	(supports instrument0 infrared0)
	(calibration_target instrument0 star5)
	(supports instrument1 image4)
	(calibration_target instrument1 star4)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 groundstation1)
	(supports instrument2 infrared5)
	(supports instrument2 image3)
	(calibration_target instrument2 groundstation1)
	(on_board instrument2 satellite1)
	(power_avail satellite1)
	(pointing satellite1 planet8)
	(supports instrument3 thermograph1)
	(calibration_target instrument3 star4)
	(calibration_target instrument3 star2)
	(supports instrument4 image4)
	(supports instrument4 thermograph1)
	(calibration_target instrument4 star0)
	(calibration_target instrument4 star3)
	(on_board instrument3 satellite2)
	(on_board instrument4 satellite2)
	(power_avail satellite2)
	(pointing satellite2 planet8)
	(supports instrument5 infrared0)
	(supports instrument5 infrared5)
	(supports instrument5 infrared2)
	(calibration_target instrument5 star2)
	(supports instrument6 infrared0)
	(supports instrument6 image4)
	(calibration_target instrument6 star0)
	(calibration_target instrument6 star5)
	(supports instrument7 infrared2)
	(calibration_target instrument7 star4)
	(on_board instrument5 satellite3)
	(on_board instrument6 satellite3)
	(on_board instrument7 satellite3)
	(power_avail satellite3)
	(pointing satellite3 star2)
	(supports instrument8 infrared2)
	(calibration_target instrument8 star4)
	(supports instrument9 image4)
	(supports instrument9 infrared2)
	(calibration_target instrument9 groundstation1)
	(calibration_target instrument9 star4)
	(on_board instrument8 satellite4)
	(on_board instrument9 satellite4)
	(power_avail satellite4)
	(pointing satellite4 star2)
	(supports instrument10 infrared5)
	(calibration_target instrument10 star5)
	(supports instrument11 thermograph1)
	(supports instrument11 infrared5)
	(calibration_target instrument11 star0)
	(supports instrument12 infrared0)
	(calibration_target instrument12 star3)
	(on_board instrument10 satellite5)
	(on_board instrument11 satellite5)
	(on_board instrument12 satellite5)
	(power_avail satellite5)
	(pointing satellite5 star4)
	(supports instrument13 image3)
	(supports instrument13 infrared5)
	(calibration_target instrument13 star0)
	(supports instrument14 infrared0)
	(supports instrument14 thermograph1)
	(calibration_target instrument14 star3)
	(calibration_target instrument14 star5)
	(on_board instrument13 satellite6)
	(on_board instrument14 satellite6)
	(power_avail satellite6)
	(pointing satellite6 star11)
)
(:goal (and
	(have_image star6 thermograph1)
	(have_image star6 image3)
	(have_image phenomenon7 infrared2)
	(have_image phenomenon7 infrared5)
	(have_image planet8 infrared0)
	(have_image planet8 image3)
	(have_image phenomenon9 infrared2)
	(have_image planet10 thermograph1)
	(have_image star11 infrared5)
	(have_image star11 image3)
	(have_image phenomenon12 infrared5)
	(have_image phenomenon13 infrared2)
))

)
