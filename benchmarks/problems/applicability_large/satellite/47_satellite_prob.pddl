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
	spectrograph0 - mode
	infrared4 - mode
	infrared1 - mode
	thermograph3 - mode
	thermograph2 - mode
	groundstation3 - direction
	star4 - direction
	groundstation0 - direction
	groundstation2 - direction
	groundstation1 - direction
	planet5 - direction
	planet6 - direction
	planet7 - direction
	planet8 - direction
	star9 - direction
	planet10 - direction
	star11 - direction
)
(:init
	(supports instrument0 spectrograph0)
	(supports instrument0 thermograph3)
	(supports instrument0 infrared1)
	(calibration_target instrument0 groundstation1)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 planet10)
	(supports instrument1 spectrograph0)
	(calibration_target instrument1 groundstation2)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 planet10)
	(supports instrument2 thermograph3)
	(supports instrument2 infrared4)
	(supports instrument2 spectrograph0)
	(calibration_target instrument2 groundstation0)
	(supports instrument3 thermograph3)
	(supports instrument3 spectrograph0)
	(supports instrument3 thermograph2)
	(calibration_target instrument3 star4)
	(on_board instrument2 satellite2)
	(on_board instrument3 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star4)
	(supports instrument4 infrared4)
	(calibration_target instrument4 groundstation0)
	(supports instrument5 thermograph3)
	(supports instrument5 infrared1)
	(calibration_target instrument5 star4)
	(on_board instrument4 satellite3)
	(on_board instrument5 satellite3)
	(power_avail satellite3)
	(pointing satellite3 planet10)
	(supports instrument6 spectrograph0)
	(calibration_target instrument6 groundstation0)
	(supports instrument7 infrared4)
	(calibration_target instrument7 groundstation0)
	(on_board instrument6 satellite4)
	(on_board instrument7 satellite4)
	(power_avail satellite4)
	(pointing satellite4 planet6)
	(supports instrument8 spectrograph0)
	(supports instrument8 infrared4)
	(supports instrument8 thermograph3)
	(calibration_target instrument8 groundstation2)
	(supports instrument9 infrared4)
	(supports instrument9 thermograph3)
	(supports instrument9 infrared1)
	(calibration_target instrument9 groundstation1)
	(on_board instrument8 satellite5)
	(on_board instrument9 satellite5)
	(power_avail satellite5)
	(pointing satellite5 star4)
)
(:goal (and
	(pointing satellite4 star11)
	(have_image planet5 spectrograph0)
	(have_image planet6 thermograph3)
	(have_image planet7 spectrograph0)
	(have_image planet8 spectrograph0)
	(have_image star9 infrared4)
	(have_image planet10 infrared1)
	(have_image star11 thermograph3)
))

)
