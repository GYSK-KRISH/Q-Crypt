# Q-Crypt: BB84 Quantum Key Distribution Simulator

> **A Class 12 Computer Science & Physics Educational Project**  
> *Simulating Quantum Key Distribution (BB84), Channel Eavesdropping, Quantum Noise, and Classical One-Time Pad Encryption using Python and Qiskit.*

---

## 1. Project Overview

**Q-Crypt** is an educational software simulator developed to demonstrate the principles of **Quantum Key Distribution (QKD)** using the landmark **BB84 protocol** (proposed by Charles Bennett and Gilles Brassard in 1984). 

Built using Python, IBM Qiskit, Matplotlib, and Tkinter, Q-Crypt simulates the complete cryptographic lifecycle:
1. Quantum state preparation in complementary measurement bases ($Z$ and $X$).
2. Quantum transmission over an optical channel with optional eavesdropping (Eve) and environmental noise.
3. Measurement collapse according to Born's rule of quantum mechanics.
4. Classical basis sifting and Quantum Bit Error Rate (QBER) parameter estimation.
5. Classical symmetric encryption and decryption of a text message using the established candidate key via the **One-Time Pad (XOR)** algorithm.

> **Important Educational Note:**  
> Q-Crypt is an **educational computer simulation** executed on classical hardware using mathematical statevector and density matrix operations in Qiskit. It is **not** a physical quantum optical device (which requires physical single-photon emitters, beam splitters, and avalanche photodiodes).

---

## 2. Problem Statement

In modern digital communication, data security relies on **public-key cryptography** (such as RSA and Diffie-Hellman). These algorithms base their security on unproven mathematical hardness assumptions—specifically, the computational difficulty of prime factorization and discrete logarithms.

However, the advent of quantum computing poses an existential threat: **Shor's Algorithm** running on a sufficiently large fault-tolerant quantum computer can solve prime factorization in polynomial time ($O((\log N)^3)$), breaking RSA and classical public-key infrastructure.

Furthermore, classical key exchange protocols are vulnerable to passive interception: an eavesdropper can copy classical bits unnoticed without altering the data stream.

---

## 3. Project Objectives

The primary objectives of this project are:
1. **Model Single Qubit Superposition:** Demonstrate quantum superposition and probabilistic state collapse using Hadamard ($H$) and Pauli-$X$ gates.
2. **Implement the BB84 Protocol:** Faithfully simulate the 4 BB84 quantum states ($|0\rangle, |1\rangle, |+\rangle, |-\rangle$) across the rectilinear ($Z$) and diagonal ($X$) bases.
3. **Simulate Eavesdropping (Eve):** Demonstrate how an *Intercept-Resend Attack* introduces detectable physical disturbance due to the **No-Cloning Theorem** and measurement collapse.
4. **Model Environmental Noise:** Simulate real-world quantum channel imperfections using Qiskit Aer depolarizing noise and detector readout errors.
5. **Compute QBER:** Implement statistical parameter estimation to calculate the Quantum Bit Error Rate and decide whether to accept or discard candidate keys.
6. **Demonstrate Classical Message Encryption:** Integrate the established quantum candidate key with classical **One-Time Pad (OTP/XOR)** encryption to demonstrate real-world text messaging.
7. **Provide an Interactive Educational GUI:** Offer a clean Tkinter desktop interface with visual transmission flows, circuit diagrams, and live stream monitors.

---

## 4. What is the BB84 Protocol?

The **BB84 Protocol** is the world's first quantum cryptographic protocol. Instead of mathematical complexity, BB84 derives its security directly from the fundamental laws of **quantum physics**:

1. **Heisenberg's Uncertainty Principle & Complementary Bases:**  
   Measuring a quantum particle in one basis permanently disturbs any information encoded in a complementary basis.
2. **The No-Cloning Theorem:**  
   An unknown quantum state cannot be perfectly cloned or copied. An eavesdropper cannot duplicate photons to measure later.

### The 4 BB84 Quantum States

