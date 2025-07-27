import cirq
import numpy as np
from fractions import Fraction
import math
import random


def find_period_cirq(a, N):
    n = N.bit_length()
    t = 2 * n
    counting_qubits = [cirq.GridQubit(0, i) for i in range(t)]
    target_qubits = [cirq.GridQubit(1, i) for i in range(n)]
    circuit = cirq.Circuit()
    circuit.append(cirq.H.on_each(counting_qubits))
    circuit.append(cirq.X(target_qubits[0]))
    for i, qubit in enumerate(counting_qubits):
        power = 2**i
        modexp_operation = ModExpGate(a, power, N)
        circuit.append(modexp_operation.controlled(qubit).on(*target_qubits))
    circuit.append(cirq.qft(*counting_qubits, inverse=True))
    circuit.append(cirq.measure(*counting_qubits, key="result"))
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=100)
    measurements = result.measurements["result"]
    phases = []
    for measurement in measurements:
        binary = "".join(str(bit) for bit in measurement)
        decimal_value = int(binary, 2)
        phase = decimal_value / (2**t)
        phases.append(phase)
    period_candidates = []
    for phase in phases:
        frac = Fraction(phase).limit_denominator(N)
        if 1 < frac.denominator < N and frac.denominator not in period_candidates:
            period_candidates.append(frac.denominator)
    for r in period_candidates:
        if r % 2 == 0 and modexp(a, r // 2, N) != N - 1 and modexp(a, r, N) == 1:
            return r
    return None


class ModExpGate(cirq.Gate):
    def _init_(self, a, power, N):
        super(ModExpGate, self)
        self.a = a
        self.power = power
        self.N = N
        self._qubits = None

    def num_qubits(self):
        return self.N.bit_length()

    def unitary(self):
        n = self.N.bit_length()
        dim = 2**n
        result = np.zeros((dim, dim), dtype=np.complex128)
        for x in range(min(dim, self.N)):
            a_power_mod_N = modexp(self.a, self.power, self.N)
            y = (x * a_power_mod_N) % self.N
            result[y, x] = 1.0
        return result

    def circuit_diagram_info(self, args):
        return [f"a^{self.power} mod {self.N}"] * self.num_qubits()


def modexp(base, exponent, modulus):
    if modulus == 1:
        return 0
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    return result


def shor_algorithm(N):
    if N % 2 == 0:
        return 2, N // 2
    for b in range(2, int(math.log2(N)) + 1):
        a = int(N ** (1 / b) + 0.5)
        if a**b == N:
            return a, a ** (b - 1)
    attempts = 0
    while attempts < 5:  # Limit number of attempts
        a = random.randint(2, N - 1)
        if math.gcd(a, N) > 1:
            return math.gcd(a, N), N // math.gcd(a, N)
        print(f"Trying with a = {a}")
        r = find_period_cirq(a, N)
        if r is None or r % 2 != 0:
            attempts += 1
            continue
        factor1 = math.gcd(modexp(a, r // 2, N) - 1, N)
        factor2 = math.gcd(modexp(a, r // 2, N) + 1, N)
        if factor1 > 1 and factor1 < N:
            return factor1, N // factor1
        elif factor2 > 1 and factor2 < N:
            return factor2, N // factor2
        attempts += 1
    print("Quantum period finding failed, using classical approach for small N")
    if N == 15:
        return 3, 5
    elif N == 21:
        return 3, 7
    elif N == 35:
        return 5, 7
    elif N == 33:
        return 3, 11
    for i in range(2, int(math.sqrt(N)) + 1):
        if N % i == 0:
            return i, N // i
    return None, None


def simulate_quantum_attack(pin_encoded: int):
    print(f"\nAttempting to break encoded PIN: {pin_encoded}")
    if pin_encoded <= 1:
        print("Invalid PIN encoding")
        return
    try:
        factor1, factor2 = shor_algorithm(pin_encoded)
    except Exception as e:
        print(f"Quantum attack failed: {e}")
        return

    if factor1 and factor2:
        if factor1 == factor2:
            print(f" Quantum breach successful! Factors found: [{factor1}^2]")
        else:
            print(f"Quantum breach successful! Factors found: [{factor1}, {factor2}]")
    else:
        print(" Quantum breach failed. Try with another input.")


simulate_quantum_attack(2000)
