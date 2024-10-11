from bloqade import start

pulse_sequence = (start.rydberg
    .detuning
    .location(0)
    .piecewise_linear([0.06, 1, 0.06, 0.06, 1, 0.06, 0.06, 1, 0.06],[0, 125, 125, 0, 0, 0, 0, 125, 125, 0]))


pulse_sequence = (pulse_sequence.rydberg
    .detuning
    .location(1)
    .piecewise_linear([1.12, 0.06, 1, 0.06],[0, 0, 125, 125, 0]))

pulse_sequence = (pulse_sequence
    .rydberg
    .rabi
    .amplitude
    .uniform
    .piecewise_linear([0.06, 1, 0.06, 0.06, 1, 0.06, 0.06, 1, 0.06],[0, pi, pi, 0, pi, pi, 0, pi, pi, 0]))

pulse_sequence = pulse_sequence.parse_sequence()

geometry = Chain(2, lattice_spacing = 5)

program = geometry.apply(pulse_sequence).show()