| Classical Bit | Encoding Basis | Dirac Ket State | Preparation Gates in Qiskit | Physical Polarization |
| :---: | :---: | :---: | :---: | :---: |
| **0** | **Z** (Rectilinear) | $\|0\rangle$ | Default ground state | Horizontal ($0^\circ$) |
| **1** | **Z** (Rectilinear) | $\|1\rangle$ | $X$ gate | Vertical ($90^\circ$) |
| **0** | **X** (Diagonal) | $\|+\rangle = \frac{\|0\rangle + \|1\rangle}{\sqrt{2}}$ | $H$ gate | Diagonal ($+45^\circ$) |
| **1** | **X** (Diagonal) | $\|-\rangle = \frac{\|0\rangle - \|1\rangle}{\sqrt{2}}$ | $X$ gate followed by $H$ gate | Anti-diagonal ($-45^\circ$) |

### Measurement Mechanics
- **Matching Bases (Alice Basis == Bob Basis):** Measurement is **100% deterministic**. Bob measures Alice's exact bit.
- **Mismatched Bases (Alice Basis != Bob Basis):** The state undergoes quantum collapse. Bob measures $0$ or $1$ with equal $50\%$ probability, losing the original bit value.

---

## 5. How Q-Crypt Works (Complete Pipeline)

```text
       Alice                              Eve                              Bob
         │                                 │                                │
         ├─── [1. Prepare Photons] ────────┼───────────────────────────────►│
         │    (|0>, |1>, |+>, |->)         │ (Intercept-Resend Attack)      │
         │                                 │                                ├─── [2. Measure Photons]
         │                                 │                                │    (Random Z or X bases)
         │                                 │                                │
         │◄════════════════════════════════╪═══════════════════════════════►│
         │                     [3. Public Basis Sifting]                    │
         │                     (Discard basis mismatches)                   │
         │                                                                  │
         │◄════════════════════════════════════════════════════════════════►│
         │                [4. Parameter Estimation & QBER Test]             │
         │                 (Sample test bits & discard them)                │
         │                                                                  │
         │                     [5. Security Decision]                       │
         │            If QBER <= Threshold -> Accept Candidate Key          │
         │            If QBER >  Threshold -> Abort Key Exchange            │
         │                                                                  │
[6. Classical OTP Encryption]                                               │
   Ciphertext = Message XOR Key                                             │
         │                                                                  │
         ├──────────────────── [7. Send Ciphertext (Public Channel)] ──────►│
         │                                                                  │
         │                                                    [8. Classical OTP Decryption]
         │                                                       Message = Ciphertext XOR Key
```

### Key Architectural Separation:
> **BB84 does NOT encrypt the message directly!**  
> BB84 is strictly a **Key Establishment Protocol**. Alice and Bob use the quantum channel solely to generate a shared secret key. Once established, they use classical cryptography (One-Time Pad) to encrypt, transmit, and decrypt their message.

---

## 6. Technology Stack

