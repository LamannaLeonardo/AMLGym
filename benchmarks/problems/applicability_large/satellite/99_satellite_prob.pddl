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
	satellite4 - satellite
	instrument7 - instrument
	satellite5 - satellite
	instrument8 - instrument
	instrument9 - instrument
	instrument10 - instrument
	satellite6 - satellite
	instrument11 - instrument
	instrument12 - instrument
	instrument13 - instrument
	infrared5 - mode
	image0 - mode
	thermograph4 - mode
	infrared3 - mode
	infrared1 - mode
	thermograph2 - mode
	star2 - direction
	star1 - direction
	groundstation4 - direction
	star0 - direction
	groundstation5 - direction
	star3 - direction
	phenomenon6 - direction
	planet7 - direction
	planet8 - direction
	phenomenon9 - direction
	phenomenon10 - direction
	phenomenon11 - direction
	phenomenon12 - direction
	star13 - direction
)
(:init
	(supports instrument0 thermograph2)
	(calibration_target instrument0 star0)
	(calibration_target instrument0 groundstation5)
	(supports instrument1 infrared5)
	(supports instrument1 infrared1)
	(calibration_target instrument1 star1)
	(calibration_target instrument1 groundstation4)
	(supports instrument2 image0)
	(calibration_target instrument2 star3)
	(calibration_target instrument2 star1)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(on_board instrument2 satellite0)
	(power_avail satellite0)
	(pointing satellite0 groundstation5)
	(supports instrument3 infrared5)
	(supports instrument3 thermograph4)
	(supports instrument3 infrared3)
	(calibration_target instrument3 star2)
	(on_board instrument3 satellite1)
	(power_avail satellite1)
	(pointing satellite1 planet7)
	(supports instrument4 infrared3)
	(supports instrument4 image0)
	(calibration_target instrument4 groundstation5)
	(calibration_target instrument4 star0)
	(on_board instrument4 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star1)
	(supports instrument5 thermograph2)
	(calibration_target instrument5 star0)
	(supports instrument6 thermograph4)
	(supports instrument6 infrared5)
	(calibration_target instrument6 star3)
	(on_board instrument5 satellite3)
	(on_board instrument6 satellite3)
	(power_avail satellite3)
	(pointing satellite3 groundstation4)
	(supports instrument7 image0)
	(supports instrument7 infrared1)
	(supports instrument7 thermograph4)
	(calibration_target instrument7 star3)
	(on_board instrument7 satellite4)
	(power_avail satellite4)
	(pointing satellite4 phenomenon9)
	(supports instrument8 infrared5)
	(supports instrument8 infrared1)
	(calibration_target instrument8 star3)
	(calibration_target instrument8 star0)
	(supports instrument9 image0)
	(calibration_target instrument9 groundstation5)
	(supports instrument10 infrared3)
	(supports instrument10 image0)
	(calibration_target instrument10 groundstation5)
	(calibration_target instrument10 star1)
	(on_board instrument8 satellite5)
	(on_board instrument9 satellite5)
	(on_board instrument10 satellite5)
	(power_avail satellite5)
	(pointing satellite5 star2)
	(supports instrument11 infrared5)
	(supports instrument11 infrared1)
	(calibration_target instrument11 groundstation5)
	(calibration_target instrument11 groundstation4)
	(supports instrument12 thermograph4)
	(supports instrument12 thermograph2)
	(supports instrument12 image0)
	(calibration_target instrument12 star0)
	(calibration_target instrument12 groundstation4)
	(supports instrument13 infrared5)
	(supports instrument13 image0)
	(supports instrument13 thermograph4)
	(calibration_target instrument13 star3)
	(calibration_target instrument13 groundstation5)
	(on_board instrument11 satellite6)
	(on_board instrument12 satellite6)
	(on_board instrument13 satellite6)
	(power_avail satellite6)
	(pointing satellite6 phenomenon11)
)
(:goal (and
	(pointing satellite1 groundstation4)
	(pointing satellite2 star13)
	(pointing satellite3 phenomenon9)
	(pointing satellite6 phenomenon6)
	(have_image phenomenon6 thermograph4)
	(have_image planet7 infrared3)
	(have_image planet8 image0)
	(have_image planet8 thermograph2)
	(have_image phenomenon9 infrared1)
	(have_image phenomenon10 infrared5)
	(have_image phenomenon11 thermograph4)
	(have_image phenomenon12 infrared1)
	(have_image phenomenon12 infrared3)
	(have_image star13 infrared5)
	(have_image star13 image0)
))

)
