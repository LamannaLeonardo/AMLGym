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
	satellite3 - satellite
	instrument4 - instrument
	instrument5 - instrument
	satellite4 - satellite
	instrument6 - instrument
	instrument7 - instrument
	satellite5 - satellite
	instrument8 - instrument
	instrument9 - instrument
	image1 - mode
	infrared2 - mode
	spectrograph0 - mode
	image3 - mode
	groundstation0 - direction
	groundstation2 - direction
	star4 - direction
	star3 - direction
	star1 - direction
	planet5 - direction
	planet6 - direction
	planet7 - direction
	planet8 - direction
	planet9 - direction
	star10 - direction
	planet11 - direction
)
(:init
	(supports instrument0 image3)
	(supports instrument0 image1)
	(calibration_target instrument0 star1)
	(supports instrument1 spectrograph0)
	(calibration_target instrument1 star1)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 planet5)
	(supports instrument2 spectrograph0)
	(supports instrument2 image3)
	(supports instrument2 image1)
	(calibration_target instrument2 star4)
	(on_board instrument2 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star4)
	(supports instrument3 image3)
	(supports instrument3 infrared2)
	(supports instrument3 image1)
	(calibration_target instrument3 star3)
	(on_board instrument3 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star10)
	(supports instrument4 infrared2)
	(supports instrument4 image3)
	(supports instrument4 image1)
	(calibration_target instrument4 star3)
	(supports instrument5 image1)
	(supports instrument5 infrared2)
	(supports instrument5 spectrograph0)
	(calibration_target instrument5 groundstation2)
	(on_board instrument4 satellite3)
	(on_board instrument5 satellite3)
	(power_avail satellite3)
	(pointing satellite3 groundstation2)
	(supports instrument6 infrared2)
	(calibration_target instrument6 star1)
	(supports instrument7 image1)
	(supports instrument7 infrared2)
	(calibration_target instrument7 star4)
	(on_board instrument6 satellite4)
	(on_board instrument7 satellite4)
	(power_avail satellite4)
	(pointing satellite4 planet9)
	(supports instrument8 image3)
	(supports instrument8 spectrograph0)
	(calibration_target instrument8 star3)
	(supports instrument9 infrared2)
	(supports instrument9 image1)
	(supports instrument9 spectrograph0)
	(calibration_target instrument9 star1)
	(on_board instrument8 satellite5)
	(on_board instrument9 satellite5)
	(power_avail satellite5)
	(pointing satellite5 star3)
)
(:goal (and
	(pointing satellite0 groundstation0)
	(pointing satellite1 planet7)
	(pointing satellite4 star3)
	(pointing satellite5 planet11)
	(have_image planet5 spectrograph0)
	(have_image planet6 infrared2)
	(have_image planet7 image1)
	(have_image planet8 infrared2)
	(have_image planet9 image1)
	(have_image star10 infrared2)
	(have_image planet11 spectrograph0)
))

)
