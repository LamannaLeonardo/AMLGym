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
	satellite4 - satellite
	instrument8 - instrument
	satellite5 - satellite
	instrument9 - instrument
	instrument10 - instrument
	satellite6 - satellite
	instrument11 - instrument
	thermograph4 - mode
	infrared0 - mode
	image5 - mode
	spectrograph2 - mode
	infrared3 - mode
	spectrograph1 - mode
	groundstation4 - direction
	groundstation0 - direction
	star1 - direction
	groundstation5 - direction
	groundstation3 - direction
	groundstation2 - direction
	star6 - direction
	star7 - direction
	planet8 - direction
	phenomenon9 - direction
	star10 - direction
	star11 - direction
	planet12 - direction
	phenomenon13 - direction
)
(:init
	(supports instrument0 infrared3)
	(supports instrument0 thermograph4)
	(supports instrument0 spectrograph1)
	(calibration_target instrument0 groundstation2)
	(calibration_target instrument0 star1)
	(supports instrument1 spectrograph2)
	(supports instrument1 thermograph4)
	(calibration_target instrument1 star1)
	(supports instrument2 thermograph4)
	(supports instrument2 spectrograph2)
	(supports instrument2 spectrograph1)
	(calibration_target instrument2 groundstation2)
	(calibration_target instrument2 groundstation5)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(on_board instrument2 satellite0)
	(power_avail satellite0)
	(pointing satellite0 phenomenon9)
	(supports instrument3 infrared3)
	(supports instrument3 infrared0)
	(calibration_target instrument3 groundstation4)
	(calibration_target instrument3 star1)
	(supports instrument4 thermograph4)
	(calibration_target instrument4 star1)
	(on_board instrument3 satellite1)
	(on_board instrument4 satellite1)
	(power_avail satellite1)
	(pointing satellite1 groundstation2)
	(supports instrument5 thermograph4)
	(supports instrument5 infrared0)
	(supports instrument5 spectrograph2)
	(calibration_target instrument5 groundstation2)
	(on_board instrument5 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star6)
	(supports instrument6 infrared3)
	(supports instrument6 image5)
	(calibration_target instrument6 groundstation0)
	(calibration_target instrument6 groundstation3)
	(supports instrument7 infrared3)
	(supports instrument7 image5)
	(supports instrument7 spectrograph1)
	(calibration_target instrument7 star1)
	(calibration_target instrument7 groundstation0)
	(on_board instrument6 satellite3)
	(on_board instrument7 satellite3)
	(power_avail satellite3)
	(pointing satellite3 planet8)
	(supports instrument8 infrared0)
	(supports instrument8 spectrograph1)
	(supports instrument8 spectrograph2)
	(calibration_target instrument8 groundstation3)
	(on_board instrument8 satellite4)
	(power_avail satellite4)
	(pointing satellite4 star10)
	(supports instrument9 infrared0)
	(calibration_target instrument9 groundstation5)
	(supports instrument10 spectrograph2)
	(calibration_target instrument10 groundstation3)
	(on_board instrument9 satellite5)
	(on_board instrument10 satellite5)
	(power_avail satellite5)
	(pointing satellite5 phenomenon13)
	(supports instrument11 spectrograph2)
	(supports instrument11 spectrograph1)
	(supports instrument11 thermograph4)
	(calibration_target instrument11 groundstation2)
	(on_board instrument11 satellite6)
	(power_avail satellite6)
	(pointing satellite6 planet8)
)
(:goal (and
	(pointing satellite5 planet8)
	(pointing satellite6 star6)
	(have_image star6 thermograph4)
	(have_image star7 infrared0)
	(have_image planet8 infrared3)
	(have_image phenomenon9 spectrograph1)
	(have_image star10 infrared3)
	(have_image star10 image5)
	(have_image star11 thermograph4)
	(have_image star11 image5)
	(have_image planet12 infrared3)
	(have_image phenomenon13 spectrograph2)
	(have_image phenomenon13 image5)
))

)
