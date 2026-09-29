# Q-Crypt: BB84 Quantum Key Distribution Simulator
## Comprehensive Project Report (AISSCE Class 12 Board Practical Examination)

---

## 1. Title

**Project Title:**  
**Q-Crypt: Simulation of the BB84 Quantum Key Distribution Protocol with Channel Eavesdropping, Quantum Noise Modeling, and Classical One-Time Pad Encryption**

**Subject:** Computer Science / Physics  
**Academic Session:** 2025 – 2026  
**Submitted By:** `[INSERT STUDENT NAME]`  
**Class / Section:** XII - `[INSERT SECTION]`  
**Roll Number:** `[INSERT ROLL NUMBER]`  
**School Name:** `[INSERT SCHOOL NAME]`  

---

## 2. Certificate

This is to certify that **`[INSERT STUDENT NAME]`**, a student of Class XII, Roll Number **`[INSERT ROLL NUMBER]`**, has successfully completed the project titled **"Q-Crypt: Simulation of the BB84 Quantum Key Distribution Protocol"** under the guidance of **`[INSERT TEACHER NAME]`** (Teacher-in-Charge) during the academic year **2025–2026** in partial fulfillment of the Physics / Computer Science Practical Examination conducted by the **Central Board of Secondary Education (CBSE)**.

<br><br>

____________________________ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ____________________________  
**Internal Examiner Signature** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **External Examiner Signature**  

<br>

____________________________  
**Principal's Signature & Seal**  

---

## 3. Acknowledgement

I would like to express my sincere gratitude to my respected Principal, **`[INSERT PRINCIPAL NAME]`**, and my project supervisor / subject teacher, **`[INSERT TEACHER NAME]`**, for their invaluable guidance, encouragement, and continuous support throughout the development of this project.

I am deeply thankful to our school's **Computer Science and Physics Laboratories** for providing the computational infrastructure, resources, and environment necessary to design and test this simulation.

Finally, I extend my heartfelt thanks to my parents and classmates for their motivation, feedback, and assistance in refining this project report.

— **`[INSERT STUDENT NAME]`**  
Class XII, Roll No: `[INSERT ROLL NUMBER]`

---

## 4. Abstract

Modern digital security relies heavily on public-key cryptosystems (such as RSA and Elliptic Curve Cryptography), whose security depends on the mathematical difficulty of factoring large composite integers or solving discrete logarithms. The advent of quantum computing and **Shor's Algorithm** threatens these systems with polynomial-time cryptanalysis. 

**Q-Crypt** is an educational software project that models **Quantum Key Distribution (QKD)** using the landmark **BB84 protocol** (Bennett & Brassard, 1984). Implemented in Python with IBM's Qiskit quantum computing framework, Q-Crypt simulates single-photon quantum state preparation in non-orthogonal measurement bases ($Z$ and $X$), quantum transmission over an insecure channel, basis sifting, parameter estimation, and **Quantum Bit Error Rate (QBER)** calculation. 

The simulator demonstrates how quantum mechanics—specifically the **Heisenberg Uncertainty Principle** and the **No-Cloning Theorem**—renders an eavesdropper's (*Eve*) intercept-resend attack physically detectable by introducing an average error rate of $\approx 25\%$. Furthermore, Q-Crypt models environmental channel noise (depolarizing and detector readout errors) using Qiskit Aer. Finally, once a secure candidate key is established and verified, classical **One-Time Pad (XOR)** encryption and decryption of ASCII text messages are executed.

---

## 5. Introduction

Cryptography is the science of secure communication. Historically, cryptography evolved from simple classical substitution ciphers (such as the Caesar cipher) to modern computational algorithms (such as AES and RSA).

Quantum Cryptography represents a fundamental paradigm shift: **its security is guaranteed not by mathematical complexity, but by the immutable laws of quantum physics.**

In a standard symmetric cryptographic system (like the One-Time Pad), if both parties—traditionally called **Alice** (sender) and **Bob** (receiver)—share an identical, completely random secret key that is as long as the message and used only once, their communication is **information-theoretically secure** (proven by Claude Shannon in 1949). The historical challenge has always been: *How can Alice and Bob securely establish this secret key over long distances without an adversary intercepting it?*

