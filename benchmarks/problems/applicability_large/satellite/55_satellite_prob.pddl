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
	instrument5 - instrument
	satellite4 - satellite
	instrument6 - instrument
	image1 - mode
	image2 - mode
	thermograph0 - mode
	infrared3 - mode
	star2 - direction
	groundstation3 - direction
	star1 - direction
	groundstation0 - direction
	phenomenon4 - direction
	phenomenon5 - direction
	star6 - direction
	planet7 - direction
	planet8 - direction
	phenomenon9 - direction
)
(:init
	(supports instrument0 image1)
	(supports instrument0 infrared3)
	(calibration_target instrument0 groundstation0)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 star6)
	(supports instrument1 image1)
	(supports instrument1 thermograph0)
	(supports instrument1 infrared3)
	(calibration_target instrument1 groundstation3)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star1)
	(supports instrument2 image2)
	(supports instrument2 thermograph0)
	(calibration_target instrument2 groundstation0)
	(supports instrument3 image2)
	(supports instrument3 infrared3)
	(supports instrument3 thermograph0)
	(calibration_target instrument3 star1)
	(on_board instrument2 satellite2)
	(on_board instrument3 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star1)
	(supports instrument4 image2)
	(calibration_target instrument4 star1)
	(supports instrument5 image1)
	(supports instrument5 thermograph0)
	(calibration_target instrument5 star1)
	(on_board instrument4 satellite3)
	(on_board instrument5 satellite3)
	(power_avail satellite3)
	(pointing satellite3 star6)
	(supports instrument6 image2)
	(supports instrument6 infrared3)
	(calibration_target instrument6 groundstation0)
	(on_board instrument6 satellite4)
	(power_avail satellite4)
	(pointing satellite4 phenomenon4)
)
(:goal (and
	(pointing satellite1 phenomenon9)
	(pointing satellite3 phenomenon4)
	(have_image phenomenon4 image1)
	(have_image phenomenon5 image2)
	(have_image star6 image1)
	(have_image planet7 image1)
	(have_image planet8 thermograph0)
	(have_image phenomenon9 infrared3)
))

)
