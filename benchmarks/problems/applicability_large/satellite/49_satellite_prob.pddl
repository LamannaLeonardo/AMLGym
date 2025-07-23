(define (problem strips_sat_x_1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	satellite1 - satellite
	instrument1 - instrument
	instrument2 - instrument
	instrument3 - instrument
	satellite2 - satellite
	instrument4 - instrument
	satellite3 - satellite
	instrument5 - instrument
	instrument6 - instrument
	satellite4 - satellite
	instrument7 - instrument
	satellite5 - satellite
	instrument8 - instrument
	instrument9 - instrument
	instrument10 - instrument
	satellite6 - satellite
	instrument11 - instrument
	instrument12 - instrument
	instrument13 - instrument
	image2 - mode
	infrared5 - mode
	infrared0 - mode
	infrared1 - mode
	image4 - mode
	spectrograph3 - mode
	groundstation4 - direction
	star3 - direction
	star0 - direction
	star5 - direction
	star2 - direction
	star1 - direction
	phenomenon6 - direction
	star7 - direction
	star8 - direction
	star9 - direction
	planet10 - direction
	planet11 - direction
	star12 - direction
	phenomenon13 - direction
)
(:init
	(supports instrument0 infrared0)
	(supports instrument0 infrared5)
	(supports instrument0 spectrograph3)
	(calibration_target instrument0 star0)
	(calibration_target instrument0 star1)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 star7)
	(supports instrument1 infrared1)
	(supports instrument1 image4)
	(supports instrument1 spectrograph3)
	(calibration_target instrument1 star0)
	(calibration_target instrument1 star3)
	(supports instrument2 infrared5)
	(supports instrument2 image2)
	(calibration_target instrument2 star1)
	(supports instrument3 spectrograph3)
	(supports instrument3 image2)
	(supports instrument3 infrared0)
	(calibration_target instrument3 star0)
	(on_board instrument1 satellite1)
	(on_board instrument2 satellite1)
	(on_board instrument3 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star9)
	(supports instrument4 spectrograph3)
	(calibration_target instrument4 star1)
	(on_board instrument4 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star0)
	(supports instrument5 infrared0)
	(calibration_target instrument5 star0)
	(supports instrument6 image4)
	(calibration_target instrument6 groundstation4)
	(calibration_target instrument6 star5)
	(on_board instrument5 satellite3)
	(on_board instrument6 satellite3)
	(power_avail satellite3)
	(pointing satellite3 star9)
	(supports instrument7 image4)
	(supports instrument7 image2)
	(supports instrument7 spectrograph3)
	(calibration_target instrument7 star3)
	(calibration_target instrument7 star2)
	(on_board instrument7 satellite4)
	(power_avail satellite4)
	(pointing satellite4 star8)
	(supports instrument8 infrared0)
	(supports instrument8 image2)
	(supports instrument8 spectrograph3)
	(calibration_target instrument8 star3)
	(calibration_target instrument8 star2)
	(supports instrument9 infrared5)
	(calibration_target instrument9 star2)
	(calibration_target instrument9 star0)
	(supports instrument10 spectrograph3)
	(calibration_target instrument10 star1)
	(on_board instrument8 satellite5)
	(on_board instrument9 satellite5)
	(on_board instrument10 satellite5)
	(power_avail satellite5)
	(pointing satellite5 star9)
	(supports instrument11 infrared0)
	(supports instrument11 infrared5)
	(calibration_target instrument11 star1)
	(supports instrument12 spectrograph3)
	(supports instrument12 image4)
	(supports instrument12 infrared0)
	(calibration_target instrument12 star2)
	(calibration_target instrument12 star5)
	(supports instrument13 image2)
	(supports instrument13 infrared1)
	(supports instrument13 infrared0)
	(calibration_target instrument13 star1)
	(on_board instrument11 satellite6)
	(on_board instrument12 satellite6)
	(on_board instrument13 satellite6)
	(power_avail satellite6)
	(pointing satellite6 star1)
)
(:goal (and
	(pointing satellite2 planet11)
	(pointing satellite5 phenomenon13)
	(pointing satellite6 phenomenon6)
	(have_image phenomenon6 infrared1)
	(have_image phenomenon6 infrared0)
	(have_image star7 infrared5)
	(have_image star7 image2)
	(have_image star8 infrared1)
	(have_image star9 image4)
	(have_image star9 image2)
	(have_image planet10 infrared0)
	(have_image planet11 infrared0)
	(have_image star12 infrared0)
	(have_image phenomenon13 infrared1)
))

)