The **BB84 Quantum Key Distribution protocol** solves this fundamental "Key Distribution Problem" by encoding digital bits into the quantum states of single photons.

---

## 6. Problem Statement

1. **Vulnerability to Quantum Algorithms:**  
   Classical asymmetric encryption (RSA, Diffie-Hellman) relies on computational complexity. A quantum computer executing Shor's Algorithm can factor a number $N$ in $O((\log N)^3)$ steps, rendering classical public-key cryptography obsolete.
2. **Undetectable Classical Eavesdropping:**  
   In classical digital transmission (e.g., copper wires, radio signals, or standard fiber optics), an eavesdropper can passively tap the line and clone the data stream without altering the original signal.
3. **The Key Distribution Dilemma:**  
   While symmetric encryption (One-Time Pad) is unbreakable, transmitting the secret key physically over classical communication channels is insecure and impractical on a global scale.

---

## 7. Objectives

The primary aims of the Q-Crypt project are:
1. To design and implement a pure-Python classical simulation of the BB84 protocol to illustrate key generation and basis sifting logic.
2. To build an authentic quantum simulation using **IBM Qiskit** that prepares single-qubit quantum states in complementary bases ($Z$ and $X$) and simulates measurement collapse.
3. To model an **Eve Intercept-Resend Attack** and mathematically demonstrate why eavesdropping introduces an average $25\%$ error rate on matching basis bits.
4. To simulate **Quantum Channel Noise** (depolarizing errors and detector readout errors) using Qiskit Aer noise models across four configurable levels (`OFF`, `LOW`, `MEDIUM`, `HIGH`).
5. To implement statistical **QBER parameter estimation**, including test-bit sampling, error detection, test-bit disposal, and configurable acceptance threshold evaluation.
6. To implement end-to-end **One-Time Pad (XOR) text message encryption and decryption**, enforcing security safeguards so that transmission aborts if QBER exceeds the safety threshold.
7. To provide an interactive, educational **Desktop Graphical User Interface (GUI)** using Python Tkinter with real-time visual transmission pipelines and Qiskit circuit diagrams.
8. To generate high-resolution scientific research graphs (300 DPI) using Matplotlib to visualize QBER vs. Noise, Eve comparison, key yield, and basis matching rates.

---

## 8. Quantum Computing Background

Quantum computing is based on quantum mechanics rather than classical electrodynamics.

Unlike classical computers that represent information as binary voltage states (high voltage $= 1$, low voltage $= 0$), a quantum computer manipulates quantum information through physical states such as photon polarization, electron spin, or superconducting transmon circuits.

