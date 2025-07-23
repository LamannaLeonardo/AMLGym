(define (problem strips_sat_x_1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	instrument2 - instrument
	satellite1 - satellite
	instrument3 - instrument
	satellite2 - satellite
	instrument4 - instrument
	satellite3 - satellite
	instrument5 - instrument
	instrument6 - instrument
	instrument7 - instrument
	satellite4 - satellite
	instrument8 - instrument
	satellite5 - satellite
	instrument9 - instrument
	instrument10 - instrument
	instrument11 - instrument
	satellite6 - satellite
	instrument12 - instrument
	instrument13 - instrument
	instrument14 - instrument
	infrared4 - mode
	thermograph1 - mode
	thermograph3 - mode
	thermograph0 - mode
	infrared2 - mode
	star1 - direction
	groundstation5 - direction
	groundstation0 - direction
	star3 - direction
	star4 - direction
	star2 - direction
	phenomenon6 - direction
	phenomenon7 - direction
	phenomenon8 - direction
	planet9 - direction
	planet10 - direction
	phenomenon11 - direction
	star12 - direction
	phenomenon13 - direction
)
(:init
	(supports instrument0 infrared2)
	(supports instrument0 thermograph3)
	(calibration_target instrument0 star4)
	(calibration_target instrument0 star3)
	(supports instrument1 thermograph0)
	(calibration_target instrument1 groundstation0)
	(supports instrument2 infrared2)
	(calibration_target instrument2 star4)
	(calibration_target instrument2 star3)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(on_board instrument2 satellite0)
	(power_avail satellite0)
	(pointing satellite0 star2)
	(supports instrument3 thermograph0)
	(supports instrument3 infrared4)
	(supports instrument3 infrared2)
	(calibration_target instrument3 star4)
	(on_board instrument3 satellite1)
	(power_avail satellite1)
	(pointing satellite1 phenomenon6)
	(supports instrument4 thermograph3)
	(calibration_target instrument4 groundstation5)
	(calibration_target instrument4 star1)
	(on_board instrument4 satellite2)
	(power_avail satellite2)
	(pointing satellite2 phenomenon11)
	(supports instrument5 thermograph0)
	(supports instrument5 thermograph3)
	(calibration_target instrument5 star3)
	(supports instrument6 infrared4)
	(calibration_target instrument6 star1)
	(supports instrument7 thermograph0)
	(supports instrument7 infrared2)
	(supports instrument7 infrared4)
	(calibration_target instrument7 star3)
	(on_board instrument5 satellite3)
	(on_board instrument6 satellite3)
	(on_board instrument7 satellite3)
	(power_avail satellite3)
	(pointing satellite3 phenomenon6)
	(supports instrument8 infrared4)
	(supports instrument8 thermograph0)
	(calibration_target instrument8 groundstation5)
	(calibration_target instrument8 star1)
	(on_board instrument8 satellite4)
	(power_avail satellite4)
	(pointing satellite4 groundstation5)
	(supports instrument9 infrared2)
	(calibration_target instrument9 groundstation5)
	(calibration_target instrument9 star1)
	(supports instrument10 infrared4)
	(supports instrument10 thermograph3)
	(calibration_target instrument10 star4)
	(supports instrument11 thermograph0)
	(supports instrument11 thermograph1)
	(calibration_target instrument11 groundstation5)
	(calibration_target instrument11 star2)
	(on_board instrument9 satellite5)
	(on_board instrument10 satellite5)
	(on_board instrument11 satellite5)
	(power_avail satellite5)
	(pointing satellite5 star4)
	(supports instrument12 infrared2)
	(supports instrument12 infrared4)
	(supports instrument12 thermograph3)
	(calibration_target instrument12 groundstation0)
	(calibration_target instrument12 star3)
	(supports instrument13 thermograph1)
	(supports instrument13 thermograph3)
	(supports instrument13 thermograph0)
	(calibration_target instrument13 star3)
	(supports instrument14 infrared4)
	(supports instrument14 thermograph0)
	(supports instrument14 thermograph1)
	(calibration_target instrument14 star2)
	(calibration_target instrument14 star4)
	(on_board instrument12 satellite6)
	(on_board instrument13 satellite6)
	(on_board instrument14 satellite6)
	(power_avail satellite6)
	(pointing satellite6 phenomenon11)
)
(:goal (and
	(pointing satellite0 star3)
	(pointing satellite1 star4)
	(pointing satellite2 star1)
	(pointing satellite3 phenomenon11)
	(pointing satellite4 planet10)
	(pointing satellite6 phenomenon7)
	(have_image phenomenon6 thermograph1)
	(have_image phenomenon7 thermograph0)
	(have_image phenomenon8 infrared4)
	(have_image planet9 infrared2)
	(have_image planet10 thermograph0)
	(have_image phenomenon11 infrared2)
	(have_image star12 thermograph3)
	(have_image phenomenon13 infrared4)
))

)
