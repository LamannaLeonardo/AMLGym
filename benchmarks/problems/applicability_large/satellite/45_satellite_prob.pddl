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
	satellite3 - satellite
	instrument5 - instrument
	instrument6 - instrument
	satellite4 - satellite
	instrument7 - instrument
	image1 - mode
	infrared3 - mode
	thermograph2 - mode
	image0 - mode
	star2 - direction
	star3 - direction
	groundstation1 - direction
	star0 - direction
	planet4 - direction
	planet5 - direction
	star6 - direction
	star7 - direction
	star8 - direction
	planet9 - direction
)
(:init
	(supports instrument0 infrared3)
	(supports instrument0 image1)
	(supports instrument0 thermograph2)
	(calibration_target instrument0 groundstation1)
	(supports instrument1 image0)
	(supports instrument1 image1)
	(calibration_target instrument1 star0)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 planet4)
	(supports instrument2 infrared3)
	(supports instrument2 thermograph2)
	(supports instrument2 image1)
	(calibration_target instrument2 star3)
	(supports instrument3 image0)
	(calibration_target instrument3 star3)
	(on_board instrument2 satellite1)
	(on_board instrument3 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star0)
	(supports instrument4 image0)
	(calibration_target instrument4 groundstation1)
	(on_board instrument4 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star8)
	(supports instrument5 image1)
	(supports instrument5 image0)
	(supports instrument5 thermograph2)
	(calibration_target instrument5 groundstation1)
	(supports instrument6 infrared3)
	(supports instrument6 thermograph2)
	(calibration_target instrument6 groundstation1)
	(on_board instrument5 satellite3)
	(on_board instrument6 satellite3)
	(power_avail satellite3)
	(pointing satellite3 star6)
	(supports instrument7 image0)
	(supports instrument7 infrared3)
	(supports instrument7 thermograph2)
	(calibration_target instrument7 star0)
	(on_board instrument7 satellite4)
	(power_avail satellite4)
	(pointing satellite4 star3)
)
(:goal (and
	(pointing satellite2 planet9)
	(pointing satellite3 groundstation1)
	(have_image planet4 thermograph2)
	(have_image planet5 thermograph2)
	(have_image star6 image1)
	(have_image star7 infrared3)
	(have_image star8 image1)
	(have_image planet9 infrared3)
))

)
