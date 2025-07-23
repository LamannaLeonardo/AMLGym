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
	instrument9 - instrument
	infrared2 - mode
	infrared1 - mode
	spectrograph3 - mode
	thermograph0 - mode
	groundstation3 - direction
	groundstation1 - direction
	star2 - direction
	star4 - direction
	groundstation0 - direction
	planet5 - direction
	star6 - direction
	star7 - direction
	star8 - direction
	planet9 - direction
	star10 - direction
	planet11 - direction
)
(:init
	(supports instrument0 thermograph0)
	(calibration_target instrument0 groundstation1)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 star4)
	(supports instrument1 infrared1)
	(supports instrument1 spectrograph3)
	(supports instrument1 infrared2)
	(calibration_target instrument1 groundstation3)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 planet11)
	(supports instrument2 infrared2)
	(supports instrument2 spectrograph3)
	(calibration_target instrument2 star4)
	(supports instrument3 infrared1)
	(supports instrument3 infrared2)
	(supports instrument3 spectrograph3)
	(calibration_target instrument3 groundstation3)
	(on_board instrument2 satellite2)
	(on_board instrument3 satellite2)
	(power_avail satellite2)
	(pointing satellite2 groundstation0)
	(supports instrument4 infrared2)
	(supports instrument4 thermograph0)
	(supports instrument4 infrared1)
	(calibration_target instrument4 star2)
	(supports instrument5 infrared2)
	(supports instrument5 spectrograph3)
	(calibration_target instrument5 groundstation1)
	(on_board instrument4 satellite3)
	(on_board instrument5 satellite3)
	(power_avail satellite3)
	(pointing satellite3 planet9)
	(supports instrument6 thermograph0)
	(supports instrument6 spectrograph3)
	(supports instrument6 infrared1)
	(calibration_target instrument6 star4)
	(supports instrument7 spectrograph3)
	(supports instrument7 infrared2)
	(calibration_target instrument7 star2)
	(on_board instrument6 satellite4)
	(on_board instrument7 satellite4)
	(power_avail satellite4)
	(pointing satellite4 planet9)
	(supports instrument8 infrared2)
	(supports instrument8 spectrograph3)
	(supports instrument8 infrared1)
	(calibration_target instrument8 star4)
	(supports instrument9 infrared2)
	(calibration_target instrument9 groundstation0)
	(on_board instrument8 satellite5)
	(on_board instrument9 satellite5)
	(power_avail satellite5)
	(pointing satellite5 star8)
)
(:goal (and
	(pointing satellite1 planet5)
	(pointing satellite2 planet9)
	(pointing satellite3 star6)
	(pointing satellite4 planet5)
	(have_image planet5 thermograph0)
	(have_image star6 infrared2)
	(have_image star7 thermograph0)
	(have_image star8 infrared2)
	(have_image planet9 infrared2)
	(have_image star10 infrared2)
	(have_image planet11 spectrograph3)
))

)