- **Programming Language:** Python 3.8+
- **Quantum Computing Framework:** [IBM Qiskit](https://www.ibm.com/quantum/qiskit) (Quantum circuits, $X$, $H$, and measurement gates)
- **Quantum Simulator Backend:** [Qiskit Aer](https://github.com/Qiskit/qiskit-aer) (`AerSimulator`, depolarizing noise models, readout error matrices)
- **Numerical Processing:** NumPy
- **Data Visualization & Graphing:** Matplotlib (high-resolution 300 DPI scientific figures)
- **Graphical User Interface:** Python Tkinter (desktop cross-platform GUI)
- **Automated Testing:** Python `unittest` framework (41 automated tests)

---

## 7. Installation Instructions

### Step 1: Clone or Open the Project
Open your command terminal (PowerShell, Command Prompt, or Bash) in the project root directory:
```bash
cd Q-Crypt
```

### Step 2: Install Python Dependencies
Install all required libraries using the included `requirements.txt`:
```bash
pip install -r requirements.txt
```

### Step 3: Run Setup Diagnostic Verifier
Verify that Python, Qiskit, Qiskit Aer, NumPy, and Matplotlib are correctly configured:
```bash
python verify_setup.py
```
*(You should see `[OK]` status checks for all dependencies).*

---

## 8. How to Run the Project

### Option A: Launch the Desktop Graphical Interface (GUI)
```bash
python main_gui.py
```
*Features:*
- Interactive Alice $\to$ Quantum Channel $\to$ Bob visual pipeline banner.
- Real-time bit and basis stream visualizer with color-coded matching indicators.
- Live Qiskit educational quantum circuit diagram visualizer.
- Parameter configuration (qubits, Eve toggle, noise levels, QBER threshold).
- One-Time Pad messaging tab with end-to-end binary and hexadecimal conversions.
- Built-in Matplotlib research graph viewer and regenerator.

---

### Option B: Run Standalone CLI Modules

1. **Experiment 1: Single Qubit Superposition & Hadamard Gate:**
   ```bash
   python src/first_qubit.py
   ```
2. **Experiment 2: The 4 BB84 Quantum States:**
   ```bash
   python src/bb84_states.py
   ```
3. **Classical Pure-Python BB84 Simulator:**
   ```bash
   python src/classical_bb84.py
   ```
4. **Full Quantum BB84 Simulator (with Eve & Noise):**
   ```bash
   python src/bb84_quantum.py
   ```
5. **Interactive Experiment Runner & Multi-Trial Engine:**
   ```bash
   python src/experiment_runner.py
   ```
6. **Multi-Trial Monte Carlo Experiment & CSV Logger:**
   ```bash
   python experiments/multi_run_experiment.py
   ```
7. **End-to-End Secure Message Encryption (One-Time Pad):**
   ```bash
   python src/encryption.py
   ```
8. **Generate Scientific Research Graphs:**
   ```bash
   python experiments/plot_results.py
   ```

---

## 9. Project Directory Structure

```text
Q-Crypt/
├── README.md                     # Comprehensive project documentation
├── requirements.txt              # Project library dependencies
├── verify_setup.py               # Dependency & environment diagnostic verifier
├── main_gui.py                   # Desktop GUI application launcher
│
├── src/                          # Core Quantum & Classical Simulation Engines
│   ├── __init__.py               # Source package initializer
│   ├── first_qubit.py            # Exp 1: Qubit superposition and Hadamard gate
│   ├── bb84_states.py            # Exp 2: 4 BB84 states in matching vs. mismatched bases
│   ├── classical_bb84.py         # Pure-Python classical logic simulator of BB84
│   ├── bb84_quantum.py           # Qiskit quantum circuit simulator with Eve & Noise
│   ├── experiment_runner.py      # Dataclass runner for single & multi-trial runs
│   ├── encryption.py             # Classical One-Time Pad (XOR) message encryption/decryption
│   └── gui.py                    # Tkinter UI with interactive visual flows & circuit models
│
├── experiments/                  # Research Scripts & CSV Logs
│   ├── README.md                 # Experimental methodologies documentation
│   ├── noise_experiment.py       # Comparative noise evaluation (OFF, LOW, MEDIUM, HIGH)
│   ├── multi_run_experiment.py   # Repeated Monte Carlo trials with CSV logger
│   └── plot_results.py           # Matplotlib scientific graph generator (300 DPI)
│
├── screenshots/                  # Publication-Quality Research Graphs
│   ├── 1_qber_vs_noise.png       # Graph 1: QBER vs. Quantum Channel Noise Level
│   ├── 2_qber_eve_off_vs_on.png  # Graph 2: QBER with Eve OFF vs. Eve ON
│   ├── 3_sifted_key_vs_qubits.png# Graph 3: Sifted Key Length vs. Number of Qubits
│   └── 4_basis_matching_percentage.png # Graph 4: Basis Matching Rate Distribution (~50%)
│
├── tests/                        # Automated Verification Test Suite (41 Tests)
│   ├── test_classical_bb84.py    # Unit tests for pure-Python classical logic
│   ├── test_bb84_quantum.py      # Unit tests for quantum circuits & QBER estimation
│   ├── test_noise.py             # Unit tests for Qiskit Aer noise models
│   ├── test_experiment_runner.py # Unit tests for runner & CSV export
│   ├── test_encryption.py        # Unit tests for OTP encryption/decryption
│   └── test_master_audit.py      # Master audit suite covering all 18 project areas
│
└── report/
    └── README.md                 # Student project documentation & viva-voce notes
```

---

## 10. Eavesdropping Experiment (Eve Intercept-Resend Attack)

When Eve is **ON**, she attempts an *Intercept-Resend Attack*:
1. Alice prepares and transmits a photon in basis $\theta_A \in \{Z, X\}$.
2. Eve intercepts the photon, picks a random basis $\theta_E \in \{Z, X\}$, measures it, and prepares a replacement photon in state $\theta_E$ to forward to Bob.
3. Bob measures the replacement photon in basis $\theta_B \in \{Z, X\}$.

### Mathematical Error Probability:
During basis sifting, Alice and Bob only retain instances where $\theta_A = \theta_B$ ($50\%$ of all bits).
- With probability $\frac{1}{2}$, Eve picked the **correct basis** ($\theta_E = \theta_A$):
  - Eve measures the correct bit value.
  - Eve resends the original state.
  - Bob measures the correct bit (Error rate = $0\%$).
- With probability $\frac{1}{2}$, Eve picked the **wrong basis** ($\theta_E \neq \theta_A$):
  - Eve forces the state to collapse into her basis.
  - Bob receives Eve's collapsed state. When Bob measures in $\theta_B = \theta_A$, he gets a random result ($50\%$ error probability).

$$\text{Total Expected Error Rate} = \left(\frac{1}{2} \times 0\right) + \left(\frac{1}{2} \times \frac{1}{2}\right) = \frac{1}{4} = \mathbf{25.0\%}$$

*Conclusion:* Eve's presence introduces an average **$25\%$ error rate** on the sifted key. This physical disturbance immediately alerts Alice and Bob.

---

## 11. Quantum Channel Noise Experiment

In physical optical fibers and free-space channels, imperfections (thermal fluctuations, photon scattering, detector dark counts) induce errors even when Eve is absent.

Q-Crypt models this using **Qiskit Aer Depolarizing Error** and **Readout Error**:

| Noise Level | Channel Error Probability ($p$) | Real-World Physical Analogy | Typical Observed QBER |
| :---: | :---: | :---: | :---: |
| **OFF** | $0.0\%$ ($p=0.00$) | Ideal theoretical quantum channel | $\mathbf{0.0\%}$ |
| **LOW** | $3.0\%$ ($p=0.03$) | Short-range, high-grade laboratory optical fiber | $\approx \mathbf{2.0\% - 4.5\%}$ |
| **MEDIUM** | $8.0\%$ ($p=0.08$) | Standard telecommunications fiber network | $\approx \mathbf{7.0\% - 10.5\%}$ |
| **HIGH** | $20.0\%$ ($p=0.20$) | Long-range satellite / high atmospheric turbulence | $\approx \mathbf{18.0\% - 24.0\%}$ |

Because Alice and Bob cannot distinguish channel noise from an eavesdropper during parameter estimation, any disturbance exceeding the threshold forces them to safely abort.

---

## 12. Quantum Bit Error Rate (QBER)

**QBER (Quantum Bit Error Rate)** measures the fraction of errors in the sifted key:

$$\text{QBER} = \frac{\text{Number of Discrepant Bits}}{\text{Total Tested Sifted Bits}} = \frac{\text{Errors}}{N_{\text{test}}}$$

### Parameter Estimation Process:
1. Alice and Bob extract their **Sifted Key** (matching basis positions).
2. They randomly sample a subset of bits (default: $33\%$ of the sifted key) over the public classical channel to calculate the QBER.
3. **Crucial Security Step:** All revealed test bits are immediately **discarded** to prevent public exposure.
4. The remaining unrevealed bits form the **Candidate Key**.
5. If $\text{QBER} \le \text{Educational Acceptance Threshold}$ (configurable, default: $11.0\%$), the candidate key is **accepted**. Otherwise, the protocol **aborts**.

---

## 13. Classical Message Encryption (One-Time Pad)

Once a shared secret candidate key is established and verified, Alice and Bob use **One-Time Pad (XOR)** encryption:

$$\text{Ciphertext Bit } C_i = M_i \oplus K_i$$
$$\text{Decrypted Bit } M_i = C_i \oplus K_i$$

### Security Guarantees & Safeguards:
- **Information-Theoretic Security:** When the key is truly random, at least as long as the message, used only once, and kept secret, the One-Time Pad is mathematically unbreakable.
- **Key Validation Check:** If the BB84 protocol aborts due to high QBER ($>11\%$) or if the key is shorter than the message, Q-Crypt explicitly **blocks encryption** and displays a critical security warning.

---

## 14. Testing & Quality Assurance

Q-Crypt includes an exhaustive automated test suite covering all 18 functional components:
```bash
python -m unittest discover tests -v
```

### Audit Test Matrix (41 / 41 Tests Passing)
- `tests/test_master_audit.py` (18 comprehensive audit tests)
- `tests/test_classical_bb84.py` (6 classical logic tests)
- `tests/test_bb84_quantum.py` (5 quantum circuit & QBER tests)
- `tests/test_noise.py` (3 Qiskit Aer noise model tests)
- `tests/test_experiment_runner.py` (4 multi-trial & CSV tests)
- `tests/test_encryption.py` (5 OTP encryption, decryption & abort tests)

---

## 15. Project Limitations (Educational Scope)

As a Class 12 high school science project, Q-Crypt models the fundamental physics and logic of QKD. The following limitations should be noted:
1. **Classical Simulation:** All quantum circuits are simulated on classical CPU hardware using matrix representations via Qiskit Aer rather than physical quantum optical hardware.
2. **Idealized Photon Detectors:** Physical Single-Photon Avalanche Diodes (SPADs) experience dead-time losses, multi-photon emissions, and dark count rates. Q-Crypt simulates 100% photon transmission arrival.
3. **Absence of Advanced Post-Processing:** Commercial QKD systems incorporate classical error correction algorithms (**CASCADE** or **Winnow**) and **Privacy Amplification** (universal hash functions) to reduce Eve's partial mutual information. For educational simplicity and clarity, Q-Crypt directly applies parameter estimation and OTP encryption.

---

## 16. Future Improvements & Extensions

Potential future enhancements for undergraduate research:
- **Decoy-State BB84 Protocol:** Implement weak coherent pulse simulations with decoy states to defend against Photon Number Splitting (PNS) attacks.
- **Entanglement-Based QKD (E91 Protocol):** Model quantum entanglement using Bell pairs ($|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}$) and the Clauser-Horne-Shimony-Holt (CHSH) Bell inequality.
- **CASCADE Classical Error Correction:** Add iterative parity exchange post-processing to correct minor channel noise errors without aborting.
- **Physical Laser/Polarization Bench Demonstration:** Pair the software simulation with an optical breadboard utilizing polarizing filters and LEDs.

---

## 17. References & Acknowledgments

1. **Bennett, C. H., & Brassard, G. (1984).** *Quantum cryptography: Public key distribution and coin tossing.* International Conference on Computers, Systems & Signal Processing, Bangalore, India, 175-179.
2. **Nielsen, M. A., & Chuang, I. L. (2010).** *Quantum Computation and Quantum Information.* Cambridge University Press.
3. **Qiskit Development Team (2024).** *Qiskit: An Open-source Framework for Quantum Computing.* IBM Quantum.
4. **NCERT Class 12 Physics & Computer Science Curriculum:** Wave Optics, Photons, Communication Systems, and Boolean Logic.

---
*Created as an educational demonstration of Quantum Key Distribution and Cryptography for Class 12 Board Examination & Practical Project Evaluation.*
