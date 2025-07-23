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
	instrument6 - instrument
	satellite4 - satellite
	instrument7 - instrument
	instrument8 - instrument
	satellite5 - satellite
	instrument9 - instrument
	spectrograph3 - mode
	image2 - mode
	spectrograph1 - mode
	image0 - mode
	groundstation2 - direction
	groundstation1 - direction
	groundstation4 - direction
	groundstation3 - direction
	star0 - direction
	phenomenon5 - direction
	planet6 - direction
	star7 - direction
	planet8 - direction
	phenomenon9 - direction
	phenomenon10 - direction
	star11 - direction
)
(:init
	(supports instrument0 image0)
	(supports instrument0 image2)
	(supports instrument0 spectrograph3)
	(calibration_target instrument0 groundstation4)
	(supports instrument1 spectrograph3)
	(calibration_target instrument1 groundstation1)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 star0)
	(supports instrument2 image0)
	(supports instrument2 image2)
	(supports instrument2 spectrograph3)
	(calibration_target instrument2 groundstation4)
	(on_board instrument2 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star11)
	(supports instrument3 image2)
	(calibration_target instrument3 star0)
	(supports instrument4 image0)
	(supports instrument4 image2)
	(supports instrument4 spectrograph1)
	(calibration_target instrument4 groundstation3)
	(on_board instrument3 satellite2)
	(on_board instrument4 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star7)
	(supports instrument5 image2)
	(supports instrument5 spectrograph3)
	(calibration_target instrument5 star0)
	(supports instrument6 spectrograph1)
	(supports instrument6 image2)
	(calibration_target instrument6 groundstation4)
	(on_board instrument5 satellite3)
	(on_board instrument6 satellite3)
	(power_avail satellite3)
	(pointing satellite3 groundstation4)
	(supports instrument7 spectrograph3)
	(supports instrument7 image0)
	(calibration_target instrument7 star0)
	(supports instrument8 image0)
	(supports instrument8 image2)
	(calibration_target instrument8 groundstation3)
	(on_board instrument7 satellite4)
	(on_board instrument8 satellite4)
	(power_avail satellite4)
	(pointing satellite4 phenomenon5)
	(supports instrument9 spectrograph1)
	(calibration_target instrument9 star0)
	(on_board instrument9 satellite5)
	(power_avail satellite5)
	(pointing satellite5 groundstation2)
)
(:goal (and
	(pointing satellite0 phenomenon10)
	(pointing satellite2 star7)
	(pointing satellite3 star11)
	(have_image phenomenon5 image0)
	(have_image planet6 spectrograph1)
	(have_image star7 spectrograph3)
	(have_image planet8 image0)
	(have_image phenomenon9 spectrograph3)
	(have_image phenomenon10 spectrograph3)
	(have_image star11 spectrograph1)
))

)