### Fundamental Principles:
1. **Linear Superposition:** A quantum system can exist in a linear combination of its basis states simultaneously.
2. **Quantum Measurement Collapse (Born's Rule):** Observing a quantum state forces it to probabilistically collapse into one of its definite eigenstates.
3. **No-Cloning Theorem (Wootters & Zurek, 1982):** It is mathematically impossible to create an identical copy of an arbitrary unknown quantum state:
   $$U |\psi\rangle |e\rangle \neq |\psi\rangle |\psi\rangle$$
   This physical law guarantees that an eavesdropper cannot duplicate a flying photon to measure later.

---

## 9. Qubits (Quantum Bits)

A **qubit** is the fundamental unit of quantum information. Mathematically, a pure single-qubit state $|\psi\rangle$ is represented as a unit vector in a two-dimensional complex Hilbert space $\mathbb{C}^2$:

$$|\psi\rangle = \alpha |0\rangle + \beta |1\rangle$$

where $\alpha, \beta \in \mathbb{C}$ are probability amplitudes satisfying the normalization condition:

$$|\alpha|^2 + |\beta|^2 = 1$$

In Dirac notation:
- $|0\rangle = \begin{pmatrix} 1 \\ 0 \end{pmatrix}$ represents the classical bit $0$ (Ground State).
- $|1\rangle = \begin{pmatrix} 0 \\ 1 \end{pmatrix}$ represents the classical bit $1$ (Excited State).

---

## 10. Superposition

When a qubit is in a superposition state:
$$|\psi\rangle = \alpha |0\rangle + \beta |1\rangle \quad (\text{with } \alpha \neq 0, \beta \neq 0)$$
the qubit does not hold a definite classical value of $0$ or $1$. Instead, it possesses a simultaneous probability of collapsing to either value upon observation.

For an equal superposition state:
$$|+\rangle = \frac{1}{\sqrt{2}}|0\rangle + \frac{1}{\sqrt{2}}|1\rangle$$
the probability of measuring $0$ is $|\alpha|^2 = \left(\frac{1}{\sqrt{2}}\right)^2 = \frac{1}{2} = 50\%$, and the probability of measuring $1$ is $|\beta|^2 = \left(\frac{1}{\sqrt{2}}\right)^2 = \frac{1}{2} = 50\%$.

---

## 11. Measurement

In quantum mechanics, measurement is not a passive observation; it is an active physical interaction that transforms the state.

According to **Born's Rule**, measuring a qubit $|\psi\rangle = \alpha |0\rangle + \beta |1\rangle$ in the computational basis yields:
- Outcome $0$ with probability $P(0) = |\alpha|^2$
- Outcome $1$ with probability $P(1) = |\beta|^2$

Immediately following the measurement, the quantum superposition is destroyed (wavefunction collapse), and the qubit remains strictly in the measured eigenstate.

---

## 12. The Complementary X and Z Bases

BB84 utilizes two mutually unbiased, complementary bases:

### 1. The Z-Basis (Standard / Rectilinear / Computational Basis)
- Basis states: $\{|0\rangle, |1\rangle\}$
- Physical photon polarization: Horizontal ($0^\circ$) and Vertical ($90^\circ$).
- Matrix representation:
  $$|0\rangle = \begin{pmatrix} 1 \\ 0 \end{pmatrix}, \quad |1\rangle = \begin{pmatrix} 0 \\ 1 \end{pmatrix}$$

### 2. The X-Basis (Hadamard / Diagonal / Superposition Basis)
- Basis states: $\{|+\rangle, |-\rangle\}$
- Physical photon polarization: $+45^\circ$ Diagonal and $-45^\circ$ Anti-Diagonal.
- Mathematical definitions:
  $$|+\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}} = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 \\ 1 \end{pmatrix}$$
  $$|-\rangle = \frac{|0\rangle - |1\rangle}{\sqrt{2}} = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 \\ -1 \end{pmatrix}$$

### Mutual Unbiasedness Property:
If a state prepared in the $Z$-basis ($|0\rangle$ or $|1\rangle$) is measured in the $X$-basis, the probability of obtaining $|+\rangle$ or $|-\rangle$ is exactly $|\langle \pm | 0 \rangle|^2 = \left(\frac{1}{\sqrt{2}}\right)^2 = \frac{1}{2} = 50\%$. 

---

## 13. The Hadamard Quantum Logic Gate

The **Hadamard Gate ($H$)** is a unitary single-qubit quantum logic gate that creates and resolves superposition.

### Unitary Matrix:
$$H = \frac{1}{\sqrt{2}} \begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}$$

### State Transformations:
$$H |0\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}} = |+\rangle$$
$$H |1\rangle = \frac{|0\rangle - |1\rangle}{\sqrt{2}} = |-\rangle$$

Because $H$ is Hermitian and self-inverse ($H = H^\dagger, H^2 = I$):
$$H |+\rangle = |0\rangle$$
$$H |-\rangle = |1\rangle$$

This mathematical property allows Bob to measure in the $X$-basis using standard $Z$-basis detectors simply by applying a Hadamard gate immediately before measurement.

---

## 14. Quantum Key Distribution (QKD)

**Quantum Key Distribution (QKD)** is a secure communication method that implements a cryptographic protocol involving quantum mechanical components. It allows two remote parties (Alice and Bob) to produce a shared random secret key known only to them.

### Fundamental Concept:
QKD does **not** transmit message data across the quantum channel. Instead, it transmits random quantum states to establish a **shared random secret key**. Once Alice and Bob possess this key, they use standard classical encryption algorithms across public channels (the Internet) to communicate securely.

