(define (problem strips_sat_x_1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	satellite1 - satellite
	instrument2 - instrument
	instrument3 - instrument
	satellite2 - satellite
	instrument4 - instrument
	instrument5 - instrument
	satellite3 - satellite
	instrument6 - instrument
	instrument7 - instrument
	satellite4 - satellite
	instrument8 - instrument
	satellite5 - satellite
	instrument9 - instrument
	instrument10 - instrument
	thermograph3 - mode
	image4 - mode
	image0 - mode
	infrared2 - mode
	infrared1 - mode
	star4 - direction
	groundstation0 - direction
	star2 - direction
	groundstation3 - direction
	star1 - direction
	phenomenon5 - direction
	planet6 - direction
	planet7 - direction
	planet8 - direction
	star9 - direction
	phenomenon10 - direction
	phenomenon11 - direction
)
(:init
	(supports instrument0 thermograph3)
	(calibration_target instrument0 groundstation0)
	(supports instrument1 infrared1)
	(supports instrument1 infrared2)
	(calibration_target instrument1 star2)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 phenomenon11)
	(supports instrument2 image0)
	(calibration_target instrument2 groundstation0)
	(supports instrument3 image4)
	(calibration_target instrument3 star1)
	(on_board instrument2 satellite1)
	(on_board instrument3 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star4)
	(supports instrument4 thermograph3)
	(calibration_target instrument4 groundstation0)
	(supports instrument5 infrared2)
	(supports instrument5 infrared1)
	(calibration_target instrument5 star2)
	(on_board instrument4 satellite2)
	(on_board instrument5 satellite2)
	(power_avail satellite2)
	(pointing satellite2 planet8)
	(supports instrument6 image0)
	(supports instrument6 image4)
	(supports instrument6 infrared2)
	(calibration_target instrument6 groundstation3)
	(supports instrument7 image4)
	(supports instrument7 infrared1)
	(supports instrument7 image0)
	(calibration_target instrument7 star1)
	(on_board instrument6 satellite3)
	(on_board instrument7 satellite3)
	(power_avail satellite3)
	(pointing satellite3 star4)
	(supports instrument8 infrared2)
	(supports instrument8 image0)
	(calibration_target instrument8 groundstation3)
	(on_board instrument8 satellite4)
	(power_avail satellite4)
	(pointing satellite4 groundstation3)
	(supports instrument9 thermograph3)
	(calibration_target instrument9 star1)
	(supports instrument10 infrared1)
	(supports instrument10 thermograph3)
	(supports instrument10 image4)
	(calibration_target instrument10 star1)
	(on_board instrument9 satellite5)
	(on_board instrument10 satellite5)
	(power_avail satellite5)
	(pointing satellite5 planet7)
)
(:goal (and
	(pointing satellite2 star9)
	(pointing satellite4 phenomenon11)
	(pointing satellite5 phenomenon11)
	(have_image phenomenon5 image4)
	(have_image planet6 infrared2)
	(have_image planet7 infrared2)
	(have_image planet8 image0)
	(have_image star9 infrared1)
	(have_image phenomenon10 thermograph3)
	(have_image phenomenon11 infrared2)
))

)
