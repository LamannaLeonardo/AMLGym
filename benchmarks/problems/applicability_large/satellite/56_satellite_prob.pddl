(define (problem strips_sat_x_1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	satellite1 - satellite
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
	instrument9 - instrument
	spectrograph2 - mode
	thermograph1 - mode
	spectrograph3 - mode
	spectrograph0 - mode
	groundstation0 - direction
	star2 - direction
	groundstation3 - direction
	groundstation4 - direction
	star1 - direction
	star5 - direction
	star6 - direction
	star7 - direction
	star8 - direction
	star9 - direction
	star10 - direction
	planet11 - direction
)
(:init
	(supports instrument0 thermograph1)
	(supports instrument0 spectrograph0)
	(supports instrument0 spectrograph3)
	(calibration_target instrument0 groundstation4)
	(supports instrument1 spectrograph3)
	(supports instrument1 spectrograph2)
	(supports instrument1 thermograph1)
	(calibration_target instrument1 groundstation4)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 groundstation0)
	(supports instrument2 thermograph1)
	(supports instrument2 spectrograph2)
	(supports instrument2 spectrograph0)
	(calibration_target instrument2 star1)
	(on_board instrument2 satellite1)
	(power_avail satellite1)
	(pointing satellite1 groundstation0)
	(supports instrument3 spectrograph3)
	(supports instrument3 spectrograph2)
	(supports instrument3 thermograph1)
	(calibration_target instrument3 star1)
	(supports instrument4 spectrograph2)
	(calibration_target instrument4 groundstation3)
	(on_board instrument3 satellite2)
	(on_board instrument4 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star10)
	(supports instrument5 spectrograph2)
	(supports instrument5 spectrograph3)
	(calibration_target instrument5 groundstation3)
	(on_board instrument5 satellite3)
	(power_avail satellite3)
	(pointing satellite3 planet11)
	(supports instrument6 spectrograph0)
	(calibration_target instrument6 star1)
	(supports instrument7 spectrograph0)
	(supports instrument7 spectrograph2)
	(supports instrument7 spectrograph3)
	(calibration_target instrument7 groundstation4)
	(on_board instrument6 satellite4)
	(on_board instrument7 satellite4)
	(power_avail satellite4)
	(pointing satellite4 star9)
	(supports instrument8 spectrograph3)
	(calibration_target instrument8 groundstation4)
	(supports instrument9 spectrograph0)
	(supports instrument9 spectrograph3)
	(calibration_target instrument9 star1)
	(on_board instrument8 satellite5)
	(on_board instrument9 satellite5)
	(power_avail satellite5)
	(pointing satellite5 star2)
)
(:goal (and
	(pointing satellite2 planet11)
	(pointing satellite5 star2)
	(have_image star5 spectrograph3)
	(have_image star6 spectrograph3)
	(have_image star7 spectrograph3)
	(have_image star8 spectrograph0)
	(have_image star9 spectrograph3)
	(have_image star10 thermograph1)
	(have_image planet11 spectrograph3)
))

)