---

## 15. The BB84 Protocol

Proposed by Charles H. Bennett and Gilles Brassard in 1984, the BB84 protocol operates in two major communication phases:

### Phase 1: Quantum Transmission Phase (Quantum Channel)
1. Alice generates a random sequence of classical bits $a_i \in \{0, 1\}$.
2. Alice randomly chooses an encoding basis $\theta_{A,i} \in \{Z, X\}$ for each bit.
3. Alice prepares single photons in the corresponding state:
   - Bit $0$, Basis $Z \implies |0\rangle$
   - Bit $1$, Basis $Z \implies |1\rangle$
   - Bit $0$, Basis $X \implies |+\rangle$
   - Bit $1$, Basis $X \implies |-\rangle$
4. Alice sends the photons to Bob across the quantum channel.
5. Bob independently and randomly chooses a measurement basis $\theta_{B,i} \in \{Z, X\}$ for each arriving photon and records his measurement outcome $b_i \in \{0, 1\}$.

### Phase 2: Classical Sifting & Parameter Estimation Phase (Public Classical Channel)
6. **Basis Reconciliation (Sifting):** Alice and Bob publicly announce their chosen bases ($\theta_A$ and $\theta_B$). They **never** announce their bit values.
7. They discard all bits where their bases differed ($\theta_A \neq \theta_B$). The remaining matching-basis bits form the **Sifted Key**.
8. **Parameter Estimation:** Alice and Bob publicly compare a small random subset of their sifted key (the **Test Sample**) to calculate the Quantum Bit Error Rate (QBER).
9. **Discard Test Bits:** All tested bits are discarded to prevent an eavesdropper from learning them.
10. **Security Evaluation:**
    - If $\text{QBER} \le \text{Threshold}$ (typically $\le 11\%$), the remaining bits form the secure **Candidate Key**.
    - If $\text{QBER} > \text{Threshold}$, they conclude an eavesdropper or severe noise is present and **abort** the protocol.

---

## 16. System Architecture

Q-Crypt is designed with a strict, modular separation between quantum key distribution and classical cryptography.

```text
========================================================================================
                                 Q-CRYPT ARCHITECTURE
========================================================================================

+--------------------------------------------------------------------------------------+
|                                ALICE (Transmitter)                                   |
|  [Random Bit Generator] ---> [Basis Selector (Z/X)] ---> [Qiskit State Preparation]  |
+--------------------------------------------------------------------------------------+
                                           |
                                [Quantum Channel]
                         (Optional: Eve Intercept-Resend)
                         (Optional: Qiskit Aer Noise)
                                           |
                                           v
+--------------------------------------------------------------------------------------+
|                                  BOB (Receiver)                                      |
|  [Basis Selector (Z/X)] ---> [Qiskit Basis Transform] ---> [AerSimulator Measurement]|
+--------------------------------------------------------------------------------------+
                                           |
                              [Public Classical Channel]
                                           |
                                           v
+--------------------------------------------------------------------------------------+
|                        PUBLIC SIFTING & ERROR ESTIMATION                             |
|  1. Public Basis Comparison (Keep matching indices)                                  |
|  2. Sample Test Bits (Calculate QBER = Errors / Test Bits)                           |
|  3. Discard Test Bits ---> Candidate Key Extraction                                  |
+--------------------------------------------------------------------------------------+
                                           |
                   +-----------------------+-----------------------+
                   | (QBER <= 11%)                                 | (QBER > 11%)
                   v                                               v
+--------------------------------------+       +---------------------------------------+
|          SECURITY ACCEPTED           |       |           PROTOCOL ABORTED            |
| Alice & Bob share valid Candidate Key|       | Eavesdropper / Severe Noise Detected! |
+--------------------------------------+       | Encryption Blocked (Zero Data Leaked) |
                   |                           +---------------------------------------+
                   v
+--------------------------------------------------------------------------------------+
|                      CLASSICAL MESSAGE ENCRYPTION (One-Time Pad)                     |
|  Alice:  Plaintext ASCII  ---> Binary Bits (M)                                        |
|          Ciphertext (C)   =    M XOR Candidate_Key                                    |
|          Transmission     ---> Send Hex Ciphertext over Internet                      |
|  Bob:    Plaintext (M)    =    C XOR Candidate_Key                                    |
|          Decrypted ASCII  <--- Recover original text message                          |
+--------------------------------------------------------------------------------------+
```

