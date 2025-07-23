(define (problem strips_sat_x_1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	instrument2 - instrument
	satellite1 - satellite
	instrument3 - instrument
	instrument4 - instrument
	satellite2 - satellite
	instrument5 - instrument
	satellite3 - satellite
	instrument6 - instrument
	instrument7 - instrument
	instrument8 - instrument
	satellite4 - satellite
	instrument9 - instrument
	instrument10 - instrument
	satellite5 - satellite
	instrument11 - instrument
	instrument12 - instrument
	instrument13 - instrument
	satellite6 - satellite
	instrument14 - instrument
	thermograph1 - mode
	thermograph0 - mode
	infrared4 - mode
	infrared2 - mode
	image3 - mode
	groundstation1 - direction
	groundstation2 - direction
	star5 - direction
	star0 - direction
	star3 - direction
	groundstation4 - direction
	star6 - direction
	star7 - direction
	phenomenon8 - direction
	phenomenon9 - direction
	phenomenon10 - direction
	star11 - direction
	phenomenon12 - direction
	planet13 - direction
)
(:init
	(supports instrument0 thermograph1)
	(calibration_target instrument0 groundstation2)
	(supports instrument1 infrared4)
	(supports instrument1 thermograph0)
	(calibration_target instrument1 star3)
	(calibration_target instrument1 star0)
	(supports instrument2 thermograph1)
	(calibration_target instrument2 groundstation4)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(on_board instrument2 satellite0)
	(power_avail satellite0)
	(pointing satellite0 star0)
	(supports instrument3 thermograph1)
	(calibration_target instrument3 groundstation1)
	(supports instrument4 thermograph0)
	(supports instrument4 infrared2)
	(supports instrument4 image3)
	(calibration_target instrument4 star3)
	(calibration_target instrument4 groundstation4)
	(on_board instrument3 satellite1)
	(on_board instrument4 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star3)
	(supports instrument5 infrared2)
	(calibration_target instrument5 star5)
	(calibration_target instrument5 groundstation1)
	(on_board instrument5 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star0)
	(supports instrument6 infrared4)
	(supports instrument6 image3)
	(calibration_target instrument6 star0)
	(calibration_target instrument6 groundstation2)
	(supports instrument7 image3)
	(calibration_target instrument7 star5)
	(supports instrument8 infrared2)
	(supports instrument8 thermograph1)
	(supports instrument8 image3)
	(calibration_target instrument8 star0)
	(calibration_target instrument8 groundstation2)
	(on_board instrument6 satellite3)
	(on_board instrument7 satellite3)
	(on_board instrument8 satellite3)
	(power_avail satellite3)
	(pointing satellite3 phenomenon8)
	(supports instrument9 infrared4)
	(supports instrument9 thermograph0)
	(supports instrument9 infrared2)
	(calibration_target instrument9 groundstation4)
	(calibration_target instrument9 star3)
	(supports instrument10 infrared4)
	(calibration_target instrument10 groundstation2)
	(on_board instrument9 satellite4)
	(on_board instrument10 satellite4)
	(power_avail satellite4)
	(pointing satellite4 star0)
	(supports instrument11 image3)
	(supports instrument11 thermograph1)
	(supports instrument11 infrared2)
	(calibration_target instrument11 groundstation2)
	(supports instrument12 infrared2)
	(supports instrument12 thermograph0)
	(supports instrument12 image3)
	(calibration_target instrument12 star5)
	(calibration_target instrument12 groundstation4)
	(supports instrument13 infrared4)
	(supports instrument13 infrared2)
	(supports instrument13 thermograph0)
	(calibration_target instrument13 star0)
	(on_board instrument11 satellite5)
	(on_board instrument12 satellite5)
	(on_board instrument13 satellite5)
	(power_avail satellite5)
	(pointing satellite5 star5)
	(supports instrument14 thermograph0)
	(supports instrument14 thermograph1)
	(calibration_target instrument14 groundstation4)
	(calibration_target instrument14 star3)
	(on_board instrument14 satellite6)
	(power_avail satellite6)
	(pointing satellite6 star7)
)
(:goal (and
	(pointing satellite1 phenomenon8)
	(pointing satellite3 star11)
	(pointing satellite5 star7)
	(have_image star6 image3)
	(have_image star7 infrared4)
	(have_image phenomenon8 infrared2)
	(have_image phenomenon9 thermograph0)
	(have_image phenomenon10 thermograph0)
	(have_image star11 infrared2)
	(have_image phenomenon12 infrared2)
	(have_image planet13 infrared2)
))

)
