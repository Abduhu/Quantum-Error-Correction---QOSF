#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 09:13:39 2021

@author: Abdellah Tounsi

Task 2: Quantum Error Correction
    The bit-flip code and the sign-flip code are two very simple circuits able
    to detect and fix the bit-flip and the sign-flip errors, respectively.
    
### Each question is solved by the functions:
    1) error_free_case
    2) noisy_case
    3) corrected_case
    4)

"""
import numpy as np
import matplotlib.pyplot as plt
from qiskit import(QuantumCircuit, QuantumRegister, 
                   ClassicalRegister,
                   execute, Aer)
from qiskit.providers.aer import QasmSimulator
from random import random

N_SHOTS = 1000   # Number of experiements
P = 0.5                  # Probability of quantum error
PX = 0.5              # Probability that error is NOT gate
PZ = 1 - PX             # Probability that error is Z gate

# Launch simulator
simulator = Aer.get_backend('qasm_simulator')



def error_free_case(n_shots=N_SHOTS,
                    change_basis=False,
                    verbose=False):
    """
    1) Build the following simple circuit to prepare the Bell state: 
         \psi> = CNOT (H otimes I) |00>
    """
    # prepare register of two qubits \00> and two classical bits
    circuit = QuantumCircuit(2, 2)
    
    # Apply (H \otimes I) gate
    # circuit.h(0)
    
    # Apply CNOT gate on control qubit 0 and target qubit 1
    circuit.cx(0, 1)
    
    # Map the quantum measurement to the classical bits
    circuit.barrier([0, 1])
    
    if change_basis:
        # to measure the state in basis of NOT eigenvectors 
        circuit.h(0)
        circuit.h(1)
        
    circuit.measure([0,1], [0,1])
    
    # Execute the circuit on the qasm simulator
    job = execute(circuit, simulator, shots=n_shots)
    
    # Grab results from the job
    result = job.result()
    
    # Returns counts
    counts = result.get_counts(circuit)
    
    if verbose:
        print("\n 1) Error-Free Quantum Circuit Output:",counts)
        
        # Draw the circuit
        circuit.draw(output='mpl', filename='Answer_1.png')
    
    return counts




class NoisyQuantumCircuit(QuantumCircuit):
    """
    This noisy circuit is a standard quantum circuit that is a list of
    instructions bound to some registers. Those instructions include
    random bit-flip and sign-flip instructions.
    
    Additional args:
        
        p: float between 0 and 1
            Probability of quantum error
        px: float  between 0 and 1
            Probability of quantum error to be bit-flip error (NOT)
        pz: float  between 0 and 1
            Probability of quantum error to be sign-flip error (Z)
    """
    
    def __init__(self, *regs, name_=None, global_phase_=0,
                 p=0.2, px=0.5):
        self.p = p
        self.px = px
        self.pz = 1 - px
        QuantumCircuit.__init__(self, *regs, name=name_,
                                global_phase=global_phase_)
        
    def error(self, qubit):
        random_number = random()
        if random_number <= self.p:
            if random() <= self.px:
                self.x(qubit)
            else:
                self.z(qubit)

def noisy_case(n_shots=N_SHOTS,
               p_=P, px_=PX,
               change_basis=False,
               verbose=False):
    """
    2) Now add, right before the CNOT gate and for each of the two qubits,
      an arbitrary “error gate”.
      By error gate we mean that with a certain probability (that you can decide
      but must be non-zero for all the choices) you have a 1 qubit unitary which
      can be either the identity, or the X gate (bit-flip error) or the Z gate
      (sign-flip error).
  
    Inputs:
        n_shots: int
                Number of repetitions of circuit, for sampling.
        p: float between 0 and 1
                probability of error
        px: float between 0 and 1
                probability of error to be bit-flip
    """
    # prepare register of two qubits \00> and two classical bits
    circuit = NoisyQuantumCircuit(2, 2, p=p_, px=px_)
    
    # Apply (H \otimes I) gate
    circuit.h(0)
    
    # Generate random quantum error
    circuit.barrier([0, 1])
    circuit.error(0)
    circuit.error(1)
    
    # Apply CNOT gate on control qubit 0 and target qubit 1
    circuit.cx(0, 1)
    
    # Map the quantum measurement to the classical bits
    circuit.barrier([0, 1])
    
    if change_basis:
        # to measure the state in basis of NOT eigenvectors 
        circuit.h(0)
        circuit.h(1)
        
    circuit.measure([0,1], [0,1])
    
    # Execute the circuit on the qasm simulator
    job = execute(circuit, simulator, shots=n_shots)
    
    # Grab results from the job
    result = job.result()
    
    # Returns counts
    counts = result.get_counts(circuit)
    
    if verbose:
        print("\n 1) Noisy Quantum Circuit Output:",counts)
        
        # Draw the circuit
        circuit.draw(output='mpl', filename='Answer_2.png')
    
    return counts



def corrected_case(n_shots=N_SHOTS,
                   p_=P, px_=PX,
                   change_basis=False,
                   verbose=False):
    """
    3) Encode each of the two qubits with a sign-flip or a bit-flip code,
        in such a way that all the possible choices for the error gates described
        in 2), occurring on the logical qubits, can be detected and fixed.
        Motivate your choice. This is the most non-trivial part of the problem,
        so do it with a lot of care!
    
    Inputs:
        n_shots: int
                Number of repetitions of circuit, for sampling.
        p: float between 0 and 1
                probability of error
        px: float between 0 and 1
                probability of error to be bit-flip
    """
    ## prepare register of two qubits \00> and two classical bits
    
    q = QuantumRegister(9 + 9 + 3)
    c = ClassicalRegister(1 + 1)
    circuit = QuantumCircuit(q, c)
    
    
    ## Encoding
    
    # qubit 0
    circuit.cx(q[0], q[3])
    circuit.cx(q[0], q[6])
    
    for i in range(3):
        circuit.h(q[0 + i * 3])
        circuit.cx(q[3 * i], q[3 * i + 1])
        circuit.cx(q[3 * i], q[3 * i + 2])
        
    # qubit 1
    circuit.cx(q[9], q[12])
    circuit.cx(q[9], q[15])
    
    for i in range(3):
        circuit.h(q[9 + i * 3])
        circuit.cx(q[9 + 3 * i], q[9 + 3 * i + 1])
        circuit.cx(q[9 + 3 * i], q[9 + 3 * i + 2])
    
    
    ## Noisy Quantum Operations
    circuit.barrier(q)
    
    
    
    # Hadamard gate on qubit 0
    for i in range(3):
        circuit.cx(q[i * 3], q[18 + i])
    for i in range(3):
        circuit.cz(q[18 + i], q[3 * i])
    for i in range(3):
        circuit.z(q[i * 3])
    # for i in range(9):
    #     circuit.x(q[i])
    # for i in range(3):
    #     circuit.h(q[18 + i])
    #     circuit.cz(q[18 + i], q[3 * i])

        
    
    
    # Generate error
    err_circuit = NoisyQuantumCircuit(18, name_='Noisy Gate', p=p_, px=px_)
    err_circuit.error(5)#int(random() * 9.))
     
    # transform the noisy gate to instruction
    err_gate = err_circuit.to_instruction()
    
    qr = []
    for i in range(18):
        qr.append(q[i])
        
    circuit.append(err_gate, qr)
    
    ## Correct  Error
    circuit.barrier(q)
    
    # Correct bit flip
    # qubit 0
    for i in range(3):
        circuit.cx(q[3 * i], q[3 * i + 1])
        circuit.cx(q[3 * i], q[3 * i + 2])
        circuit.ccx(q[3 * i + 2], q[3 * i + 1], q[3 * i])
        circuit.h(q[3 * i])
    # qubit 1
    for i in range(3):
        circuit.cx(q[9 + 3 * i], q[9 + 3 * i + 1])
        circuit.cx(q[9 + 3 * i], q[9 + 3 * i + 2])
        circuit.ccx(q[9 + 3 * i + 2], q[9 +3 * i + 1], q[9 + 3 * i])
        circuit.h(q[9 + 3 * i])
    
    # Correct phase flip
    # qubit 0
    circuit.cx(q[0], q[3])
    circuit.cx(q[0], q[6])
    circuit.ccx(q[6], q[3], q[0])
    # qubit 1
    circuit.cx(q[0 + 9], q[3 + 9])
    circuit.cx(q[0 + 9], q[6 + 9])
    circuit.ccx(q[6 + 9], q[3 + 9], q[0 + 9])
    
    # Apply CNOT (0, 1) gate
    circuit.barrier(q)
    circuit.cx(q[0], q[9])
        
    ## Measurment
    circuit.barrier(q)
    
    if change_basis:
        # to measure the state in basis of NOT eigenvectors 
        circuit.h(0)
        circuit.h(9)
        
    circuit.measure([q[0], q[9]], c)
    
    # Simulation
    # sim = QasmSimulator()
    # result = execute(circuit, sim, shots=n_shots).result()
    # counts = result.get_counts(0)

    # Execute the circuit on the qasm simulator
    job = execute(circuit, simulator, shots=n_shots)
    
    # Grab results from the job
    result = job.result()
    
    # Returns counts
    counts = result.get_counts(circuit)
    
    if verbose:
        print("\n 1) Corrected Noisy Quantum Circuit Output:",counts)
        
        # Draw the circuit
        circuit.draw(output='mpl', filename='Answer3.png')
    
    return counts

def compare(n_trials=10, n_shots_=N_SHOTS,
            p=P, px=PX):
    """
    4) Test your solution by making many measurements over the final state
    and testing that the results are in line with the expectations.
    
    Parameters
    ----------
    n_trials : int
        Number of experiements to be done.. The default is 10.
    n_shots_ : int
        Number of repetitions of circuit, for sampling. The default is N_SHOTS.
    p : float, between 0 and 1
        Probability of error The default is P.
    px : float, between 0 and 1
        Probability of error to be bit-flip. The default is PX.

    Returns
    -------
    dict
        Measurment results in basis of Z and X eigenvectors.

    """
    
    ## Verify bit-flip correction
    error_free_results_z = {'00': 0, '01': 0, '10': 0, '11': 0}
    
    for n in range(n_trials):
        result = error_free_case(n_shots=n_shots_)
        for state in result:
            error_free_results_z[state] += result[state]
        
    noisy_case_results_z = {'00': 0, '01': 0, '10': 0, '11': 0}
    
    for n in range(n_trials):
        result = noisy_case(n_shots=n_shots_, p_=p, px_=px)
        for state in result:
            noisy_case_results_z[state] += result[state]
    
    corrected_case_results_z = {'00': 0, '01': 0, '10': 0, '11': 0}
    
    for n in range(n_trials):
        result = corrected_case(n_shots=n_shots_, p_=p, px_=px)
        for state in result:
            corrected_case_results_z[state] += result[state]
    
    
    ## Verify phase-flip correction
    error_free_results_x = {'00': 0, '01': 0, '10': 0, '11': 0}
    
    for n in range(n_trials):
        result = error_free_case(n_shots=n_shots_, change_basis=True)
        for state in result:
            error_free_results_x[state] += result[state]

    
    noisy_case_results_x = {'00': 0, '01': 0, '10': 0, '11': 0}
    
    for n in range(n_trials):
        result = noisy_case(n_shots=n_shots_, p_=p, px_=px, change_basis=True)
        for state in result:
            noisy_case_results_x[state] += result[state]
    
    corrected_case_results_x = {'00': 0, '01': 0, '10': 0, '11': 0}
    
    for n in range(n_trials):
        result = corrected_case(n_shots=n_shots_, p_=p, px_=px,
                                change_basis=True)
        for state in result:
            corrected_case_results_x[state] += result[state]
    

    return {'error_free': (error_free_results_z, error_free_results_x),
            'noisy': (noisy_case_results_z, noisy_case_results_x),
            'corrected': (corrected_case_results_z, corrected_case_results_x)}
    