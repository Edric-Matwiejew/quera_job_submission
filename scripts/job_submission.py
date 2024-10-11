from math import pi
from bloqade.atom_arrangement import Chain
from bloqade import get_capabilities

body_template = "{task_ir}"

request_options = dict(params={"key": "################"})
url = "#########################"

geometry = Chain(2, lattice_spacing = 25.0)

# A NOT operation on two qubits.
NOT = (
  geometry
  .rydberg.rabi.amplitude.uniform
  .piecewise_linear(values = [0, pi, pi, 0], durations = [0.05, 1 - 0.05, 0.05])
)

result = NOT.quera.custom().submit(10, url, body_template, request_options = request_options)

# Response code of 200 if the submission was successful.
print(result)
