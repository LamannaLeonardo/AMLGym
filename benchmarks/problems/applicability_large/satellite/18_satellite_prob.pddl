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
	instrument5 - instrument
	satellite3 - satellite
	instrument6 - instrument
	instrument7 - instrument
	satellite4 - satellite
	instrument8 - instrument
	satellite5 - satellite
	instrument9 - instrument
	instrument10 - instrument
	satellite6 - satellite
	instrument11 - instrument
	spectrograph3 - mode
	infrared0 - mode
	spectrograph2 - mode
	spectrograph4 - mode
	spectrograph1 - mode
	groundstation4 - direction
	groundstation0 - direction
	star1 - direction
	groundstation5 - direction
	groundstation2 - direction
	star3 - direction
	planet6 - direction
	planet7 - direction
	star8 - direction
	star9 - direction
	planet10 - direction
	star11 - direction
	planet12 - direction
	phenomenon13 - direction
)
(:init
	(supports instrument0 spectrograph4)
	(supports instrument0 spectrograph1)
	(supports instrument0 spectrograph2)
	(calibration_target instrument0 groundstation0)
	(supports instrument1 spectrograph2)
	(supports instrument1 infrared0)
	(supports instrument1 spectrograph1)
	(calibration_target instrument1 groundstation5)
	(calibration_target instrument1 groundstation2)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 planet10)
	(supports instrument2 spectrograph3)
	(supports instrument2 infrared0)
	(calibration_target instrument2 groundstation5)
	(on_board instrument2 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star11)
	(supports instrument3 spectrograph4)
	(supports instrument3 spectrograph2)
	(supports instrument3 infrared0)
	(calibration_target instrument3 star1)
	(calibration_target instrument3 star3)
	(supports instrument4 spectrograph1)
	(supports instrument4 spectrograph3)
	(supports instrument4 spectrograph2)
	(calibration_target instrument4 groundstation0)
	(supports instrument5 spectrograph4)
	(supports instrument5 infrared0)
	(supports instrument5 spectrograph2)
	(calibration_target instrument5 star3)
	(on_board instrument3 satellite2)
	(on_board instrument4 satellite2)
	(on_board instrument5 satellite2)
	(power_avail satellite2)
	(pointing satellite2 planet7)
	(supports instrument6 spectrograph4)
	(supports instrument6 spectrograph2)
	(calibration_target instrument6 groundstation2)
	(calibration_target instrument6 groundstation5)
	(supports instrument7 spectrograph3)
	(supports instrument7 spectrograph1)
	(calibration_target instrument7 star1)
	(calibration_target instrument7 groundstation5)
	(on_board instrument6 satellite3)
	(on_board instrument7 satellite3)
	(power_avail satellite3)
	(pointing satellite3 planet7)
	(supports instrument8 spectrograph4)
	(supports instrument8 spectrograph2)
	(supports instrument8 spectrograph3)
	(calibration_target instrument8 star1)
	(on_board instrument8 satellite4)
	(power_avail satellite4)
	(pointing satellite4 planet12)
	(supports instrument9 infrared0)
	(supports instrument9 spectrograph1)
	(supports instrument9 spectrograph3)
	(calibration_target instrument9 groundstation5)
	(supports instrument10 spectrograph1)
	(calibration_target instrument10 star3)
	(calibration_target instrument10 groundstation2)
	(on_board instrument9 satellite5)
	(on_board instrument10 satellite5)
	(power_avail satellite5)
	(pointing satellite5 star8)
	(supports instrument11 infrared0)
	(calibration_target instrument11 star3)
	(on_board instrument11 satellite6)
	(power_avail satellite6)
	(pointing satellite6 star11)
)
(:goal (and
	(pointing satellite1 star3)
	(pointing satellite5 star8)
	(pointing satellite6 groundstation0)
	(have_image planet6 spectrograph2)
	(have_image planet7 infrared0)
	(have_image star8 spectrograph4)
	(have_image star9 spectrograph2)
	(have_image planet10 infrared0)
	(have_image star11 spectrograph1)
	(have_image planet12 infrared0)
	(have_image phenomenon13 spectrograph4)
))

)
