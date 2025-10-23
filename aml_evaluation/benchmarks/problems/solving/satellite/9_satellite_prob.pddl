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
	instrument5 - instrument
	satellite2 - satellite
	instrument6 - instrument
	instrument7 - instrument
	instrument8 - instrument
	satellite3 - satellite
	instrument9 - instrument
	instrument10 - instrument
	satellite4 - satellite
	instrument11 - instrument
	satellite5 - satellite
	instrument12 - instrument
	instrument13 - instrument
	instrument14 - instrument
	satellite6 - satellite
	instrument15 - instrument
	instrument16 - instrument
	instrument17 - instrument
	spectrograph4 - mode
	spectrograph5 - mode
	infrared1 - mode
	spectrograph3 - mode
	infrared2 - mode
	spectrograph0 - mode
	groundstation4 - direction
	groundstation0 - direction
	groundstation3 - direction
	groundstation2 - direction
	star1 - direction
	groundstation5 - direction
	star6 - direction
	planet7 - direction
	planet8 - direction
	star9 - direction
	star10 - direction
	star11 - direction
	planet12 - direction
	phenomenon13 - direction
)
(:init
	(supports instrument0 spectrograph3)
	(supports instrument0 spectrograph0)
	(supports instrument0 spectrograph5)
	(calibration_target instrument0 groundstation2)
	(supports instrument1 infrared2)
	(supports instrument1 spectrograph5)
	(supports instrument1 spectrograph4)
	(calibration_target instrument1 star1)
	(calibration_target instrument1 groundstation3)
	(supports instrument2 spectrograph0)
	(supports instrument2 infrared2)
	(calibration_target instrument2 star1)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(on_board instrument2 satellite0)
	(power_avail satellite0)
	(pointing satellite0 planet12)
	(supports instrument3 spectrograph0)
	(supports instrument3 spectrograph5)
	(supports instrument3 spectrograph3)
	(calibration_target instrument3 groundstation4)
	(supports instrument4 infrared2)
	(supports instrument4 spectrograph4)
	(supports instrument4 spectrograph0)
	(calibration_target instrument4 groundstation2)
	(calibration_target instrument4 star1)
	(supports instrument5 infrared1)
	(supports instrument5 spectrograph3)
	(calibration_target instrument5 groundstation0)
	(calibration_target instrument5 groundstation5)
	(on_board instrument3 satellite1)
	(on_board instrument4 satellite1)
	(on_board instrument5 satellite1)
	(power_avail satellite1)
	(pointing satellite1 planet8)
	(supports instrument6 infrared2)
	(supports instrument6 spectrograph4)
	(calibration_target instrument6 groundstation0)
	(calibration_target instrument6 groundstation5)
	(supports instrument7 spectrograph3)
	(calibration_target instrument7 groundstation3)
	(calibration_target instrument7 groundstation0)
	(supports instrument8 spectrograph3)
	(supports instrument8 spectrograph0)
	(supports instrument8 infrared2)
	(calibration_target instrument8 groundstation2)
	(calibration_target instrument8 groundstation4)
	(on_board instrument6 satellite2)
	(on_board instrument7 satellite2)
	(on_board instrument8 satellite2)
	(power_avail satellite2)
	(pointing satellite2 phenomenon13)
	(supports instrument9 spectrograph0)
	(calibration_target instrument9 star1)
	(supports instrument10 infrared1)
	(supports instrument10 spectrograph4)
	(supports instrument10 spectrograph5)
	(calibration_target instrument10 groundstation5)
	(calibration_target instrument10 groundstation0)
	(on_board instrument9 satellite3)
	(on_board instrument10 satellite3)
	(power_avail satellite3)
	(pointing satellite3 planet7)
	(supports instrument11 spectrograph3)
	(calibration_target instrument11 groundstation5)
	(on_board instrument11 satellite4)
	(power_avail satellite4)
	(pointing satellite4 groundstation2)
	(supports instrument12 spectrograph5)
	(calibration_target instrument12 groundstation3)
	(calibration_target instrument12 groundstation0)
	(supports instrument13 spectrograph5)
	(supports instrument13 spectrograph0)
	(calibration_target instrument13 star1)
	(supports instrument14 spectrograph0)
	(supports instrument14 infrared1)
	(calibration_target instrument14 groundstation3)
	(calibration_target instrument14 star1)
	(on_board instrument12 satellite5)
	(on_board instrument13 satellite5)
	(on_board instrument14 satellite5)
	(power_avail satellite5)
	(pointing satellite5 star11)
	(supports instrument15 spectrograph0)
	(supports instrument15 spectrograph5)
	(supports instrument15 infrared1)
	(calibration_target instrument15 groundstation2)
	(supports instrument16 spectrograph4)
	(calibration_target instrument16 star1)
	(supports instrument17 spectrograph0)
	(supports instrument17 infrared1)
	(calibration_target instrument17 groundstation5)
	(on_board instrument15 satellite6)
	(on_board instrument16 satellite6)
	(on_board instrument17 satellite6)
	(power_avail satellite6)
	(pointing satellite6 groundstation4)
)
(:goal (and
	(pointing satellite4 groundstation0)
	(pointing satellite5 groundstation3)
	(have_image star6 spectrograph0)
	(have_image planet7 infrared2)
	(have_image planet7 spectrograph5)
	(have_image planet8 spectrograph0)
	(have_image planet8 spectrograph3)
	(have_image star9 spectrograph5)
	(have_image star9 infrared1)
	(have_image star10 spectrograph0)
	(have_image star10 spectrograph3)
	(have_image star11 spectrograph0)
	(have_image planet12 spectrograph5)
	(have_image phenomenon13 infrared1)
))

)