---

## 17. Algorithm

### 1. Quantum State Preparation:
```text
Algorithm PrepareQubit(bit, basis):
  Input: bit in {0, 1}, basis in {'Z', 'X'}
  Output: QuantumCircuit qc with 1 qubit, 1 classical bit
  1. Initialize qc = QuantumCircuit(1, 1)
  2. If bit == 1:
       Apply Pauli-X gate to qubit 0 (qc.x(0))
  3. If basis == 'X':
       Apply Hadamard gate to qubit 0 (qc.h(0))
  4. Apply barrier to qc
  5. Return qc
```

### 2. Quantum Basis Measurement:
```text
Algorithm MeasureQubit(qc, basis, simulator):
  Input: QuantumCircuit qc, basis in {'Z', 'X'}, AerSimulator simulator
  Output: measured_bit in {0, 1}
  1. If basis == 'X':
       Apply Hadamard gate to qubit 0 (qc.h(0)) [Rotates X basis to Z basis]
  2. Apply measurement gate (qc.measure(0, 0))
  3. Execute job = simulator.run(qc, shots=1)
  4. Return measured classical bit (0 or 1)
```

### 3. Sifting & QBER Calculation:
```text
Algorithm SiftAndEstimateQBER(alice_bits, alice_bases, bob_results, bob_bases, sample_fraction):
  1. matching_indices = [i for i in range(N) if alice_bases[i] == bob_bases[i]]
  2. alice_sifted = [alice_bits[i] for i in matching_indices]
  3. bob_sifted = [bob_results[i] for i in matching_indices]
  4. num_test = max(1, floor(len(alice_sifted) * sample_fraction))
  5. test_indices = RandomSample(0 to len(alice_sifted)-1, num_test)
  6. errors = count(i in test_indices where alice_sifted[i] != bob_sifted[i])
  7. qber = errors / num_test
  8. candidate_key = [alice_sifted[i] for i in range(len(alice_sifted)) if i not in test_indices]
  9. Return qber, candidate_key
```

---

## 18. Pseudocode

```python
# BB84 Full Protocol Pseudocode
function RunBB84(N_qubits, Eve_Enabled, Noise_Level, Threshold):
    Alice_Bits  = GenerateRandomBits(N_qubits)
    Alice_Bases = GenerateRandomBases(N_qubits)
    Bob_Bases   = GenerateRandomBases(N_qubits)
    Bob_Results = []

    For i from 0 to N_qubits - 1:
        qc = PrepareQubit(Alice_Bits[i], Alice_Bases[i])
        
        If Eve_Enabled is TRUE:
            Eve_Basis = ChooseRandomBasis()
            Eve_Bit = MeasureQubit(qc, Eve_Basis)
            qc = PrepareQubit(Eve_Bit, Eve_Basis) # Intercept & Resend
            
        Bob_Bit = MeasureQubit(qc, Bob_Bases[i], Noise_Level)
        Bob_Results.append(Bob_Bit)
        
    # Basis Sifting
    Alice_Sifted = []
    Bob_Sifted = []
    For i from 0 to N_qubits - 1:
        If Alice_Bases[i] == Bob_Bases[i]:
            Alice_Sifted.append(Alice_Bits[i])
            Bob_Sifted.append(Bob_Results[i])
            
    # Parameter Estimation
    Test_Indices = SelectRandomSubset(Alice_Sifted, fraction=0.33)
    Errors = CountMismatches(Alice_Sifted, Bob_Sifted, Test_Indices)
    QBER = Errors / length(Test_Indices)
    
    Candidate_Key = ExtractUntestedBits(Alice_Sifted, Test_Indices)
    
    If QBER <= Threshold:
        Status = "KEY ACCEPTED"
    Else:
        Status = "KEY REJECTED / ABORTED"
        
    Return Status, QBER, Candidate_Key
```

