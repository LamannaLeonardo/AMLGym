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
	thermograph2 - mode
	spectrograph3 - mode
	image0 - mode
	thermograph1 - mode
	star3 - direction
	star2 - direction
	star0 - direction
	groundstation1 - direction
	star4 - direction
	phenomenon5 - direction
	star6 - direction
	planet7 - direction
	star8 - direction
	star9 - direction
)
(:init
	(supports instrument0 spectrograph3)
	(calibration_target instrument0 star2)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 star0)
	(supports instrument1 image0)
	(calibration_target instrument1 star3)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 groundstation1)
	(supports instrument2 thermograph2)
	(calibration_target instrument2 star3)
	(supports instrument3 spectrograph3)
	(supports instrument3 thermograph1)
	(supports instrument3 thermograph2)
	(calibration_target instrument3 star3)
	(on_board instrument2 satellite2)
	(on_board instrument3 satellite2)
	(power_avail satellite2)
	(pointing satellite2 groundstation1)
	(supports instrument4 thermograph2)
	(calibration_target instrument4 star2)
	(supports instrument5 image0)
	(calibration_target instrument5 star0)
	(on_board instrument4 satellite3)
	(on_board instrument5 satellite3)
	(power_avail satellite3)
	(pointing satellite3 star4)
	(supports instrument6 thermograph2)
	(calibration_target instrument6 groundstation1)
	(on_board instrument6 satellite4)
	(power_avail satellite4)
	(pointing satellite4 star8)
)
(:goal (and
	(pointing satellite1 star0)
	(pointing satellite3 planet7)
	(pointing satellite4 groundstation1)
	(have_image star4 thermograph1)
	(have_image phenomenon5 thermograph2)
	(have_image star6 image0)
	(have_image planet7 image0)
	(have_image star8 thermograph1)
	(have_image star9 thermograph2)
))

)
