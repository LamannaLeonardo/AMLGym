(define (problem strips_sat_x_1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	satellite1 - satellite
	instrument1 - instrument
	satellite2 - satellite
	instrument2 - instrument
	satellite3 - satellite
	instrument3 - instrument
	instrument4 - instrument
	satellite4 - satellite
	instrument5 - instrument
	instrument6 - instrument
	thermograph1 - mode
	thermograph3 - mode
	image0 - mode
	image2 - mode
	star1 - direction
	groundstation3 - direction
	star2 - direction
	star0 - direction
	star4 - direction
	star5 - direction
	star6 - direction
	planet7 - direction
	phenomenon8 - direction
	star9 - direction
)
(:init
	(supports instrument0 thermograph3)
	(supports instrument0 image2)
	(calibration_target instrument0 star2)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 star2)
	(supports instrument1 thermograph1)
	(calibration_target instrument1 star0)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star1)
	(supports instrument2 image0)
	(calibration_target instrument2 star0)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star9)
	(supports instrument3 image2)
	(calibration_target instrument3 star2)
	(supports instrument4 image0)
	(calibration_target instrument4 star0)
	(on_board instrument3 satellite3)
	(on_board instrument4 satellite3)
	(power_avail satellite3)
	(pointing satellite3 star5)
	(supports instrument5 image0)
	(supports instrument5 image2)
	(supports instrument5 thermograph1)
	(calibration_target instrument5 star2)
	(supports instrument6 image0)
	(supports instrument6 thermograph3)
	(calibration_target instrument6 star0)
	(on_board instrument5 satellite4)
	(on_board instrument6 satellite4)
	(power_avail satellite4)
	(pointing satellite4 star6)
)
(:goal (and
	(have_image star4 thermograph1)
	(have_image star5 thermograph3)
	(have_image star6 thermograph1)
	(have_image planet7 thermograph3)
	(have_image phenomenon8 thermograph3)
	(have_image star9 thermograph3)
))

)