---

## 19. Implementation Details

The implementation is structured into clean, modular Python source files in the `src/` and `experiments/` directories:

1. **`src/first_qubit.py`:** Demonstrates single-qubit state creation, Hadamard gate superposition, and Born's rule statistical verification.
2. **`src/bb84_states.py`:** Tests all four BB84 states ($|0\rangle, |1\rangle, |+\rangle, |-\rangle$) in matching vs. mismatched bases.
3. **`src/classical_bb84.py`:** Pure-Python implementation of the classical BB84 sifting logic without external quantum dependencies.
4. **`src/bb84_quantum.py`:** Complete Qiskit quantum circuit simulator featuring Eve intercept-resend attacks, noise injection, and QBER estimation.
5. **`src/experiment_runner.py`:** Dataclass-based simulation runner (`ExperimentConfig`, `ExperimentResult`, `run_multi_experiment`) supporting multi-trial Monte Carlo experiments and CSV logging.
6. **`src/encryption.py`:** One-Time Pad (XOR) binary and hexadecimal encryption and decryption routines with safety threshold validation.
7. **`src/gui.py` & `main_gui.py`:** Tkinter desktop graphical interface with visual pipeline monitors and interactive quantum circuit diagrams.
8. **`experiments/plot_results.py`:** Matplotlib graphing script generating four 300 DPI research figures.

---

## 20. Eve Intercept-Resend Experiment

An eavesdropper, **Eve**, cannot passively observe quantum photons due to the **No-Cloning Theorem**. She must physically measure each photon and transmit a newly prepared photon to Bob.

### Mathematical Derivation of Error Probability:
During basis sifting, only cases where Alice and Bob used the same basis ($\theta_A = \theta_B$) are analyzed.

1. **Case 1: Eve chooses the SAME basis as Alice ($\theta_E = \theta_A$) [Probability = $50\%$]:**
   - Eve measures the correct state without disturbance.
   - Eve prepares and sends the exact state Alice originally transmitted.
   - Bob measures in $\theta_B = \theta_A$ and obtains the correct bit.
   - **Error Rate = $0\%$**.

2. **Case 2: Eve chooses the WRONG basis ($\theta_E \neq \theta_A$) [Probability = $50\%$]:**
   - Eve forces Alice's photon to collapse into Eve's basis.
   - Eve sends her collapsed state to Bob.
   - Bob measures in his basis ($\theta_B = \theta_A \neq \theta_E$).
   - Bob's measurement collapses randomly with $50\%$ probability of being $0$ and $50\%$ of being $1$.
   - **Error Rate = $50\%$**.

### Total Theoretical QBER with Eve:
$$\text{Expected QBER}_{\text{Eve}} = P(\theta_E = \theta_A) \times 0 + P(\theta_E \neq \theta_A) \times \frac{1}{2} = \left(\frac{1}{2} \times 0\right) + \left(\frac{1}{2} \times \frac{1}{2}\right) = \mathbf{25.0\%}$$

*Experimental Observation:*  
In simulated runs with Eve active, the observed QBER fluctuates around **$\approx 25\%$** (e.g., `[INSERT ACTUAL QBER RESULT]`), which significantly exceeds the standard $11.0\%$ threshold and immediately triggers a protocol abort.

---

## 21. Quantum Channel Noise Experiment

Physical quantum communication media (fiber optic cables and free-space air channels) introduce depolarizing errors due to photon scattering, birefringence, and detector dark counts.

Q-Crypt models this using Qiskit Aer's `NoiseModel`, `depolarizing_error`, and `ReadoutError`:

| Configured Noise Level | Quantum Channel Error Rate ($p$) | Physical Media Analogy | Observed Average QBER |
| :---: | :---: | :---: | :---: |
| **OFF** | $0.0\%$ | Ideal theoretical channel | `[INSERT ACTUAL QBER RESULT]` |
| **LOW** | $3.0\%$ | Ultra-low loss laboratory fiber | `[INSERT ACTUAL QBER RESULT]` |
| **MEDIUM** | $8.0\%$ | Standard metropolitan telecom fiber | `[INSERT ACTUAL QBER RESULT]` |
| **HIGH** | $20.0\%$ | Long-range turbulent satellite link | `[INSERT ACTUAL QBER RESULT]` |

