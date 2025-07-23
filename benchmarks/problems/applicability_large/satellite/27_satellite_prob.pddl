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
	satellite3 - satellite
	instrument4 - instrument
	satellite4 - satellite
	instrument5 - instrument
	instrument6 - instrument
	satellite5 - satellite
	instrument7 - instrument
	instrument8 - instrument
	image3 - mode
	spectrograph2 - mode
	thermograph1 - mode
	image4 - mode
	infrared0 - mode
	groundstation1 - direction
	star3 - direction
	groundstation2 - direction
	groundstation4 - direction
	star0 - direction
	planet5 - direction
	planet6 - direction
	planet7 - direction
	star8 - direction
	star9 - direction
	star10 - direction
	planet11 - direction
)
(:init
	(supports instrument0 thermograph1)
	(supports instrument0 spectrograph2)
	(calibration_target instrument0 groundstation4)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 groundstation2)
	(supports instrument1 infrared0)
	(supports instrument1 thermograph1)
	(supports instrument1 image3)
	(calibration_target instrument1 groundstation4)
	(supports instrument2 image4)
	(calibration_target instrument2 star3)
	(on_board instrument1 satellite1)
	(on_board instrument2 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star9)
	(supports instrument3 image4)
	(supports instrument3 spectrograph2)
	(supports instrument3 infrared0)
	(calibration_target instrument3 star3)
	(on_board instrument3 satellite2)
	(power_avail satellite2)
	(pointing satellite2 groundstation4)
	(supports instrument4 infrared0)
	(calibration_target instrument4 star3)
	(on_board instrument4 satellite3)
	(power_avail satellite3)
	(pointing satellite3 groundstation4)
	(supports instrument5 thermograph1)
	(supports instrument5 image4)
	(calibration_target instrument5 groundstation2)
	(supports instrument6 infrared0)
	(calibration_target instrument6 groundstation4)
	(on_board instrument5 satellite4)
	(on_board instrument6 satellite4)
	(power_avail satellite4)
	(pointing satellite4 planet5)
	(supports instrument7 image4)
	(supports instrument7 image3)
	(supports instrument7 spectrograph2)
	(calibration_target instrument7 groundstation4)
	(supports instrument8 spectrograph2)
	(supports instrument8 image3)
	(calibration_target instrument8 star0)
	(on_board instrument7 satellite5)
	(on_board instrument8 satellite5)
	(power_avail satellite5)
	(pointing satellite5 star9)
)
(:goal (and
	(pointing satellite3 star3)
	(pointing satellite4 planet5)
	(have_image planet5 infrared0)
	(have_image planet6 infrared0)
	(have_image planet7 image4)
	(have_image star8 infrared0)
	(have_image star9 image3)
	(have_image star10 image3)
	(have_image planet11 image3)
))

)
