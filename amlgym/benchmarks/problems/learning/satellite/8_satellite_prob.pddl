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
	satellite3 - satellite
	instrument7 - instrument
	satellite4 - satellite
	instrument8 - instrument
	satellite5 - satellite
	instrument9 - instrument
	satellite6 - satellite
	instrument10 - instrument
	instrument11 - instrument
	thermograph3 - mode
	infrared0 - mode
	infrared4 - mode
	spectrograph1 - mode
	thermograph2 - mode
	groundstation0 - direction
	groundstation5 - direction
	star1 - direction
	groundstation3 - direction
	groundstation4 - direction
	groundstation2 - direction
	star6 - direction
	star7 - direction
	star8 - direction
	planet9 - direction
	star10 - direction
	phenomenon11 - direction
	planet12 - direction
	star13 - direction
)
(:init
	(supports instrument0 infrared4)
	(supports instrument0 spectrograph1)
	(calibration_target instrument0 groundstation2)
	(calibration_target instrument0 groundstation0)
	(supports instrument1 infrared0)
	(supports instrument1 spectrograph1)
	(calibration_target instrument1 groundstation2)
	(calibration_target instrument1 groundstation5)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 planet9)
	(supports instrument2 thermograph2)
	(supports instrument2 infrared4)
	(calibration_target instrument2 groundstation5)
	(calibration_target instrument2 star1)
	(supports instrument3 thermograph3)
	(supports instrument3 spectrograph1)
	(calibration_target instrument3 groundstation2)
	(supports instrument4 thermograph3)
	(calibration_target instrument4 groundstation0)
	(calibration_target instrument4 star1)
	(on_board instrument2 satellite1)
	(on_board instrument3 satellite1)
	(on_board instrument4 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star7)
	(supports instrument5 thermograph2)
	(supports instrument5 infrared4)
	(supports instrument5 spectrograph1)
	(calibration_target instrument5 groundstation0)
	(calibration_target instrument5 groundstation3)
	(supports instrument6 infrared4)
	(calibration_target instrument6 groundstation5)
	(on_board instrument5 satellite2)
	(on_board instrument6 satellite2)
	(power_avail satellite2)
	(pointing satellite2 groundstation3)
	(supports instrument7 infrared0)
	(calibration_target instrument7 groundstation2)
	(on_board instrument7 satellite3)
	(power_avail satellite3)
	(pointing satellite3 planet12)
	(supports instrument8 thermograph2)
	(supports instrument8 infrared0)
	(supports instrument8 spectrograph1)
	(calibration_target instrument8 groundstation0)
	(calibration_target instrument8 groundstation3)
	(on_board instrument8 satellite4)
	(power_avail satellite4)
	(pointing satellite4 star13)
	(supports instrument9 spectrograph1)
	(supports instrument9 infrared4)
	(calibration_target instrument9 groundstation5)
	(calibration_target instrument9 groundstation0)
	(on_board instrument9 satellite5)
	(power_avail satellite5)
	(pointing satellite5 star6)
	(supports instrument10 thermograph2)
	(calibration_target instrument10 groundstation3)
	(calibration_target instrument10 star1)
	(supports instrument11 thermograph3)
	(calibration_target instrument11 groundstation2)
	(calibration_target instrument11 groundstation4)
	(on_board instrument10 satellite6)
	(on_board instrument11 satellite6)
	(power_avail satellite6)
	(pointing satellite6 planet12)
)
(:goal (and
	(pointing satellite2 star1)
	(pointing satellite4 groundstation5)
	(pointing satellite6 star8)
	(have_image star6 thermograph2)
	(have_image star7 thermograph3)
	(have_image star8 infrared0)
	(have_image planet9 thermograph2)
	(have_image star10 thermograph3)
	(have_image phenomenon11 spectrograph1)
	(have_image planet12 thermograph2)
	(have_image star13 spectrograph1)
))

)
