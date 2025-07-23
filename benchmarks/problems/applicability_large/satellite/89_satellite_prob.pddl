(define (problem strips_sat_x_1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	satellite1 - satellite
	instrument1 - instrument
	satellite2 - satellite
	instrument2 - instrument
	satellite3 - satellite
	instrument3 - instrument
	instrument4 - instrument
	satellite4 - satellite
	instrument5 - instrument
	satellite5 - satellite
	instrument6 - instrument
	instrument7 - instrument
	instrument8 - instrument
	satellite6 - satellite
	instrument9 - instrument
	infrared3 - mode
	infrared0 - mode
	spectrograph4 - mode
	thermograph1 - mode
	infrared5 - mode
	infrared2 - mode
	groundstation0 - direction
	groundstation5 - direction
	star4 - direction
	groundstation1 - direction
	star2 - direction
	star3 - direction
	planet6 - direction
	phenomenon7 - direction
	phenomenon8 - direction
	star9 - direction
	planet10 - direction
	planet11 - direction
	planet12 - direction
	star13 - direction
)
(:init
	(supports instrument0 spectrograph4)
	(calibration_target instrument0 star2)
	(calibration_target instrument0 groundstation5)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 phenomenon7)
	(supports instrument1 infrared2)
	(calibration_target instrument1 groundstation1)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star3)
	(supports instrument2 thermograph1)
	(supports instrument2 infrared2)
	(calibration_target instrument2 star4)
	(calibration_target instrument2 groundstation0)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star3)
	(supports instrument3 infrared0)
	(supports instrument3 infrared5)
	(calibration_target instrument3 groundstation5)
	(supports instrument4 infrared2)
	(supports instrument4 infrared0)
	(supports instrument4 infrared5)
	(calibration_target instrument4 groundstation1)
	(calibration_target instrument4 groundstation5)
	(on_board instrument3 satellite3)
	(on_board instrument4 satellite3)
	(power_avail satellite3)
	(pointing satellite3 planet6)
	(supports instrument5 spectrograph4)
	(supports instrument5 infrared5)
	(supports instrument5 infrared3)
	(calibration_target instrument5 groundstation1)
	(on_board instrument5 satellite4)
	(power_avail satellite4)
	(pointing satellite4 star3)
	(supports instrument6 thermograph1)
	(supports instrument6 infrared2)
	(supports instrument6 infrared5)
	(calibration_target instrument6 star3)
	(supports instrument7 infrared5)
	(supports instrument7 infrared2)
	(supports instrument7 infrared0)
	(calibration_target instrument7 star4)
	(calibration_target instrument7 star2)
	(supports instrument8 thermograph1)
	(calibration_target instrument8 star2)
	(calibration_target instrument8 groundstation1)
	(on_board instrument6 satellite5)
	(on_board instrument7 satellite5)
	(on_board instrument8 satellite5)
	(power_avail satellite5)
	(pointing satellite5 phenomenon8)
	(supports instrument9 infrared3)
	(calibration_target instrument9 star3)
	(on_board instrument9 satellite6)
	(power_avail satellite6)
	(pointing satellite6 planet11)
)
(:goal (and
	(pointing satellite3 phenomenon8)
	(pointing satellite6 planet12)
	(have_image planet6 spectrograph4)
	(have_image phenomenon7 infrared2)
	(have_image phenomenon8 infrared5)
	(have_image phenomenon8 infrared0)
	(have_image star9 infrared2)
	(have_image star9 spectrograph4)
	(have_image planet10 thermograph1)
	(have_image planet10 infrared0)
	(have_image planet11 spectrograph4)
	(have_image planet12 infrared5)
	(have_image star13 infrared3)
))

)
