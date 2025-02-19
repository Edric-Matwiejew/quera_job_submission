# This program prepares a single-excitation Rydberg state in a 2x2 square lattice.
# A piecewise-linear detuning and Rabi amplitude sequence is applied. Atoms 0 and 2
# experience negative detuning, making the Rydberg state lower in energy for those sites.
# Due to Rydberg blockade and staggered local detuning, the system evolves into a
# superposition:
#    |r g g g> + |g g r g>
# where 'r' = Rydberg state, 'g' = ground state. Only one Rydberg excitation is favored.
#
# A brief detuning 'correction' phase counters unwanted phase accumulation after
# the Rabi drive ramps down.

from bloqade import start
import numpy as np
from bloqade.atom_arrangement import Square

body_template = "{task_ir}"

key = None

request_options = dict(params={"key": key})
url = "https://hooks.zapier.com/hooks/catch/14354283/3meteap/"
nshots = 100  # 1000

# Maximum detuning slew rate (MHz/us)
# Note, programs that exceed the maximum detuning slew rate will pass validation
max_detuning_slew_rate = 1256
# Target detuning amplitude (MHz)
detuning_amp = -125  # local detuning amplitude must be between -125 and 0
# Time required to reach target detuning
# (using the max slew rate constraint)
detuning_slope_time = np.abs(detuning_amp) / max_detuning_slew_rate

# Maximum Rabi amplitude (MHz)
rabi_max_amp = 15.8
# Time for Rabi ramp-up (us)
min_rabi_slope_time = 0.05  # minimum pulse segement duration
rabi_slope_down_time = 2 * min_rabi_slope_time
# Effective time for Rabi oscillation to reach a π rotation (us)
# accounting for a factor of 1/2
rabi_effective_time = 2 * np.pi / rabi_max_amp
# Duration of constant Rabi amplitude phase
rabi_const_time = rabi_effective_time - min_rabi_slope_time

detuning_phase_correction_amp = 0.5 * detuning_amp

# Time for a detuning correction phase
detuning_correction_time = (
    rabi_slope_down_time * detuning_amp
) / detuning_phase_correction_amp

# Define a 2x2 square lattice with 6.0 µm spacing
geometry = Square(2, 2, lattice_spacing=6.0)

# Define time durations for piecewise-linear pulses
durations = [
    detuning_slope_time,  # Ramp up detuning
    min_rabi_slope_time,  # Ramp up Rabi drive
    rabi_const_time,  # Keep Rabi drive constant
    2 * min_rabi_slope_time,  # More gradual ramp-down of Rabi drive
    detuning_slope_time,  # Ramp down detuning
    detuning_correction_time,  # Correction phase for phase errors
    detuning_slope_time,  # Final return to zero detuning
]

# Global detuning
program = geometry.rydberg.detuning.uniform.piecewise_linear(
    durations, [0, 0, 0, 0, 0, 0, -detuning_phase_correction_amp, 0]
)

# local detuning
local_detuning_weights = [1, 0, 1, 0]
program = program.detuning.location(
    list(range(4)), local_detuning_weights
).piecewise_linear(
    durations, [0, detuning_amp, detuning_amp, detuning_amp, detuning_amp, 0, 0, 0]
)

# Global rabi pulse
program = program.rydberg.rabi.amplitude.uniform.piecewise_linear(
    durations, [0, 0, rabi_max_amp, rabi_max_amp, 0, 0, 0, 0]
)

# program.show()

results = program.bloqade.python().run(nshots)

# Show result statistics
results.report().show()

# results = program.quera.custom().submit(nshots, url, body_template, request_options = request_options)
# print(results)
