# QOSF - Screening Task 2 (Quantum Error Correction)

This project is completed to satisfy the application requirements of QOSF mentorship program. You will find here my solution to Task 2 of the screening tasks.

## Content
+ ''Task2.pdf'' is a theoretical report about the task:
+ ''quantum_error_correction.py'' is the script that includes the answers of each question:

  + You will find functions in the script. Each function is related to a question in the task.
  + I prefered to use **qiskit** package and **aer** simulator to test QC.

## Task 2
The bit-flip code and the sign-flip code (you can find a description of both here) are two very simple circuits able to detect and fix the bit-flip and the sign-flip errors, respectively.
1. Build the following simple circuit to prepare the Bell state: ![\Large (\ket{0} + \ket{1})/\sqrt{2}](https://latex.codecogs.com/svg.latex?\Large&space;(\ket{0} + \ket{1})/\sqrt{2}) 
2. Now add, right before the CNOT gate and for each of the two qubits, an arbitrary “error gate”. By error gate we mean that with a certain probability (that you can decide but must be non-zero for all the choices) you have a 1 qubit unitary which can be either the identity, or the X gate (bit-flip error) or the Z gate (sign-flip error).
3. Encode each of the two qubits with a sign-flip or a bit-flip code, in such a way that all the possible choices for the error gates described in 2), occurring on the logical qubits, can be detected and fixed. Motivate your choice. This is the most non-trivial part of the problem, so do it with a lot of care!
4. Test your solution by making many measurements over the final state and testing that the results are in line with the expectations.

