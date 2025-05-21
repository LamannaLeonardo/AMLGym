(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	satellite1 - satellite
	instrument2 - instrument
	instrument3 - instrument
	satellite2 - satellite
	instrument4 - instrument
	satellite3 - satellite
	instrument5 - instrument
	spectrograph1 - mode
	infrared0 - mode
	groundstation2 - direction
	groundstation1 - direction
	groundstation0 - direction
	phenomenon3 - direction
	planet4 - direction
	phenomenon5 - direction
	phenomenon6 - direction
	phenomenon7 - direction
)
(:init
	(supports instrument0 infrared0)
	(supports instrument0 spectrograph1)
	(calibration_target instrument0 groundstation1)
	(supports instrument1 spectrograph1)
	(calibration_target instrument1 groundstation1)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 groundstation2)
	(supports instrument2 infrared0)
	(supports instrument2 spectrograph1)
	(calibration_target instrument2 groundstation2)
	(supports instrument3 spectrograph1)
	(supports instrument3 infrared0)
	(calibration_target instrument3 groundstation1)
	(on_board instrument2 satellite1)
	(on_board instrument3 satellite1)
	(power_avail satellite1)
	(pointing satellite1 phenomenon7)
	(supports instrument4 spectrograph1)
	(supports instrument4 infrared0)
	(calibration_target instrument4 groundstation1)
	(on_board instrument4 satellite2)
	(power_avail satellite2)
	(pointing satellite2 planet4)
	(supports instrument5 spectrograph1)
	(supports instrument5 infrared0)
	(calibration_target instrument5 groundstation0)
	(on_board instrument5 satellite3)
	(power_avail satellite3)
	(pointing satellite3 phenomenon7)
)
(:goal (and
	(pointing satellite0 phenomenon6)
	(pointing satellite1 groundstation1)
	(pointing satellite3 phenomenon7)
	(have_image phenomenon3 spectrograph1)
	(have_image planet4 spectrograph1)
	(have_image phenomenon5 infrared0)
	(have_image phenomenon6 infrared0)
	(have_image phenomenon7 infrared0)
))

)
