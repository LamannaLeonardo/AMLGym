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
	satellite4 - satellite
	instrument7 - instrument
	thermograph0 - mode
	spectrograph1 - mode
	spectrograph3 - mode
	spectrograph2 - mode
	groundstation3 - direction
	groundstation2 - direction
	groundstation1 - direction
	groundstation0 - direction
	planet4 - direction
	phenomenon5 - direction
	star6 - direction
	planet7 - direction
	planet8 - direction
	phenomenon9 - direction
)
(:init
	(supports instrument0 spectrograph2)
	(supports instrument0 thermograph0)
	(supports instrument0 spectrograph1)
	(calibration_target instrument0 groundstation3)
	(supports instrument1 spectrograph2)
	(supports instrument1 spectrograph1)
	(calibration_target instrument1 groundstation0)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 phenomenon9)
	(supports instrument2 spectrograph1)
	(calibration_target instrument2 groundstation0)
	(on_board instrument2 satellite1)
	(power_avail satellite1)
	(pointing satellite1 planet8)
	(supports instrument3 thermograph0)
	(supports instrument3 spectrograph3)
	(supports instrument3 spectrograph2)
	(calibration_target instrument3 groundstation3)
	(supports instrument4 thermograph0)
	(supports instrument4 spectrograph3)
	(calibration_target instrument4 groundstation0)
	(on_board instrument3 satellite2)
	(on_board instrument4 satellite2)
	(power_avail satellite2)
	(pointing satellite2 planet4)
	(supports instrument5 spectrograph3)
	(supports instrument5 spectrograph2)
	(calibration_target instrument5 groundstation2)
	(supports instrument6 thermograph0)
	(supports instrument6 spectrograph1)
	(calibration_target instrument6 groundstation1)
	(on_board instrument5 satellite3)
	(on_board instrument6 satellite3)
	(power_avail satellite3)
	(pointing satellite3 groundstation3)
	(supports instrument7 spectrograph2)
	(supports instrument7 spectrograph1)
	(calibration_target instrument7 groundstation0)
	(on_board instrument7 satellite4)
	(power_avail satellite4)
	(pointing satellite4 groundstation3)
)
(:goal (and
	(pointing satellite0 groundstation3)
	(pointing satellite1 groundstation1)
	(have_image planet4 spectrograph1)
	(have_image phenomenon5 thermograph0)
	(have_image star6 spectrograph2)
	(have_image planet7 thermograph0)
	(have_image planet8 spectrograph1)
	(have_image phenomenon9 spectrograph3)
))

)
