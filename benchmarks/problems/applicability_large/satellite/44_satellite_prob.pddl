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
	instrument8 - instrument
	spectrograph0 - mode
	image1 - mode
	thermograph2 - mode
	star3 - direction
	star0 - direction
	star2 - direction
	star1 - direction
	phenomenon4 - direction
	phenomenon5 - direction
	planet6 - direction
	planet7 - direction
	star8 - direction
	phenomenon9 - direction
)
(:init
	(supports instrument0 image1)
	(calibration_target instrument0 star2)
	(supports instrument1 thermograph2)
	(supports instrument1 image1)
	(supports instrument1 spectrograph0)
	(calibration_target instrument1 star3)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 phenomenon5)
	(supports instrument2 image1)
	(calibration_target instrument2 star1)
	(supports instrument3 thermograph2)
	(calibration_target instrument3 star3)
	(on_board instrument2 satellite1)
	(on_board instrument3 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star3)
	(supports instrument4 image1)
	(supports instrument4 spectrograph0)
	(supports instrument4 thermograph2)
	(calibration_target instrument4 star3)
	(on_board instrument4 satellite2)
	(power_avail satellite2)
	(pointing satellite2 phenomenon5)
	(supports instrument5 image1)
	(supports instrument5 thermograph2)
	(calibration_target instrument5 star0)
	(supports instrument6 spectrograph0)
	(supports instrument6 thermograph2)
	(calibration_target instrument6 star0)
	(on_board instrument5 satellite3)
	(on_board instrument6 satellite3)
	(power_avail satellite3)
	(pointing satellite3 star1)
	(supports instrument7 thermograph2)
	(calibration_target instrument7 star2)
	(supports instrument8 thermograph2)
	(supports instrument8 spectrograph0)
	(supports instrument8 image1)
	(calibration_target instrument8 star1)
	(on_board instrument7 satellite4)
	(on_board instrument8 satellite4)
	(power_avail satellite4)
	(pointing satellite4 star0)
)
(:goal (and
	(pointing satellite4 phenomenon5)
	(have_image phenomenon4 spectrograph0)
	(have_image phenomenon5 image1)
	(have_image planet6 spectrograph0)
	(have_image planet7 thermograph2)
	(have_image star8 thermograph2)
	(have_image phenomenon9 spectrograph0)
))

)
