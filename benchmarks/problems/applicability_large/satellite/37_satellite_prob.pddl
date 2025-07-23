(define (problem strips_sat_x_1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	satellite1 - satellite
	instrument1 - instrument
	satellite2 - satellite
	instrument2 - instrument
	instrument3 - instrument
	satellite3 - satellite
	instrument4 - instrument
	satellite4 - satellite
	instrument5 - instrument
	instrument6 - instrument
	satellite5 - satellite
	instrument7 - instrument
	instrument8 - instrument
	infrared4 - mode
	image3 - mode
	image1 - mode
	image0 - mode
	thermograph2 - mode
	star3 - direction
	star1 - direction
	star2 - direction
	star0 - direction
	groundstation4 - direction
	phenomenon5 - direction
	star6 - direction
	phenomenon7 - direction
	phenomenon8 - direction
	planet9 - direction
	planet10 - direction
	phenomenon11 - direction
)
(:init
	(supports instrument0 image0)
	(supports instrument0 thermograph2)
	(calibration_target instrument0 star1)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 planet10)
	(supports instrument1 thermograph2)
	(supports instrument1 infrared4)
	(supports instrument1 image1)
	(calibration_target instrument1 star3)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star6)
	(supports instrument2 image0)
	(supports instrument2 infrared4)
	(calibration_target instrument2 star1)
	(supports instrument3 image3)
	(calibration_target instrument3 star1)
	(on_board instrument2 satellite2)
	(on_board instrument3 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star3)
	(supports instrument4 image3)
	(calibration_target instrument4 star2)
	(on_board instrument4 satellite3)
	(power_avail satellite3)
	(pointing satellite3 star6)
	(supports instrument5 image1)
	(calibration_target instrument5 star2)
	(supports instrument6 image1)
	(supports instrument6 infrared4)
	(supports instrument6 image3)
	(calibration_target instrument6 groundstation4)
	(on_board instrument5 satellite4)
	(on_board instrument6 satellite4)
	(power_avail satellite4)
	(pointing satellite4 planet10)
	(supports instrument7 image0)
	(supports instrument7 image3)
	(supports instrument7 infrared4)
	(calibration_target instrument7 star0)
	(supports instrument8 thermograph2)
	(calibration_target instrument8 groundstation4)
	(on_board instrument7 satellite5)
	(on_board instrument8 satellite5)
	(power_avail satellite5)
	(pointing satellite5 star1)
)
(:goal (and
	(pointing satellite0 star1)
	(pointing satellite2 star1)
	(pointing satellite3 groundstation4)
	(have_image phenomenon5 thermograph2)
	(have_image star6 image3)
	(have_image phenomenon7 image0)
	(have_image phenomenon8 image3)
	(have_image planet9 infrared4)
	(have_image planet10 infrared4)
	(have_image phenomenon11 infrared4)
))

)