*Crucial Cryptographic Insight:*  
Because Alice and Bob cannot differentiate environmental noise from an eavesdropper, any QBER above the safety threshold forces an abort.

---

## 22. Quantum Bit Error Rate (QBER)

The **Quantum Bit Error Rate (QBER)** is defined as:

$$\text{QBER} = \frac{N_{\text{errors}}}{N_{\text{tested\_bits}}} = \frac{\sum_{i \in \text{TestSet}} (a_i \oplus b_i)}{|\text{TestSet}|}$$

### Security Threshold:
In theoretical quantum cryptography, the maximum tolerable error rate for which secret key distillation is mathematically possible (using classical error correction and privacy amplification) is **$\approx 11.0\%$** (Shor-Preskill security bound).

In Q-Crypt, the educational acceptance threshold is configurable (default: **$11.0\%$**).

---

## 23. Classical Message Encryption (One-Time Pad)

Once the BB84 simulation accepts a candidate key, Alice and Bob utilize the **One-Time Pad (XOR)** cipher:

### Encryption (Alice):
1. Plaintext text message is converted to 8-bit ASCII binary chunks.
2. Each message bit $M_i$ is XORed with candidate key bit $K_i$:
   $$C_i = M_i \oplus K_i$$
3. Ciphertext bits are converted to hexadecimal format for transmission across the public classical network.

### Decryption (Bob):
1. Bob receives ciphertext bits $C_i$.
2. Bob applies his identical candidate key $K_i$ via XOR:
   $$M_i = C_i \oplus K_i = (M_i \oplus K_i) \oplus K_i = M_i \oplus 0 = M_i$$
3. Binary bits are reassembled into 8-bit characters to recover the original plaintext.

### Security Validation:
If the candidate key length is insufficient ($|K| < |M|$) or if the key exchange aborted ($QBER > 11\%$), the encryption function rejects the operation and outputs an explicit error message.

---

## 24. Experimental Results

### Single Run Demonstration (Sample Data Format):
- **Total Qubits Sent ($N$):** `[INSERT TRIAL COUNT]`
- **Eve Status:** `OFF`
- **Noise Level:** `OFF`
- **Matching Bases Sifted:** `[INSERT ACTUAL AVERAGE SIFTED KEY LENGTH]` bits ($\approx 50\%$ sifting efficiency)
- **Test Bits Sampled:** `[INSERT TEST SAMPLE SIZE]` bits
- **Errors Detected:** `0`
- **Measured QBER:** `[INSERT ACTUAL QBER RESULT]` ($0.00\%$)
- **Candidate Key Yield:** `[INSERT CANDIDATE KEY LENGTH]` bits
- **Protocol Status:** `PASSED`
- **Sample Plaintext Message:** `'QUANTUM'`
- **Recovered Decrypted Message:** `'QUANTUM'` (100% Fidelity)

### Multi-Trial Statistical Summary (`[INSERT TRIAL COUNT]` Repetitions):
- **Average Sifted Key Length:** `[INSERT ACTUAL AVERAGE SIFTED KEY LENGTH]` bits
- **Average QBER (Eve OFF, Noise OFF):** `[INSERT ACTUAL QBER RESULT]`
- **Average QBER (Eve ON, Noise OFF):** `[INSERT ACTUAL QBER RESULT]` ($\approx 25\%$)
- **Key Acceptance Rate (Eve OFF):** `[INSERT ACCEPTANCE RATE]`%
- **Key Acceptance Rate (Eve ON):** `[INSERT ABORT RATE]`% (Safely Aborted)

---

## 25. Research Graphs & Visual Analysis

All four research graphs were generated using real simulation data from `experiments/plot_results.py` and saved at 300 DPI in `screenshots/`:

1. **Graph 1: QBER vs. Quantum Noise Level (`1_qber_vs_noise.png`):**  
   Illustrates a monotonic increase in observed error rates as noise increases from `OFF` to `HIGH`, with an explicit marker for the $11\%$ acceptance threshold.
