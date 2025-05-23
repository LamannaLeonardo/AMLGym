(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	instrument2 - instrument
	instrument3 - instrument
	satellite1 - satellite
	instrument4 - instrument
	instrument5 - instrument
	instrument6 - instrument
	satellite2 - satellite
	instrument7 - instrument
	instrument8 - instrument
	instrument9 - instrument
	satellite3 - satellite
	instrument10 - instrument
	satellite4 - satellite
	instrument11 - instrument
	instrument12 - instrument
	instrument13 - instrument
	instrument14 - instrument
	satellite5 - satellite
	instrument15 - instrument
	instrument16 - instrument
	infrared0 - mode
	infrared1 - mode
	thermograph2 - mode
	image3 - mode
	groundstation4 - direction
	star1 - direction
	star3 - direction
	groundstation2 - direction
	star0 - direction
	phenomenon5 - direction
	planet6 - direction
	star7 - direction
	phenomenon8 - direction
	phenomenon9 - direction
	phenomenon10 - direction
	phenomenon11 - direction
)
(:init
	(supports instrument0 image3)
	(supports instrument0 thermograph2)
	(supports instrument0 infrared0)
	(calibration_target instrument0 star3)
	(supports instrument1 infrared0)
	(supports instrument1 image3)
	(supports instrument1 thermograph2)
	(calibration_target instrument1 star1)
	(supports instrument2 image3)
	(calibration_target instrument2 star3)
	(supports instrument3 image3)
	(calibration_target instrument3 groundstation4)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(on_board instrument2 satellite0)
	(on_board instrument3 satellite0)
	(power_avail satellite0)
	(pointing satellite0 planet6)
	(supports instrument4 image3)
	(supports instrument4 thermograph2)
	(supports instrument4 infrared1)
	(calibration_target instrument4 star0)
	(supports instrument5 infrared1)
	(supports instrument5 thermograph2)
	(supports instrument5 image3)
	(calibration_target instrument5 star0)
	(supports instrument6 image3)
	(calibration_target instrument6 star0)
	(on_board instrument4 satellite1)
	(on_board instrument5 satellite1)
	(on_board instrument6 satellite1)
	(power_avail satellite1)
	(pointing satellite1 phenomenon9)
	(supports instrument7 thermograph2)
	(supports instrument7 infrared1)
	(supports instrument7 infrared0)
	(calibration_target instrument7 groundstation2)
	(supports instrument8 image3)
	(supports instrument8 infrared0)
	(calibration_target instrument8 star1)
	(supports instrument9 infrared0)
	(supports instrument9 image3)
	(supports instrument9 thermograph2)
	(calibration_target instrument9 groundstation4)
	(on_board instrument7 satellite2)
	(on_board instrument8 satellite2)
	(on_board instrument9 satellite2)
	(power_avail satellite2)
	(pointing satellite2 groundstation4)
	(supports instrument10 infrared0)
	(supports instrument10 image3)
	(supports instrument10 thermograph2)
	(calibration_target instrument10 star0)
	(on_board instrument10 satellite3)
	(power_avail satellite3)
	(pointing satellite3 phenomenon9)
	(supports instrument11 thermograph2)
	(supports instrument11 infrared0)
	(supports instrument11 image3)
	(calibration_target instrument11 star1)
	(supports instrument12 thermograph2)
	(supports instrument12 infrared1)
	(calibration_target instrument12 star0)
	(supports instrument13 infrared1)
	(supports instrument13 thermograph2)
	(calibration_target instrument13 star1)
	(supports instrument14 image3)
	(supports instrument14 thermograph2)
	(calibration_target instrument14 star3)
	(on_board instrument11 satellite4)
	(on_board instrument12 satellite4)
	(on_board instrument13 satellite4)
	(on_board instrument14 satellite4)
	(power_avail satellite4)
	(pointing satellite4 star3)
	(supports instrument15 infrared0)
	(supports instrument15 infrared1)
	(supports instrument15 image3)
	(calibration_target instrument15 groundstation2)
	(supports instrument16 image3)
	(supports instrument16 infrared0)
	(calibration_target instrument16 star0)
	(on_board instrument15 satellite5)
	(on_board instrument16 satellite5)
	(power_avail satellite5)
	(pointing satellite5 planet6)
)
(:goal (and
	(pointing satellite0 star0)
	(pointing satellite2 star0)
	(pointing satellite3 phenomenon5)
	(have_image phenomenon5 image3)
	(have_image planet6 image3)
	(have_image star7 infrared1)
	(have_image phenomenon8 image3)
	(have_image phenomenon9 infrared1)
	(have_image phenomenon10 infrared1)
	(have_image phenomenon11 thermograph2)
))

)
