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
	instrument5 - instrument
	satellite4 - satellite
	instrument6 - instrument
	instrument7 - instrument
	satellite5 - satellite
	instrument8 - instrument
	instrument9 - instrument
	spectrograph4 - mode
	image0 - mode
	image3 - mode
	image2 - mode
	infrared1 - mode
	groundstation0 - direction
	star4 - direction
	star2 - direction
	groundstation1 - direction
	star3 - direction
	phenomenon5 - direction
	planet6 - direction
	star7 - direction
	star8 - direction
	planet9 - direction
	planet10 - direction
	planet11 - direction
)
(:init
	(supports instrument0 infrared1)
	(calibration_target instrument0 star3)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 planet9)
	(supports instrument1 image0)
	(calibration_target instrument1 star3)
	(supports instrument2 image0)
	(supports instrument2 image2)
	(calibration_target instrument2 groundstation0)
	(on_board instrument1 satellite1)
	(on_board instrument2 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star3)
	(supports instrument3 infrared1)
	(supports instrument3 image0)
	(calibration_target instrument3 groundstation1)
	(on_board instrument3 satellite2)
	(power_avail satellite2)
	(pointing satellite2 planet11)
	(supports instrument4 spectrograph4)
	(calibration_target instrument4 star2)
	(supports instrument5 spectrograph4)
	(supports instrument5 image2)
	(calibration_target instrument5 star4)
	(on_board instrument4 satellite3)
	(on_board instrument5 satellite3)
	(power_avail satellite3)
	(pointing satellite3 star2)
	(supports instrument6 infrared1)
	(calibration_target instrument6 star4)
	(supports instrument7 infrared1)
	(supports instrument7 image2)
	(supports instrument7 spectrograph4)
	(calibration_target instrument7 star2)
	(on_board instrument6 satellite4)
	(on_board instrument7 satellite4)
	(power_avail satellite4)
	(pointing satellite4 planet11)
	(supports instrument8 image2)
	(supports instrument8 infrared1)
	(supports instrument8 image3)
	(calibration_target instrument8 groundstation1)
	(supports instrument9 infrared1)
	(supports instrument9 spectrograph4)
	(calibration_target instrument9 star3)
	(on_board instrument8 satellite5)
	(on_board instrument9 satellite5)
	(power_avail satellite5)
	(pointing satellite5 planet11)
)
(:goal (and
	(pointing satellite1 phenomenon5)
	(pointing satellite3 star2)
	(have_image phenomenon5 image2)
	(have_image planet6 image2)
	(have_image star7 image0)
	(have_image star8 infrared1)
	(have_image planet9 image2)
	(have_image planet10 image0)
	(have_image planet11 image0)
))

)
