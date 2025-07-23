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
	satellite4 - satellite
	instrument6 - instrument
	instrument7 - instrument
	instrument8 - instrument
	satellite5 - satellite
	instrument9 - instrument
	satellite6 - satellite
	instrument10 - instrument
	infrared0 - mode
	thermograph5 - mode
	image2 - mode
	infrared3 - mode
	spectrograph1 - mode
	image4 - mode
	groundstation3 - direction
	star1 - direction
	groundstation4 - direction
	star0 - direction
	groundstation2 - direction
	groundstation5 - direction
	phenomenon6 - direction
	phenomenon7 - direction
	planet8 - direction
	phenomenon9 - direction
	star10 - direction
	phenomenon11 - direction
	phenomenon12 - direction
	phenomenon13 - direction
)
(:init
	(supports instrument0 image2)
	(supports instrument0 spectrograph1)
	(calibration_target instrument0 groundstation3)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 groundstation4)
	(supports instrument1 thermograph5)
	(calibration_target instrument1 star0)
	(calibration_target instrument1 groundstation3)
	(supports instrument2 spectrograph1)
	(supports instrument2 image2)
	(calibration_target instrument2 star0)
	(supports instrument3 image2)
	(calibration_target instrument3 star1)
	(on_board instrument1 satellite1)
	(on_board instrument2 satellite1)
	(on_board instrument3 satellite1)
	(power_avail satellite1)
	(pointing satellite1 groundstation3)
	(supports instrument4 spectrograph1)
	(calibration_target instrument4 groundstation2)
	(on_board instrument4 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star10)
	(supports instrument5 image2)
	(supports instrument5 thermograph5)
	(supports instrument5 infrared3)
	(calibration_target instrument5 star0)
	(calibration_target instrument5 groundstation4)
	(on_board instrument5 satellite3)
	(power_avail satellite3)
	(pointing satellite3 planet8)
	(supports instrument6 image2)
	(supports instrument6 thermograph5)
	(supports instrument6 infrared3)
	(calibration_target instrument6 groundstation5)
	(calibration_target instrument6 star0)
	(supports instrument7 image2)
	(calibration_target instrument7 star0)
	(supports instrument8 thermograph5)
	(supports instrument8 image2)
	(calibration_target instrument8 groundstation2)
	(on_board instrument6 satellite4)
	(on_board instrument7 satellite4)
	(on_board instrument8 satellite4)
	(power_avail satellite4)
	(pointing satellite4 groundstation3)
	(supports instrument9 image2)
	(supports instrument9 infrared0)
	(supports instrument9 image4)
	(calibration_target instrument9 groundstation5)
	(on_board instrument9 satellite5)
	(power_avail satellite5)
	(pointing satellite5 phenomenon9)
	(supports instrument10 image2)
	(supports instrument10 infrared3)
	(supports instrument10 thermograph5)
	(calibration_target instrument10 groundstation5)
	(on_board instrument10 satellite6)
	(power_avail satellite6)
	(pointing satellite6 star0)
)
(:goal (and
	(pointing satellite2 phenomenon13)
	(have_image phenomenon6 infrared0)
	(have_image phenomenon7 infrared0)
	(have_image planet8 image2)
	(have_image phenomenon9 image4)
	(have_image star10 image4)
	(have_image phenomenon11 image2)
	(have_image phenomenon12 image4)
	(have_image phenomenon12 thermograph5)
	(have_image phenomenon13 thermograph5)
	(have_image phenomenon13 infrared3)
))

)
