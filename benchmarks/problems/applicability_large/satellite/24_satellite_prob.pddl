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
	satellite4 - satellite
	instrument5 - instrument
	instrument6 - instrument
	thermograph1 - mode
	spectrograph2 - mode
	spectrograph0 - mode
	groundstation3 - direction
	groundstation1 - direction
	groundstation0 - direction
	star2 - direction
	phenomenon4 - direction
	planet5 - direction
	phenomenon6 - direction
	planet7 - direction
	phenomenon8 - direction
	star9 - direction
)
(:init
	(supports instrument0 thermograph1)
	(calibration_target instrument0 groundstation0)
	(supports instrument1 spectrograph2)
	(calibration_target instrument1 star2)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 groundstation0)
	(supports instrument2 spectrograph0)
	(supports instrument2 spectrograph2)
	(supports instrument2 thermograph1)
	(calibration_target instrument2 groundstation0)
	(on_board instrument2 satellite1)
	(power_avail satellite1)
	(pointing satellite1 phenomenon6)
	(supports instrument3 spectrograph2)
	(supports instrument3 thermograph1)
	(supports instrument3 spectrograph0)
	(calibration_target instrument3 star2)
	(on_board instrument3 satellite2)
	(power_avail satellite2)
	(pointing satellite2 planet7)
	(supports instrument4 spectrograph0)
	(calibration_target instrument4 groundstation1)
	(on_board instrument4 satellite3)
	(power_avail satellite3)
	(pointing satellite3 star9)
	(supports instrument5 thermograph1)
	(supports instrument5 spectrograph0)
	(calibration_target instrument5 groundstation0)
	(supports instrument6 thermograph1)
	(calibration_target instrument6 star2)
	(on_board instrument5 satellite4)
	(on_board instrument6 satellite4)
	(power_avail satellite4)
	(pointing satellite4 phenomenon4)
)
(:goal (and
	(pointing satellite0 phenomenon8)
	(pointing satellite3 phenomenon6)
	(pointing satellite4 phenomenon6)
	(have_image phenomenon4 thermograph1)
	(have_image planet5 spectrograph0)
	(have_image phenomenon6 spectrograph2)
	(have_image planet7 spectrograph2)
	(have_image phenomenon8 spectrograph0)
	(have_image star9 thermograph1)
))

)
