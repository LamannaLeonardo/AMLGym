(define (problem strips-sat-x-1)
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
	instrument5 - instrument
	instrument6 - instrument
	satellite3 - satellite
	instrument7 - instrument
	instrument8 - instrument
	instrument9 - instrument
	instrument10 - instrument
	satellite4 - satellite
	instrument11 - instrument
	instrument12 - instrument
	satellite5 - satellite
	instrument13 - instrument
	thermograph2 - mode
	image3 - mode
	image4 - mode
	infrared0 - mode
	infrared1 - mode
	groundstation2 - direction
	star4 - direction
	groundstation0 - direction
	groundstation3 - direction
	star1 - direction
	planet5 - direction
	phenomenon6 - direction
	planet7 - direction
	phenomenon8 - direction
	phenomenon9 - direction
	star10 - direction
	star11 - direction
)
(:init
	(supports instrument0 image4)
	(calibration_target instrument0 star1)
	(supports instrument1 thermograph2)
	(supports instrument1 infrared0)
	(calibration_target instrument1 groundstation2)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 star4)
	(supports instrument2 infrared0)
	(calibration_target instrument2 groundstation2)
	(on_board instrument2 satellite1)
	(power_avail satellite1)
	(pointing satellite1 phenomenon8)
	(supports instrument3 infrared0)
	(supports instrument3 infrared1)
	(supports instrument3 image3)
	(calibration_target instrument3 star4)
	(supports instrument4 infrared1)
	(calibration_target instrument4 star1)
	(supports instrument5 infrared1)
	(supports instrument5 image3)
	(calibration_target instrument5 groundstation0)
	(supports instrument6 infrared0)
	(supports instrument6 infrared1)
	(calibration_target instrument6 groundstation2)
	(on_board instrument3 satellite2)
	(on_board instrument4 satellite2)
	(on_board instrument5 satellite2)
	(on_board instrument6 satellite2)
	(power_avail satellite2)
	(pointing satellite2 phenomenon6)
	(supports instrument7 thermograph2)
	(supports instrument7 image4)
	(supports instrument7 image3)
	(calibration_target instrument7 star1)
	(supports instrument8 infrared1)
	(supports instrument8 image4)
	(calibration_target instrument8 star4)
	(supports instrument9 infrared1)
	(calibration_target instrument9 groundstation0)
	(supports instrument10 image4)
	(calibration_target instrument10 groundstation3)
	(on_board instrument7 satellite3)
	(on_board instrument8 satellite3)
	(on_board instrument9 satellite3)
	(on_board instrument10 satellite3)
	(power_avail satellite3)
	(pointing satellite3 phenomenon8)
	(supports instrument11 thermograph2)
	(calibration_target instrument11 star1)
	(supports instrument12 thermograph2)
	(calibration_target instrument12 groundstation3)
	(on_board instrument11 satellite4)
	(on_board instrument12 satellite4)
	(power_avail satellite4)
	(pointing satellite4 phenomenon9)
	(supports instrument13 thermograph2)
	(supports instrument13 image3)
	(calibration_target instrument13 star1)
	(on_board instrument13 satellite5)
	(power_avail satellite5)
	(pointing satellite5 groundstation3)
)
(:goal (and
	(pointing satellite1 groundstation2)
	(pointing satellite5 groundstation0)
	(have_image planet5 infrared0)
	(have_image phenomenon6 thermograph2)
	(have_image planet7 infrared0)
	(have_image phenomenon8 image4)
	(have_image phenomenon9 infrared1)
	(have_image star10 infrared1)
	(have_image star11 image3)
))

)
