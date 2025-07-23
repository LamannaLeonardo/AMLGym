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
	spectrograph0 - mode
	infrared1 - mode
	groundstation0 - direction
	groundstation2 - direction
	groundstation1 - direction
	star3 - direction
	phenomenon4 - direction
	star5 - direction
	phenomenon6 - direction
	phenomenon7 - direction
)
(:init
	(supports instrument0 infrared1)
	(supports instrument0 spectrograph0)
	(calibration_target instrument0 groundstation0)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 star5)
	(supports instrument1 spectrograph0)
	(supports instrument1 infrared1)
	(calibration_target instrument1 groundstation1)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 groundstation0)
	(supports instrument2 infrared1)
	(supports instrument2 spectrograph0)
	(calibration_target instrument2 groundstation2)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 phenomenon7)
	(supports instrument3 spectrograph0)
	(calibration_target instrument3 groundstation1)
	(on_board instrument3 satellite3)
	(power_avail satellite3)
	(pointing satellite3 phenomenon6)
)
(:goal (and
	(pointing satellite0 phenomenon4)
	(pointing satellite2 groundstation0)
	(have_image star3 infrared1)
	(have_image phenomenon4 spectrograph0)
	(have_image star5 infrared1)
	(have_image phenomenon6 spectrograph0)
	(have_image phenomenon7 infrared1)
))

)
