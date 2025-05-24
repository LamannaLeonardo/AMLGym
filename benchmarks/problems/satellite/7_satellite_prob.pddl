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
	instrument5 - instrument
	satellite3 - satellite
	instrument6 - instrument
	satellite4 - satellite
	instrument7 - instrument
	instrument8 - instrument
	satellite5 - satellite
	instrument9 - instrument
	thermograph2 - mode
	spectrograph4 - mode
	infrared1 - mode
	thermograph0 - mode
	infrared3 - mode
	groundstation1 - direction
	groundstation4 - direction
	star0 - direction
	groundstation3 - direction
	star2 - direction
	star5 - direction
	star6 - direction
	phenomenon7 - direction
	star8 - direction
	star9 - direction
	planet10 - direction
	phenomenon11 - direction
)
(:init
	(supports instrument0 thermograph0)
	(supports instrument0 infrared1)
	(calibration_target instrument0 star0)
	(supports instrument1 thermograph0)
	(calibration_target instrument1 star0)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 groundstation1)
	(supports instrument2 spectrograph4)
	(calibration_target instrument2 groundstation3)
	(supports instrument3 spectrograph4)
	(supports instrument3 thermograph2)
	(supports instrument3 infrared1)
	(calibration_target instrument3 groundstation4)
	(on_board instrument2 satellite1)
	(on_board instrument3 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star8)
	(supports instrument4 thermograph0)
	(supports instrument4 infrared1)
	(calibration_target instrument4 star0)
	(supports instrument5 infrared3)
	(supports instrument5 spectrograph4)
	(supports instrument5 thermograph2)
	(calibration_target instrument5 groundstation1)
	(on_board instrument4 satellite2)
	(on_board instrument5 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star5)
	(supports instrument6 infrared1)
	(calibration_target instrument6 groundstation4)
	(on_board instrument6 satellite3)
	(power_avail satellite3)
	(pointing satellite3 star9)
	(supports instrument7 thermograph0)
	(calibration_target instrument7 star0)
	(supports instrument8 infrared1)
	(calibration_target instrument8 groundstation3)
	(on_board instrument7 satellite4)
	(on_board instrument8 satellite4)
	(power_avail satellite4)
	(pointing satellite4 star8)
	(supports instrument9 infrared1)
	(supports instrument9 infrared3)
	(supports instrument9 thermograph0)
	(calibration_target instrument9 star2)
	(on_board instrument9 satellite5)
	(power_avail satellite5)
	(pointing satellite5 groundstation4)
)
(:goal (and
	(pointing satellite1 phenomenon11)
	(pointing satellite5 star0)
	(have_image star5 thermograph0)
	(have_image star6 infrared3)
	(have_image phenomenon7 infrared1)
	(have_image star8 spectrograph4)
	(have_image star9 thermograph2)
	(have_image planet10 infrared3)
	(have_image phenomenon11 thermograph0)
))

)
