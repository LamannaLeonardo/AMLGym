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
	satellite4 - satellite
	instrument4 - instrument
	instrument5 - instrument
	satellite5 - satellite
	instrument6 - instrument
	thermograph1 - mode
	spectrograph2 - mode
	spectrograph4 - mode
	image0 - mode
	spectrograph3 - mode
	star2 - direction
	star3 - direction
	groundstation0 - direction
	groundstation1 - direction
	star4 - direction
	planet5 - direction
	star6 - direction
	planet7 - direction
	star8 - direction
	planet9 - direction
	star10 - direction
	star11 - direction
)
(:init
	(supports instrument0 thermograph1)
	(calibration_target instrument0 star3)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 groundstation0)
	(supports instrument1 spectrograph2)
	(supports instrument1 thermograph1)
	(calibration_target instrument1 star3)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star2)
	(supports instrument2 thermograph1)
	(supports instrument2 spectrograph3)
	(supports instrument2 spectrograph4)
	(calibration_target instrument2 groundstation1)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star3)
	(supports instrument3 image0)
	(calibration_target instrument3 star4)
	(on_board instrument3 satellite3)
	(power_avail satellite3)
	(pointing satellite3 planet9)
	(supports instrument4 spectrograph2)
	(supports instrument4 spectrograph3)
	(supports instrument4 image0)
	(calibration_target instrument4 groundstation0)
	(supports instrument5 thermograph1)
	(supports instrument5 image0)
	(calibration_target instrument5 groundstation1)
	(on_board instrument4 satellite4)
	(on_board instrument5 satellite4)
	(power_avail satellite4)
	(pointing satellite4 star2)
	(supports instrument6 spectrograph3)
	(calibration_target instrument6 star4)
	(on_board instrument6 satellite5)
	(power_avail satellite5)
	(pointing satellite5 star4)
)
(:goal (and
	(pointing satellite0 planet5)
	(pointing satellite4 star4)
	(have_image planet5 spectrograph3)
	(have_image star6 spectrograph4)
	(have_image planet7 image0)
	(have_image star8 spectrograph2)
	(have_image planet9 thermograph1)
	(have_image star10 spectrograph2)
	(have_image star11 spectrograph2)
))

)
