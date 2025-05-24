(define (problem strips_sat_x_1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	instrument2 - instrument
	satellite1 - satellite
	instrument3 - instrument
	instrument4 - instrument
	satellite2 - satellite
	instrument5 - instrument
	satellite3 - satellite
	instrument6 - instrument
	instrument7 - instrument
	instrument8 - instrument
	satellite4 - satellite
	instrument9 - instrument
	instrument10 - instrument
	instrument11 - instrument
	satellite5 - satellite
	instrument12 - instrument
	satellite6 - satellite
	instrument13 - instrument
	instrument14 - instrument
	instrument15 - instrument
	spectrograph0 - mode
	spectrograph3 - mode
	infrared4 - mode
	infrared2 - mode
	image1 - mode
	star4 - direction
	star1 - direction
	star0 - direction
	groundstation2 - direction
	star3 - direction
	star5 - direction
	phenomenon6 - direction
	planet7 - direction
	planet8 - direction
	planet9 - direction
	planet10 - direction
	planet11 - direction
	star12 - direction
	planet13 - direction
)
(:init
	(supports instrument0 spectrograph0)
	(calibration_target instrument0 star4)
	(supports instrument1 spectrograph3)
	(calibration_target instrument1 star4)
	(calibration_target instrument1 star1)
	(supports instrument2 infrared2)
	(supports instrument2 infrared4)
	(calibration_target instrument2 groundstation2)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(on_board instrument2 satellite0)
	(power_avail satellite0)
	(pointing satellite0 star12)
	(supports instrument3 infrared4)
	(calibration_target instrument3 star5)
	(supports instrument4 spectrograph3)
	(calibration_target instrument4 star4)
	(on_board instrument3 satellite1)
	(on_board instrument4 satellite1)
	(power_avail satellite1)
	(pointing satellite1 planet7)
	(supports instrument5 spectrograph0)
	(supports instrument5 spectrograph3)
	(supports instrument5 image1)
	(calibration_target instrument5 star0)
	(calibration_target instrument5 groundstation2)
	(on_board instrument5 satellite2)
	(power_avail satellite2)
	(pointing satellite2 planet10)
	(supports instrument6 infrared2)
	(supports instrument6 spectrograph0)
	(supports instrument6 spectrograph3)
	(calibration_target instrument6 star3)
	(calibration_target instrument6 star4)
	(supports instrument7 infrared4)
	(calibration_target instrument7 star0)
	(supports instrument8 spectrograph3)
	(calibration_target instrument8 star1)
	(calibration_target instrument8 star4)
	(on_board instrument6 satellite3)
	(on_board instrument7 satellite3)
	(on_board instrument8 satellite3)
	(power_avail satellite3)
	(pointing satellite3 planet13)
	(supports instrument9 infrared4)
	(supports instrument9 infrared2)
	(supports instrument9 spectrograph0)
	(calibration_target instrument9 star0)
	(calibration_target instrument9 star3)
	(supports instrument10 spectrograph3)
	(supports instrument10 image1)
	(supports instrument10 infrared4)
	(calibration_target instrument10 groundstation2)
	(supports instrument11 infrared4)
	(calibration_target instrument11 groundstation2)
	(calibration_target instrument11 star3)
	(on_board instrument9 satellite4)
	(on_board instrument10 satellite4)
	(on_board instrument11 satellite4)
	(power_avail satellite4)
	(pointing satellite4 star0)
	(supports instrument12 infrared2)
	(supports instrument12 infrared4)
	(supports instrument12 image1)
	(calibration_target instrument12 star3)
	(calibration_target instrument12 groundstation2)
	(on_board instrument12 satellite5)
	(power_avail satellite5)
	(pointing satellite5 planet9)
	(supports instrument13 infrared2)
	(supports instrument13 spectrograph3)
	(calibration_target instrument13 groundstation2)
	(supports instrument14 spectrograph0)
	(supports instrument14 image1)
	(calibration_target instrument14 star5)
	(supports instrument15 spectrograph3)
	(calibration_target instrument15 star5)
	(calibration_target instrument15 star3)
	(on_board instrument13 satellite6)
	(on_board instrument14 satellite6)
	(on_board instrument15 satellite6)
	(power_avail satellite6)
	(pointing satellite6 planet7)
)
(:goal (and
	(pointing satellite0 star5)
	(pointing satellite1 star12)
	(pointing satellite5 planet8)
	(pointing satellite6 planet10)
	(have_image phenomenon6 spectrograph3)
	(have_image planet7 spectrograph3)
	(have_image planet8 image1)
	(have_image planet9 infrared2)
	(have_image planet10 spectrograph3)
	(have_image planet11 image1)
	(have_image star12 infrared4)
	(have_image planet13 infrared2)
))

)
