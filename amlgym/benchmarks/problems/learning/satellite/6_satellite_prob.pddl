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
	instrument7 - instrument
	satellite5 - satellite
	instrument8 - instrument
	image1 - mode
	image3 - mode
	thermograph2 - mode
	thermograph0 - mode
	groundstation1 - direction
	groundstation3 - direction
	star2 - direction
	star4 - direction
	groundstation0 - direction
	star5 - direction
	planet6 - direction
	planet7 - direction
	planet8 - direction
	star9 - direction
	star10 - direction
	planet11 - direction
)
(:init
	(supports instrument0 thermograph2)
	(calibration_target instrument0 star4)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 planet7)
	(supports instrument1 image3)
	(supports instrument1 thermograph2)
	(supports instrument1 image1)
	(supports instrument1 thermograph0)
	(calibration_target instrument1 star4)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star10)
	(supports instrument2 thermograph2)
	(calibration_target instrument2 groundstation1)
	(supports instrument3 image1)
	(supports instrument3 image3)
	(calibration_target instrument3 groundstation0)
	(on_board instrument2 satellite2)
	(on_board instrument3 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star2)
	(supports instrument4 image3)
	(calibration_target instrument4 groundstation3)
	(supports instrument5 thermograph2)
	(calibration_target instrument5 star2)
	(on_board instrument4 satellite3)
	(on_board instrument5 satellite3)
	(power_avail satellite3)
	(pointing satellite3 groundstation0)
	(supports instrument6 thermograph2)
	(calibration_target instrument6 groundstation0)
	(supports instrument7 image1)
	(calibration_target instrument7 star4)
	(on_board instrument6 satellite4)
	(on_board instrument7 satellite4)
	(power_avail satellite4)
	(pointing satellite4 groundstation0)
	(supports instrument8 thermograph2)
	(supports instrument8 image1)
	(calibration_target instrument8 groundstation0)
	(on_board instrument8 satellite5)
	(power_avail satellite5)
	(pointing satellite5 groundstation1)
)
(:goal (and
	(pointing satellite0 star2)
	(pointing satellite2 star9)
	(pointing satellite4 groundstation1)
	(pointing satellite5 planet11)
	(have_image star5 thermograph0)
	(have_image planet6 image3)
	(have_image planet7 thermograph0)
	(have_image planet8 thermograph0)
	(have_image star9 image3)
	(have_image star10 thermograph0)
	(have_image planet11 image1)
))

)
