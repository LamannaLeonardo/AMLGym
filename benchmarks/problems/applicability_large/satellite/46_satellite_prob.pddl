(define (problem strips_sat_x_1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	satellite1 - satellite
	instrument1 - instrument
	instrument2 - instrument
	satellite2 - satellite
	instrument3 - instrument
	instrument4 - instrument
	satellite3 - satellite
	instrument5 - instrument
	satellite4 - satellite
	instrument6 - instrument
	instrument7 - instrument
	satellite5 - satellite
	instrument8 - instrument
	thermograph2 - mode
	image0 - mode
	thermograph1 - mode
	image3 - mode
	groundstation1 - direction
	star0 - direction
	star2 - direction
	groundstation4 - direction
	groundstation3 - direction
	phenomenon5 - direction
	phenomenon6 - direction
	star7 - direction
	star8 - direction
	star9 - direction
	star10 - direction
	phenomenon11 - direction
)
(:init
	(supports instrument0 thermograph1)
	(calibration_target instrument0 groundstation4)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 star9)
	(supports instrument1 thermograph1)
	(supports instrument1 image3)
	(supports instrument1 thermograph2)
	(calibration_target instrument1 groundstation4)
	(supports instrument2 image3)
	(calibration_target instrument2 star0)
	(on_board instrument1 satellite1)
	(on_board instrument2 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star7)
	(supports instrument3 image0)
	(calibration_target instrument3 groundstation1)
	(supports instrument4 thermograph1)
	(supports instrument4 image3)
	(supports instrument4 thermograph2)
	(calibration_target instrument4 star0)
	(on_board instrument3 satellite2)
	(on_board instrument4 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star0)
	(supports instrument5 thermograph1)
	(supports instrument5 image3)
	(supports instrument5 thermograph2)
	(calibration_target instrument5 star0)
	(on_board instrument5 satellite3)
	(power_avail satellite3)
	(pointing satellite3 groundstation4)
	(supports instrument6 thermograph2)
	(calibration_target instrument6 star2)
	(supports instrument7 image0)
	(supports instrument7 thermograph2)
	(supports instrument7 thermograph1)
	(calibration_target instrument7 groundstation4)
	(on_board instrument6 satellite4)
	(on_board instrument7 satellite4)
	(power_avail satellite4)
	(pointing satellite4 star7)
	(supports instrument8 thermograph1)
	(supports instrument8 image3)
	(calibration_target instrument8 groundstation3)
	(on_board instrument8 satellite5)
	(power_avail satellite5)
	(pointing satellite5 groundstation1)
)
(:goal (and
	(pointing satellite0 star7)
	(pointing satellite2 star8)
	(pointing satellite4 star8)
	(have_image phenomenon5 image3)
	(have_image phenomenon6 thermograph1)
	(have_image star7 image3)
	(have_image star8 thermograph2)
	(have_image star9 thermograph1)
	(have_image star10 image3)
	(have_image phenomenon11 thermograph2)
))

)
