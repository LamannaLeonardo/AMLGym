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
	satellite3 - satellite
	instrument5 - instrument
	instrument6 - instrument
	instrument7 - instrument
	satellite4 - satellite
	instrument8 - instrument
	instrument9 - instrument
	instrument10 - instrument
	satellite5 - satellite
	instrument11 - instrument
	instrument12 - instrument
	instrument13 - instrument
	satellite6 - satellite
	instrument14 - instrument
	spectrograph0 - mode
	thermograph4 - mode
	infrared2 - mode
	infrared3 - mode
	thermograph1 - mode
	groundstation0 - direction
	groundstation4 - direction
	groundstation5 - direction
	groundstation1 - direction
	groundstation3 - direction
	groundstation2 - direction
	planet6 - direction
	phenomenon7 - direction
	planet8 - direction
	planet9 - direction
	phenomenon10 - direction
	phenomenon11 - direction
	planet12 - direction
	planet13 - direction
)
(:init
	(supports instrument0 thermograph1)
	(calibration_target instrument0 groundstation2)
	(calibration_target instrument0 groundstation3)
	(supports instrument1 spectrograph0)
	(supports instrument1 infrared2)
	(calibration_target instrument1 groundstation3)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 groundstation1)
	(supports instrument2 infrared2)
	(calibration_target instrument2 groundstation0)
	(calibration_target instrument2 groundstation1)
	(on_board instrument2 satellite1)
	(power_avail satellite1)
	(pointing satellite1 phenomenon11)
	(supports instrument3 thermograph1)
	(supports instrument3 thermograph4)
	(supports instrument3 infrared2)
	(calibration_target instrument3 groundstation2)
	(supports instrument4 spectrograph0)
	(supports instrument4 thermograph1)
	(calibration_target instrument4 groundstation2)
	(calibration_target instrument4 groundstation1)
	(on_board instrument3 satellite2)
	(on_board instrument4 satellite2)
	(power_avail satellite2)
	(pointing satellite2 phenomenon11)
	(supports instrument5 infrared3)
	(supports instrument5 thermograph1)
	(supports instrument5 thermograph4)
	(calibration_target instrument5 groundstation5)
	(calibration_target instrument5 groundstation4)
	(supports instrument6 infrared2)
	(calibration_target instrument6 groundstation5)
	(calibration_target instrument6 groundstation0)
	(supports instrument7 thermograph1)
	(supports instrument7 thermograph4)
	(supports instrument7 infrared3)
	(calibration_target instrument7 groundstation1)
	(on_board instrument5 satellite3)
	(on_board instrument6 satellite3)
	(on_board instrument7 satellite3)
	(power_avail satellite3)
	(pointing satellite3 phenomenon11)
	(supports instrument8 infrared2)
	(supports instrument8 thermograph1)
	(supports instrument8 infrared3)
	(calibration_target instrument8 groundstation4)
	(calibration_target instrument8 groundstation5)
	(supports instrument9 infrared2)
	(supports instrument9 spectrograph0)
	(calibration_target instrument9 groundstation4)
	(supports instrument10 thermograph1)
	(calibration_target instrument10 groundstation5)
	(on_board instrument8 satellite4)
	(on_board instrument9 satellite4)
	(on_board instrument10 satellite4)
	(power_avail satellite4)
	(pointing satellite4 phenomenon7)
	(supports instrument11 spectrograph0)
	(calibration_target instrument11 groundstation3)
	(supports instrument12 spectrograph0)
	(supports instrument12 infrared2)
	(calibration_target instrument12 groundstation1)
	(supports instrument13 thermograph1)
	(calibration_target instrument13 groundstation2)
	(calibration_target instrument13 groundstation3)
	(on_board instrument11 satellite5)
	(on_board instrument12 satellite5)
	(on_board instrument13 satellite5)
	(power_avail satellite5)
	(pointing satellite5 planet6)
	(supports instrument14 infrared2)
	(supports instrument14 thermograph4)
	(supports instrument14 thermograph1)
	(calibration_target instrument14 groundstation2)
	(on_board instrument14 satellite6)
	(power_avail satellite6)
	(pointing satellite6 groundstation0)
)
(:goal (and
	(have_image planet6 infrared2)
	(have_image phenomenon7 infrared2)
	(have_image planet8 infrared3)
	(have_image planet9 infrared2)
	(have_image phenomenon10 infrared3)
	(have_image phenomenon11 spectrograph0)
	(have_image planet12 thermograph1)
	(have_image planet13 infrared2)
))

)
