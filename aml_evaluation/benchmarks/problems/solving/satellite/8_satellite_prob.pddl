(define (problem strips_sat_x_1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	satellite1 - satellite
	instrument2 - instrument
	instrument3 - instrument
	instrument4 - instrument
	satellite2 - satellite
	instrument5 - instrument
	instrument6 - instrument
	instrument7 - instrument
	satellite3 - satellite
	instrument8 - instrument
	satellite4 - satellite
	instrument9 - instrument
	satellite5 - satellite
	instrument10 - instrument
	instrument11 - instrument
	instrument12 - instrument
	satellite6 - satellite
	instrument13 - instrument
	instrument14 - instrument
	image2 - mode
	infrared1 - mode
	spectrograph3 - mode
	spectrograph0 - mode
	infrared4 - mode
	star5 - direction
	groundstation4 - direction
	star2 - direction
	groundstation0 - direction
	groundstation1 - direction
	groundstation3 - direction
	planet6 - direction
	planet7 - direction
	star8 - direction
	planet9 - direction
	planet10 - direction
	star11 - direction
	planet12 - direction
	star13 - direction
)
(:init
	(supports instrument0 infrared1)
	(supports instrument0 spectrograph0)
	(calibration_target instrument0 groundstation1)
	(calibration_target instrument0 star2)
	(supports instrument1 infrared4)
	(calibration_target instrument1 star5)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 planet10)
	(supports instrument2 spectrograph3)
	(calibration_target instrument2 groundstation3)
	(calibration_target instrument2 star5)
	(supports instrument3 spectrograph3)
	(supports instrument3 infrared4)
	(supports instrument3 spectrograph0)
	(calibration_target instrument3 star5)
	(calibration_target instrument3 star2)
	(supports instrument4 infrared1)
	(supports instrument4 spectrograph0)
	(supports instrument4 spectrograph3)
	(calibration_target instrument4 groundstation3)
	(calibration_target instrument4 groundstation1)
	(on_board instrument2 satellite1)
	(on_board instrument3 satellite1)
	(on_board instrument4 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star8)
	(supports instrument5 image2)
	(calibration_target instrument5 groundstation0)
	(calibration_target instrument5 star5)
	(supports instrument6 infrared4)
	(supports instrument6 infrared1)
	(calibration_target instrument6 groundstation0)
	(calibration_target instrument6 groundstation4)
	(supports instrument7 image2)
	(supports instrument7 spectrograph0)
	(supports instrument7 infrared1)
	(calibration_target instrument7 groundstation0)
	(on_board instrument5 satellite2)
	(on_board instrument6 satellite2)
	(on_board instrument7 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star13)
	(supports instrument8 infrared1)
	(calibration_target instrument8 groundstation1)
	(on_board instrument8 satellite3)
	(power_avail satellite3)
	(pointing satellite3 groundstation3)
	(supports instrument9 spectrograph0)
	(supports instrument9 spectrograph3)
	(supports instrument9 infrared4)
	(calibration_target instrument9 groundstation1)
	(on_board instrument9 satellite4)
	(power_avail satellite4)
	(pointing satellite4 star11)
	(supports instrument10 image2)
	(supports instrument10 spectrograph0)
	(supports instrument10 spectrograph3)
	(calibration_target instrument10 star2)
	(supports instrument11 infrared4)
	(supports instrument11 spectrograph0)
	(calibration_target instrument11 star2)
	(supports instrument12 infrared4)
	(supports instrument12 image2)
	(calibration_target instrument12 groundstation1)
	(calibration_target instrument12 groundstation3)
	(on_board instrument10 satellite5)
	(on_board instrument11 satellite5)
	(on_board instrument12 satellite5)
	(power_avail satellite5)
	(pointing satellite5 star11)
	(supports instrument13 image2)
	(supports instrument13 spectrograph0)
	(calibration_target instrument13 groundstation3)
	(calibration_target instrument13 groundstation0)
	(supports instrument14 spectrograph3)
	(supports instrument14 spectrograph0)
	(calibration_target instrument14 groundstation3)
	(calibration_target instrument14 groundstation1)
	(on_board instrument13 satellite6)
	(on_board instrument14 satellite6)
	(power_avail satellite6)
	(pointing satellite6 star5)
)
(:goal (and
	(pointing satellite2 planet10)
	(have_image planet6 image2)
	(have_image planet7 infrared4)
	(have_image star8 spectrograph0)
	(have_image planet9 infrared1)
	(have_image planet10 infrared1)
	(have_image star11 infrared1)
	(have_image planet12 infrared1)
	(have_image star13 infrared1)
))

)
