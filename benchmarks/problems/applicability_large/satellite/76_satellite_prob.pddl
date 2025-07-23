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
	satellite4 - satellite
	instrument5 - instrument
	instrument6 - instrument
	satellite5 - satellite
	instrument7 - instrument
	infrared0 - mode
	thermograph1 - mode
	spectrograph3 - mode
	image2 - mode
	groundstation3 - direction
	star4 - direction
	star0 - direction
	groundstation2 - direction
	groundstation1 - direction
	phenomenon5 - direction
	phenomenon6 - direction
	star7 - direction
	star8 - direction
	star9 - direction
	phenomenon10 - direction
	star11 - direction
)
(:init
	(supports instrument0 image2)
	(supports instrument0 infrared0)
	(supports instrument0 thermograph1)
	(calibration_target instrument0 star0)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 phenomenon6)
	(supports instrument1 thermograph1)
	(calibration_target instrument1 groundstation2)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star9)
	(supports instrument2 thermograph1)
	(calibration_target instrument2 groundstation2)
	(supports instrument3 thermograph1)
	(supports instrument3 image2)
	(supports instrument3 infrared0)
	(calibration_target instrument3 groundstation1)
	(on_board instrument2 satellite2)
	(on_board instrument3 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star9)
	(supports instrument4 infrared0)
	(supports instrument4 spectrograph3)
	(calibration_target instrument4 groundstation2)
	(on_board instrument4 satellite3)
	(power_avail satellite3)
	(pointing satellite3 phenomenon10)
	(supports instrument5 spectrograph3)
	(supports instrument5 thermograph1)
	(supports instrument5 image2)
	(calibration_target instrument5 groundstation1)
	(supports instrument6 infrared0)
	(calibration_target instrument6 groundstation1)
	(on_board instrument5 satellite4)
	(on_board instrument6 satellite4)
	(power_avail satellite4)
	(pointing satellite4 groundstation1)
	(supports instrument7 image2)
	(supports instrument7 thermograph1)
	(calibration_target instrument7 groundstation1)
	(on_board instrument7 satellite5)
	(power_avail satellite5)
	(pointing satellite5 phenomenon5)
)
(:goal (and
	(pointing satellite0 phenomenon10)
	(pointing satellite3 groundstation1)
	(pointing satellite5 phenomenon5)
	(have_image phenomenon5 image2)
	(have_image phenomenon6 thermograph1)
	(have_image star7 thermograph1)
	(have_image star8 spectrograph3)
	(have_image star9 image2)
	(have_image phenomenon10 infrared0)
	(have_image star11 image2)
))

)
