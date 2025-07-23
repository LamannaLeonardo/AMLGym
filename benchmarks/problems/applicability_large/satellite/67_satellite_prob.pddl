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
	satellite5 - satellite
	instrument6 - instrument
	instrument7 - instrument
	infrared0 - mode
	image1 - mode
	image4 - mode
	thermograph2 - mode
	infrared3 - mode
	groundstation1 - direction
	star4 - direction
	star2 - direction
	groundstation3 - direction
	groundstation0 - direction
	phenomenon5 - direction
	phenomenon6 - direction
	phenomenon7 - direction
	phenomenon8 - direction
	planet9 - direction
	star10 - direction
	planet11 - direction
)
(:init
	(supports instrument0 image4)
	(supports instrument0 infrared0)
	(calibration_target instrument0 groundstation3)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 planet9)
	(supports instrument1 infrared3)
	(supports instrument1 image1)
	(calibration_target instrument1 groundstation3)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 phenomenon8)
	(supports instrument2 infrared3)
	(supports instrument2 thermograph2)
	(supports instrument2 image1)
	(calibration_target instrument2 star2)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 phenomenon5)
	(supports instrument3 image1)
	(supports instrument3 image4)
	(supports instrument3 thermograph2)
	(calibration_target instrument3 star2)
	(supports instrument4 image4)
	(supports instrument4 thermograph2)
	(calibration_target instrument4 star2)
	(on_board instrument3 satellite3)
	(on_board instrument4 satellite3)
	(power_avail satellite3)
	(pointing satellite3 phenomenon7)
	(supports instrument5 infrared0)
	(supports instrument5 thermograph2)
	(calibration_target instrument5 groundstation3)
	(on_board instrument5 satellite4)
	(power_avail satellite4)
	(pointing satellite4 planet9)
	(supports instrument6 image1)
	(calibration_target instrument6 groundstation3)
	(supports instrument7 thermograph2)
	(calibration_target instrument7 groundstation0)
	(on_board instrument6 satellite5)
	(on_board instrument7 satellite5)
	(power_avail satellite5)
	(pointing satellite5 planet11)
)
(:goal (and
	(pointing satellite3 groundstation0)
	(have_image phenomenon5 thermograph2)
	(have_image phenomenon6 infrared3)
	(have_image phenomenon7 image4)
	(have_image phenomenon8 thermograph2)
	(have_image planet9 image1)
	(have_image star10 image4)
	(have_image planet11 infrared3)
))

)