2. **Graph 2: QBER with Eve OFF vs. Eve ON (`2_qber_eve_off_vs_on.png`):**  
   A comparative bar chart demonstrating that Eve's intercept-resend attack elevates QBER to $\approx 25\%$, well above the security threshold.
3. **Graph 3: Sifted Key Length vs. Number of Qubits (`3_sifted_key_vs_qubits.png`):**  
   Shows a linear relationship with a slope of $\approx 0.50$, validating the theoretical $50\%$ basis-matching probability.
4. **Graph 4: Basis Matching Rate Distribution (`4_basis_matching_percentage.png`):**  
   A histogram confirming a normal distribution centered around the theoretical mean of $50\%$.

---

## 26. Limitations of the Simulation

1. **Classical Emulation vs. Physical Quantum Hardware:**  
   Q-Crypt executes on a classical computer using Qiskit Aer matrix simulations. It does not utilize physical single-photon emitters, optical fibers, or single-photon avalanche photodiode (SPAD) detectors.
2. **Idealized Detector Efficiency:**  
   The simulation assumes that every transmitted photon successfully arrives at Bob's detector (no photon loss or detector dead time).
3. **Absence of Post-Processing Error Correction:**  
   Real-world commercial QKD systems employ classical reconciliation algorithms (**CASCADE** or **Winnow**) to correct minor noise errors and **Privacy Amplification** (universal hash functions) to remove partial eavesdropper information. Q-Crypt simplifies this by directly accepting keys below the threshold for educational clarity.

---

## 27. Future Scope

1. **Decoy-State BB84 Protocol:** Implement weak coherent laser pulses with decoy states to defend against Photon-Number-Splitting (PNS) attacks.
2. **Entanglement-Based QKD (E91 Protocol):** Simulate quantum entanglement using Bell pairs ($|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}$) and verify security via Clauser-Horne-Shimony-Holt (CHSH) Bell inequality violations.
3. **CASCADE Error Correction Implementation:** Add an interactive post-processing module that corrects minor bit flips through iterative parity checks.
4. **Physical Polarization Optical Bench:** Pair the simulation software with physical optical hardware utilizing polarizing beam splitters, waveplates, and lasers in the school physics laboratory.

---

## 28. Conclusion

The **Q-Crypt** project successfully models and demonstrates the physics and computer science principles underlying **Quantum Key Distribution (BB84)**. 

Through classical logic and Qiskit quantum circuit simulations, the project confirms that:
1. Quantum superposition and complementary measurement bases enable secure, random key generation between remote parties.
2. The fundamental laws of quantum physics (Heisenberg's Uncertainty Principle and the No-Cloning Theorem) make eavesdropping detectable by introducing a characteristic $\approx 25\%$ error rate.
3. Once established and verified through QBER testing, a quantum candidate key combined with classical One-Time Pad encryption achieves unbreakable communication.

Q-Crypt provides an accessible, rigorous, and visually intuitive platform for high school students to explore the intersection of quantum mechanics and modern cryptography.

---

## 29. References

1. **Bennett, C. H., & Brassard, G. (1984).** *Quantum cryptography: Public key distribution and coin tossing.* Proceedings of IEEE International Conference on Computers, Systems and Signal Processing, Bangalore, India, pp. 175–179.
2. **Wootters, W. K., & Zurek, W. H. (1982).** *A single quantum cannot be cloned.* Nature, 299(5886), 802–803.
3. **Shannon, C. E. (1949).** *Communication theory of secrecy systems.* Bell System Technical Journal, 28(4), 656–715.
4. **Nielsen, M. A., & Chuang, I. L. (2010).** *Quantum Computation and Quantum Information (10th Anniversary Edition).* Cambridge University Press.
5. **NCERT Class XII Physics Textbook:** Unit VI (Optics) & Unit VII (Dual Nature of Radiation and Matter).
6. **NCERT Class XII Computer Science Textbook:** Unit I (Computational Thinking and Programming) & Unit II (Computer Networks).
7. **IBM Qiskit Documentation (2024):** *Qiskit Aer Simulator and Noise Models.* https://qiskit.org/
