"""
====================================================================
Q-Crypt: Desktop GUI Application (Enhanced Visual Edition)
====================================================================
Educational Objective (Class 12 CS / Physics Project Demonstration):
Provides an interactive graphical interface for:
1. Visualizing the complete Alice -> Quantum Channel -> Bob pipeline.
2. Observing Alice's bases, Bob's bases, and the basis sifting mechanism.
3. Viewing interactive Qiskit quantum circuit models for state preparation and measurement.
4. Performing Classical Message Encryption & Decryption (One-Time Pad).
5. Viewing and regenerating scientific Matplotlib research graphs.

*Educational Disclaimer*:
The circuit diagrams and visual channels represent educational mathematical
models of quantum logic gates in Qiskit, not physical quantum hardware devices.
====================================================================
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import Optional

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from qiskit import QuantumCircuit
from src.experiment_runner import (
    ExperimentConfig,
    ExperimentResult,
    run_experiment,
    run_multi_experiment,
    NOISE_PROBABILITIES,
)
from src.encryption import (
    text_to_bits,
    encrypt_message,
    decrypt_message,
)

# Optional image loading for graphs tab
try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


def generate_educational_circuit(bit: int, prep_basis: str, meas_basis: str) -> str:
    """
    Generates a textual Qiskit quantum circuit diagram for educational demonstration.
    Always returns a string.
    """
    qc = QuantumCircuit(1, 1)

    # Alice State Preparation
    if bit == 1:
        qc.x(0)
    if prep_basis == "X":
        qc.h(0)

    qc.barrier()

    # Bob Measurement Basis Transformation
    if meas_basis == "X":
        qc.h(0)
    qc.measure(0, 0)

    try:
        return str(qc.draw(output="text"))
    except Exception:
        return str(qc)


class QCryptGUI:
    """
    Main Tkinter Desktop Application for Q-Crypt BB84 Simulator.
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Q-Crypt: BB84 Quantum Key Distribution Simulator")
        self.root.geometry("1020x760")
        self.root.minsize(920, 680)

        # State storage
        self.current_result: Optional[ExperimentResult] = None
        self.current_ciphertext_payload: Optional[dict] = None

        # Setup styling
        self._setup_styles()

        # Build UI layout
        self._build_header()
        self._build_pipeline_banner()
        self._build_tabs()
        self._build_statusbar()

    def _setup_styles(self):
        """Configures ttk styles and color palette."""
        style = ttk.Style()
        style.theme_use("clam")

        self.PRIMARY_COLOR = "#2c3e50"
        self.ACCENT_COLOR = "#2980b9"
        self.SUCCESS_COLOR = "#27ae60"
        self.DANGER_COLOR = "#c0392b"
        self.BG_COLOR = "#f8f9fa"

        style.configure("TFrame", background=self.BG_COLOR)
        style.configure("TLabel", background=self.BG_COLOR, font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 15, "bold"), foreground="#1a252f")
        style.configure("Section.TLabel", font=("Segoe UI", 11, "bold"), foreground=self.PRIMARY_COLOR)

        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"), background=self.ACCENT_COLOR, foreground="white")
        style.map("Accent.TButton", background=[("active", "#1f618d")])

        style.configure("Success.TButton", font=("Segoe UI", 10, "bold"), background=self.SUCCESS_COLOR, foreground="white")
        style.map("Success.TButton", background=[("active", "#1e8449")])

        style.configure("Danger.TButton", font=("Segoe UI", 10, "bold"), background=self.DANGER_COLOR, foreground="white")
        style.map("Danger.TButton", background=[("active", "#962d22")])

    def _build_header(self):
        """Renders the top branding header banner."""
        header_frame = tk.Frame(self.root, bg="#1a252f", padx=20, pady=10)
        header_frame.pack(fill="x")

        title_lbl = tk.Label(
            header_frame,
            text="Q-Crypt: BB84 Quantum Key Distribution Simulator",
            font=("Segoe UI", 16, "bold"),
            fg="#ecf0f1",
            bg="#1a252f",
        )
        title_lbl.pack(anchor="w")

        subtitle_lbl = tk.Label(
            header_frame,
            text="Class 12 Educational Project | Quantum Mechanics & Classical Cryptography Interface",
            font=("Segoe UI", 9),
            fg="#bdc3c7",
            bg="#1a252f",
        )
        subtitle_lbl.pack(anchor="w")

    def _build_pipeline_banner(self):
        """
        Renders a clean visual flow diagram: Alice -> Quantum Channel -> Bob
        """
        pipeline_frame = tk.Frame(self.root, bg="#2c3e50", padx=15, pady=8)
        pipeline_frame.pack(fill="x", padx=12, pady=(8, 0))

        # 1. Alice Block
        alice_box = tk.Label(
            pipeline_frame,
            text="👩 ALICE (Sender)\n• Generates Random Bits\n• Prepares |0>,|1>,|+>,|->",
            font=("Segoe UI", 9, "bold"),
            bg="#34495e",
            fg="#ecf0f1",
            padx=12,
            pady=4,
            relief="groove",
        )
        alice_box.pack(side="left", padx=4)

        # Arrow 1
        arr1 = tk.Label(pipeline_frame, text="═══►", font=("Consolas", 12, "bold"), fg="#1abc9c", bg="#2c3e50")
        arr1.pack(side="left", padx=4)

        # 2. Quantum Channel Block
        self.channel_box = tk.Label(
            pipeline_frame,
            text="🌐 QUANTUM CHANNEL\nPhotons / Optical Fiber\n[Eve: OFF | Noise: OFF]",
            font=("Segoe UI", 9, "bold"),
            bg="#16a085",
            fg="white",
            padx=16,
            pady=4,
            relief="groove",
        )
        self.channel_box.pack(side="left", padx=4, fill="x", expand=True)

        # Arrow 2
        arr2 = tk.Label(pipeline_frame, text="═══►", font=("Consolas", 12, "bold"), fg="#1abc9c", bg="#2c3e50")
        arr2.pack(side="left", padx=4)

        # 3. Bob Block
        bob_box = tk.Label(
            pipeline_frame,
            text="👨 BOB (Receiver)\n• Random Z / X Measurement\n• Quantum State Collapse",
            font=("Segoe UI", 9, "bold"),
            bg="#34495e",
            fg="#ecf0f1",
            padx=12,
            pady=4,
            relief="groove",
        )
        bob_box.pack(side="left", padx=4)

    def _update_pipeline_status(self, eve_on: bool, noise_lvl: str):
        """Updates the interactive channel status banner."""
        eve_text = "Eve: ACTIVE (Intercept-Resend)" if eve_on else "Eve: OFF"
        noise_text = f"Noise: {noise_lvl}"

        if eve_on or (noise_lvl != "OFF"):
            bg_color = "#c0392b"  # Warning Red
        else:
            bg_color = "#16a085"  # Safe Teal

        self.channel_box.config(
            text=f"🌐 QUANTUM CHANNEL\nPhotons / Optical Fiber\n[{eve_text} | {noise_text}]",
            bg=bg_color,
        )

    def _build_tabs(self):
        """Creates the tabbed navigation notebook."""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=8)

        # Tab 1: Quantum Simulation & Visualizer
        self.sim_tab = ttk.Frame(self.notebook, padding=8)
        self.notebook.add(self.sim_tab, text="  ⚛️ 1. BB84 Simulation & Visualizer  ")
        self._setup_simulation_tab(self.sim_tab)

        # Tab 2: Classical Encryption & Decryption
        self.msg_tab = ttk.Frame(self.notebook, padding=8)
        self.notebook.add(self.msg_tab, text="  🔒 2. Secure Messaging (OTP)  ")
        self._setup_messaging_tab(self.msg_tab)

        # Tab 3: Scientific Research Graphs
        self.graphs_tab = ttk.Frame(self.notebook, padding=8)
        self.notebook.add(self.graphs_tab, text="  📈 3. Scientific Graphs  ")
        self._setup_graphs_tab(self.graphs_tab)

    # -------------------------------------------------------------
    # TAB 1: QUANTUM SIMULATION & VISUALIZER
    # -------------------------------------------------------------
    def _setup_simulation_tab(self, parent):
        """Builds controls, metrics, and visualizers for Tab 1."""
        top_split = ttk.Frame(parent)
        top_split.pack(fill="x", pady=(0, 6))

        # --- LEFT: Controls ---
        control_frame = ttk.LabelFrame(top_split, text=" Simulation Controls ", padding=10)
        control_frame.pack(side="left", fill="both", expand=True, padx=(0, 6))

        # Row 1: Qubits & Threshold
        ttk.Label(control_frame, text="Qubits:").grid(row=0, column=0, sticky="w", pady=2)
        self.qubit_var = tk.StringVar(value="50")
        self.qubit_entry = ttk.Entry(control_frame, textvariable=self.qubit_var, width=8)
        self.qubit_entry.grid(row=0, column=1, sticky="w", pady=2)

        ttk.Label(control_frame, text="Threshold:").grid(row=0, column=2, sticky="w", padx=(10, 2), pady=2)
        self.thresh_var = tk.StringVar(value="0.11")
        self.thresh_entry = ttk.Entry(control_frame, textvariable=self.thresh_var, width=8)
        self.thresh_entry.grid(row=0, column=3, sticky="w", pady=2)

        # Row 2: Eve & Noise
        self.eve_var = tk.BooleanVar(value=False)
        self.eve_check = ttk.Checkbutton(
            control_frame,
            text="Eve Intercept-Resend",
            variable=self.eve_var,
            command=self._on_control_change,
        )
        self.eve_check.grid(row=1, column=0, columnspan=2, sticky="w", pady=2)

        self.noise_var = tk.BooleanVar(value=False)
        self.noise_check = ttk.Checkbutton(
            control_frame,
            text="Channel Noise",
            variable=self.noise_var,
            command=self._on_control_change,
        )
        self.noise_check.grid(row=1, column=2, sticky="w", pady=2)

        self.noise_level_var = tk.StringVar(value="LOW")
        self.noise_combo = ttk.Combobox(
            control_frame,
            textvariable=self.noise_level_var,
            values=["OFF", "LOW", "MEDIUM", "HIGH"],
            state="readonly",
            width=8,
        )
        self.noise_combo.grid(row=1, column=3, sticky="w", pady=2)
        self.noise_combo.bind("<<ComboboxSelected>>", lambda e: self._on_control_change())

        # Action Buttons
        btn_box = ttk.Frame(control_frame)
        btn_box.grid(row=2, column=0, columnspan=4, pady=(8, 0), sticky="ew")

        self.run_btn = ttk.Button(
            btn_box,
            text="▶ RUN BB84 SIMULATION",
            style="Accent.TButton",
            command=self._handle_run_bb84,
        )
        self.run_btn.pack(side="left", fill="x", expand=True, padx=(0, 4))

        self.multi_btn = ttk.Button(
            btn_box,
            text="📊 Multi-Trial (10x CSV)",
            command=self._handle_run_multi_trial,
        )
        self.multi_btn.pack(side="left", padx=4)

        # --- RIGHT: Metrics & Status ---
        results_frame = ttk.LabelFrame(top_split, text=" Summary Metrics ", padding=10)
        results_frame.pack(side="left", fill="both", expand=True)

        metrics_grid = tk.Frame(results_frame, bg="#ecf0f1", padx=8, pady=4)
        metrics_grid.pack(fill="both", expand=True)

        self.lbl_qubits_sent = tk.Label(metrics_grid, text="Qubits: --", bg="#ecf0f1", font=("Segoe UI", 9, "bold"))
        self.lbl_qubits_sent.grid(row=0, column=0, sticky="w", padx=6, pady=2)

        self.lbl_matching_bases = tk.Label(metrics_grid, text="Matches: --", bg="#ecf0f1", font=("Segoe UI", 9, "bold"))
        self.lbl_matching_bases.grid(row=0, column=1, sticky="w", padx=6, pady=2)

        self.lbl_sifted_len = tk.Label(metrics_grid, text="Sifted Key: --", bg="#ecf0f1", font=("Segoe UI", 9, "bold"))
        self.lbl_sifted_len.grid(row=1, column=0, sticky="w", padx=6, pady=2)

        self.lbl_qber = tk.Label(metrics_grid, text="QBER: --", bg="#ecf0f1", font=("Segoe UI", 9, "bold"), fg="#2c3e50")
        self.lbl_qber.grid(row=1, column=1, sticky="w", padx=6, pady=2)

        self.lbl_status = tk.Label(
            metrics_grid,
            text="STATUS: NOT RUN",
            bg="#95a5a6",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=8,
            pady=2,
        )
        self.lbl_status.grid(row=0, column=2, rowspan=2, padx=10, pady=2)

        # --- BOTTOM SUB-NOTEBOOK: Visualizers ---
        sub_notebook = ttk.Notebook(parent)
        sub_notebook.pack(fill="both", expand=True, pady=(4, 0))

        # Sub-Tab A: Basis Sifting Alignment Visualizer
        sifting_sub = ttk.Frame(sub_notebook, padding=6)
        sub_notebook.add(sifting_sub, text="  🔍 Basis Alignment & Sifting Visualizer  ")

        ttk.Label(
            sifting_sub,
            text="Alice vs. Bob Photon-by-Photon Transmission Stream (Green = Matching Basis, Kept in Sifted Key):",
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w", pady=(0, 4))

        self.sifting_text = scrolledtext.ScrolledText(sifting_sub, height=9, font=("Consolas", 10), wrap="none")
        self.sifting_text.pack(fill="both", expand=True)

        # Sub-Tab B: Qiskit Quantum Circuit Diagram
        circuit_sub = ttk.Frame(sub_notebook, padding=6)
        sub_notebook.add(circuit_sub, text="  ⚛️ Qiskit Quantum Circuit Diagram  ")

        circuit_ctrl = ttk.Frame(circuit_sub)
        circuit_ctrl.pack(fill="x", pady=(0, 4))

        ttk.Label(circuit_ctrl, text="Bit:").pack(side="left", padx=2)
        self.circ_bit_var = tk.StringVar(value="0")
        ttk.Combobox(circuit_ctrl, textvariable=self.circ_bit_var, values=["0", "1"], state="readonly", width=3).pack(side="left", padx=2)

        ttk.Label(circuit_ctrl, text="Alice Basis:").pack(side="left", padx=(8, 2))
        self.circ_abasis_var = tk.StringVar(value="Z")
        ttk.Combobox(circuit_ctrl, textvariable=self.circ_abasis_var, values=["Z", "X"], state="readonly", width=3).pack(side="left", padx=2)

        ttk.Label(circuit_ctrl, text="Bob Basis:").pack(side="left", padx=(8, 2))
        self.circ_bbasis_var = tk.StringVar(value="Z")
        ttk.Combobox(circuit_ctrl, textvariable=self.circ_bbasis_var, values=["Z", "X"], state="readonly", width=3).pack(side="left", padx=2)

        ttk.Button(circuit_ctrl, text="Generate Circuit", command=self._update_circuit_view).pack(side="left", padx=10)

        disclaimer_lbl = tk.Label(
            circuit_sub,
            text="Note: This circuit diagram represents the mathematical quantum gate simulation in Qiskit, not a physical hardware device.",
            font=("Segoe UI", 8, "italic"),
            fg="#7f8c8d",
            bg=self.BG_COLOR,
        )
        disclaimer_lbl.pack(anchor="w", pady=(2, 2))

        self.circuit_text = scrolledtext.ScrolledText(circuit_sub, height=7, font=("Consolas", 11), wrap="none")
        self.circuit_text.pack(fill="both", expand=True)
        self._update_circuit_view()

        # Sub-Tab C: Full Transmission Table Log
        log_sub = ttk.Frame(sub_notebook, padding=6)
        sub_notebook.add(log_sub, text="  📋 Full Transmission Log  ")

        self.log_text = scrolledtext.ScrolledText(log_sub, height=9, font=("Consolas", 9), wrap="none")
        self.log_text.pack(fill="both", expand=True)

    # -------------------------------------------------------------
    # TAB 2: SECURE MESSAGING (ENCRYPTION & DECRYPTION)
    # -------------------------------------------------------------
    def _setup_messaging_tab(self, parent):
        """Builds message encryption and decryption controls."""
        container = ttk.Frame(parent, padding=10)
        container.pack(fill="both", expand=True)

        info_box = tk.Label(
            container,
            text="Classical One-Time Pad (XOR) Encryption using BB84 Candidate Key\n"
                 "Architecture: Alice -> BB84 -> Shared Candidate Key -> Classical Encryption -> Ciphertext -> Bob -> Decryption",
            font=("Segoe UI", 9, "italic"),
            bg="#e8f8f5",
            fg="#16a085",
            padx=10,
            pady=6,
            relief="groove",
        )
        info_box.pack(fill="x", pady=(0, 8))

        # Alice Encryption
        alice_frame = ttk.LabelFrame(container, text=" Step 1: Alice Encrypts Message ", padding=10)
        alice_frame.pack(fill="x", pady=4)

        ttk.Label(alice_frame, text="Plaintext Message:").grid(row=0, column=0, sticky="w", pady=3)
        self.msg_input_var = tk.StringVar(value="HELLO QUANTUM")
        self.msg_entry = ttk.Entry(alice_frame, textvariable=self.msg_input_var, width=35)
        self.msg_entry.grid(row=0, column=1, sticky="w", padx=6, pady=3)

        self.encrypt_btn = ttk.Button(
            alice_frame,
            text="🔒 Encrypt Message (XOR)",
            style="Success.TButton",
            command=self._handle_encrypt_message,
        )
        self.encrypt_btn.grid(row=0, column=2, padx=10, pady=3)

        ttk.Label(alice_frame, text="Ciphertext (Public Transmission):").grid(row=1, column=0, sticky="w", pady=3)
        self.cipher_var = tk.StringVar(value="--")
        self.cipher_entry = ttk.Entry(alice_frame, textvariable=self.cipher_var, state="readonly", font=("Consolas", 10), width=45)
        self.cipher_entry.grid(row=1, column=1, columnspan=2, sticky="ew", padx=6, pady=3)

        # Bob Decryption
        bob_frame = ttk.LabelFrame(container, text=" Step 2: Bob Decrypts Ciphertext ", padding=10)
        bob_frame.pack(fill="x", pady=4)

        self.decrypt_btn = ttk.Button(
            bob_frame,
            text="🔓 Decrypt Message (XOR)",
            style="Accent.TButton",
            command=self._handle_decrypt_message,
        )
        self.decrypt_btn.grid(row=0, column=0, padx=6, pady=4)

        self.lbl_decrypt_verdict = tk.Label(bob_frame, text="Status: Waiting for encryption...", font=("Segoe UI", 10))
        self.lbl_decrypt_verdict.grid(row=0, column=1, sticky="w", padx=10)

        ttk.Label(bob_frame, text="Recovered Plaintext:").grid(row=1, column=0, sticky="w", pady=3)
        self.recovered_var = tk.StringVar(value="--")
        self.recovered_entry = ttk.Entry(bob_frame, textvariable=self.recovered_var, state="readonly", font=("Segoe UI", 11, "bold"), width=35)
        self.recovered_entry.grid(row=1, column=1, sticky="w", padx=6, pady=3)

        # Cryptographic Details Log
        ttk.Label(container, text="Cryptographic Details & Bitwise Operations:").pack(anchor="w", pady=(8, 2))
        self.msg_log = scrolledtext.ScrolledText(container, height=8, font=("Consolas", 9), wrap="none")
        self.msg_log.pack(fill="both", expand=True)

    # -------------------------------------------------------------
    # TAB 3: SCIENTIFIC RESEARCH GRAPHS
    # -------------------------------------------------------------
    def _setup_graphs_tab(self, parent):
        """Builds viewer for scientific matplotlib research graphs."""
        top_bar = ttk.Frame(parent)
        top_bar.pack(fill="x", pady=(0, 6))

        ttk.Label(top_bar, text="Select Graph:", font=("Segoe UI", 10, "bold")).pack(side="left", padx=4)

        graphs = [
            ("1. QBER vs. Noise", "1_qber_vs_noise.png"),
            ("2. Eve OFF vs. ON", "2_qber_eve_off_vs_on.png"),
            ("3. Sifted Key Yield", "3_sifted_key_vs_qubits.png"),
            ("4. Basis Matching Dist.", "4_basis_matching_percentage.png"),
        ]

        for title, filename in graphs:
            btn = ttk.Button(
                top_bar,
                text=title,
                command=lambda f=filename: self._display_graph_image(f),
            )
            btn.pack(side="left", padx=3)

        regen_btn = ttk.Button(
            top_bar,
            text="🔄 Regenerate All Graphs",
            command=self._handle_regenerate_graphs,
        )
        regen_btn.pack(side="right", padx=4)

        self.graph_display_frame = ttk.Frame(parent, relief="sunken")
        self.graph_display_frame.pack(fill="both", expand=True)

        self.graph_label = ttk.Label(self.graph_display_frame, text="Click a button above to display the corresponding scientific graph.")
        self.graph_label.pack(expand=True)

    def _build_statusbar(self):
        """Builds the bottom application status bar."""
        self.statusbar = tk.Label(
            self.root,
            text="Ready | Q-Crypt BB84 Simulator v1.1",
            bd=1,
            relief="sunken",
            anchor="w",
            font=("Segoe UI", 9),
            padx=8,
            pady=3,
        )
        self.statusbar.pack(side="bottom", fill="x")

    # -------------------------------------------------------------
    # EVENT HANDLERS & SIMULATION DISPATCH
    # -------------------------------------------------------------
    def _on_control_change(self):
        """Updates the banner when Eve or Noise controls change."""
        eve_on = self.eve_var.get()
        noise_lvl = self.noise_level_var.get() if self.noise_var.get() else "OFF"
        self._update_pipeline_status(eve_on, noise_lvl)

    def _update_circuit_view(self):
        """Updates the textual Qiskit quantum circuit display."""
        try:
            bit = int(self.circ_bit_var.get())
            abasis = self.circ_abasis_var.get()
            bbasis = self.circ_bbasis_var.get()
            diag = generate_educational_circuit(bit, abasis, bbasis)

            state_name = ("|0>" if bit == 0 else "|1>") if abasis == "Z" else ("|+>" if bit == 0 else "|->")
            match_status = "MATCH (Deterministic 100%)" if abasis == bbasis else "MISMATCH (Probabilistic 50/50)"

            self.circuit_text.delete("1.0", tk.END)
            self.circuit_text.insert(tk.END, f"=== Quantum Circuit Model: Alice prepares {state_name} ({abasis} basis) -> Bob measures in {bbasis} basis ===\n")
            self.circuit_text.insert(tk.END, f"Basis Alignment: {match_status}\n\n")
            self.circuit_text.insert(tk.END, diag)
            self.circuit_text.insert(tk.END, "\n\nLegend: X = Pauli-X Bit Flip Gate | H = Hadamard Superposition Gate | M = Quantum Detector Measurement\n")
        except Exception as e:
            self.circuit_text.delete("1.0", tk.END)
            self.circuit_text.insert(tk.END, f"Error generating circuit: {e}")

    def _handle_run_bb84(self):
        """Executes a single BB84 quantum simulation and populates all visualizers."""
        try:
            num_qubits = int(self.qubit_var.get().strip())
            if num_qubits <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid positive integer for number of qubits.")
            return

        try:
            threshold = float(self.thresh_var.get().strip())
            if not (0.0 <= threshold <= 1.0):
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Acceptance threshold must be a decimal between 0.0 and 1.0 (e.g., 0.11).")
            return

        eve_enabled = self.eve_var.get()
        noise_enabled = self.noise_var.get()
        noise_level = self.noise_level_var.get() if noise_enabled else "OFF"
        self._update_pipeline_status(eve_enabled, noise_level)

        self.statusbar.config(text="Running Qiskit quantum simulation... Please wait.")
        self.root.update_idletasks()

        config = ExperimentConfig(
            num_qubits=num_qubits,
            eve_enabled=eve_enabled,
            noise_enabled=noise_enabled,
            noise_level=noise_level,
            qber_threshold=threshold,
        )

        try:
            result = run_experiment(config)
            self.current_result = result

            # Update Summary Metrics
            self.lbl_qubits_sent.config(text=f"Qubits: {result.total_qubits}")
            self.lbl_matching_bases.config(text=f"Matches: {len(result.matching_positions)}")
            self.lbl_sifted_len.config(text=f"Sifted Key: {len(result.alice_sifted_key)} bits")
            self.lbl_qber.config(text=f"QBER: {result.qber * 100:.2f}%")

            if result.status == "PASSED":
                self.lbl_status.config(text="STATUS: PASSED (Accepted)", bg=self.SUCCESS_COLOR, fg="white")
            else:
                self.lbl_status.config(text="STATUS: ABORTED (Rejected)", bg=self.DANGER_COLOR, fg="white")

            # Update Sifting Alignment Visualizer
            self.sifting_text.delete("1.0", tk.END)
            display_limit = min(num_qubits, 30)

            alice_bits_str = " ".join(f"{result.alice_bits[i]:^3}" for i in range(display_limit))
            alice_bases_str = " ".join(f"{result.alice_bases[i]:^3}" for i in range(display_limit))
            bob_bases_str = " ".join(f"{result.bob_bases[i]:^3}" for i in range(display_limit))
            bob_res_str = " ".join(f"{result.bob_results[i]:^3}" for i in range(display_limit))

            matching_set = set(result.matching_positions)
            match_sym_str = " ".join(f"{'OK' if i in matching_set else '--':^3}" for i in range(display_limit))
            sifted_str = " ".join(f"{str(result.alice_bits[i]) if i in matching_set else '-':^3}" for i in range(display_limit))

            self.sifting_text.insert(tk.END, f"Index Position   : " + " ".join(f"{i:^3}" for i in range(display_limit)) + "\n")
            self.sifting_text.insert(tk.END, f"Alice Raw Bits   : {alice_bits_str}\n")
            self.sifting_text.insert(tk.END, f"Alice Bases      : {alice_bases_str}\n")
            self.sifting_text.insert(tk.END, f"Bob Bases        : {bob_bases_str}\n")
            self.sifting_text.insert(tk.END, f"Matching Basis?  : {match_sym_str}\n")
            self.sifting_text.insert(tk.END, f"Bob Measured     : {bob_res_str}\n")
            self.sifting_text.insert(tk.END, f"-------------------" + "----" * display_limit + "\n")
            self.sifting_text.insert(tk.END, f"Sifted Key Stream: {sifted_str}\n\n")
            self.sifting_text.insert(tk.END, f"Alice Sifted Key : {''.join(map(str, result.alice_sifted_key))}\n")
            self.sifting_text.insert(tk.END, f"Bob Sifted Key   : {''.join(map(str, result.bob_sifted_key))}\n")
            self.sifting_text.insert(tk.END, f"Candidate Key    : {''.join(map(str, result.alice_candidate_key))}\n")

            if num_qubits > display_limit:
                self.sifting_text.insert(tk.END, f"\n[... display truncated for neatness; showing first {display_limit} of {num_qubits} qubits ...]\n")

            # Update Log Table
            self.log_text.delete("1.0", tk.END)
            self.log_text.insert(tk.END, f"{'Idx':^5}|{'Alice Bit':^10}|{'Alice Bas':^10}|{'Bob Bas':^10}|{'Bob Res':^10}|{'Match?':^8}\n")
            self.log_text.insert(tk.END, "-" * 60 + "\n")
            for i in range(display_limit):
                matched = "YES" if i in matching_set else "NO"
                self.log_text.insert(
                    tk.END,
                    f"{i:^5}|{result.alice_bits[i]:^10}|{result.alice_bases[i]:^10}|{result.bob_bases[i]:^10}|{result.bob_results[i]:^10}|{matched:^8}\n"
                )

            self.statusbar.config(text=f"Simulation Complete: {result.status} | QBER: {result.qber * 100:.2f}% | Sifted: {len(result.alice_sifted_key)} bits")

        except Exception as e:
            messagebox.showerror("Simulation Error", f"An error occurred while running BB84: {e}")
            self.statusbar.config(text="Error occurred during simulation.")

    def _handle_run_multi_trial(self):
        """Runs a 10-trial statistical batch and saves to CSV."""
        try:
            num_qubits = int(self.qubit_var.get().strip())
        except ValueError:
            num_qubits = 50

        try:
            threshold = float(self.thresh_var.get().strip())
        except ValueError:
            threshold = 0.11

        eve_enabled = self.eve_var.get()
        noise_level = self.noise_level_var.get() if self.noise_var.get() else "OFF"

        self.statusbar.config(text="Running 10-trial Monte Carlo simulation & exporting CSV...")
        self.root.update_idletasks()

        summary = run_multi_experiment(
            num_qubits=num_qubits,
            num_repetitions=10,
            eve_enabled=eve_enabled,
            noise_level=noise_level,
            qber_threshold=threshold,
            save_csv=True,
            output_dir="experiments",
        )

        msg = (
            f"Multi-Trial Experiment Completed (10 Trials of {num_qubits} Qubits):\n\n"
            f"• Average QBER: {summary.avg_qber * 100:.2f}%\n"
            f"• Min / Max QBER: {summary.min_qber * 100:.2f}% / {summary.max_qber * 100:.2f}%\n"
            f"• Average Sifted Key Length: {summary.avg_sifted_key_len:.1f} bits\n"
            f"• Trials Passed: {summary.passed_runs} / 10 ({summary.passed_runs * 10}%)\n\n"
            f"Saved CSV Log: {summary.csv_filepath}"
        )
        messagebox.showinfo("Multi-Trial Experiment Report", msg)
        self.statusbar.config(text=f"Multi-trial results saved to {summary.csv_filepath}")

    def _handle_encrypt_message(self):
        """Classically encrypts Alice's message using the candidate key."""
        if not self.current_result:
            messagebox.showwarning("No Key", "Please run the BB84 simulation first to establish a candidate key.")
            return

        if self.current_result.status != "PASSED":
            messagebox.showerror(
                "Key Security Violation",
                f"Cannot encrypt: Candidate key was REJECTED / ABORTED.\n"
                f"Observed QBER ({self.current_result.qber * 100:.2f}%) exceeded threshold.\n"
                "Possible eavesdropping or high noise detected!"
            )
            return

        plaintext = self.msg_input_var.get().strip()
        if not plaintext:
            messagebox.showwarning("Empty Message", "Please enter a message to encrypt.")
            return

        cand_key = self.current_result.alice_candidate_key
        req_bits = len(text_to_bits(plaintext))

        if len(cand_key) < req_bits:
            messagebox.showerror(
                "Key Length Insufficient",
                f"The candidate key ({len(cand_key)} bits) is shorter than the message ({req_bits} bits needed).\n"
                f"Please run BB84 with at least {int(req_bits * 3.5)} qubits."
            )
            return

        payload = encrypt_message(plaintext, cand_key)
        self.current_ciphertext_payload = payload

        self.cipher_var.set(f"0x{payload['ciphertext_hex']}")
        self.recovered_var.set("--")
        self.lbl_decrypt_verdict.config(text="Status: Ciphertext ready for Bob.", fg=self.ACCENT_COLOR)

        self.msg_log.delete("1.0", tk.END)
        self.msg_log.insert(tk.END, "=== ALICE ONE-TIME PAD (XOR) ENCRYPTION ===\n")
        self.msg_log.insert(tk.END, f"Plaintext (M)        : '{plaintext}'\n")
        self.msg_log.insert(tk.END, f"Plaintext Bits       : {''.join(map(str, payload['plaintext_bits']))}\n")
        self.msg_log.insert(tk.END, f"Alice Key Slice (K)  : {''.join(map(str, payload['key_slice']))}\n")
        self.msg_log.insert(tk.END, f"Ciphertext Bits (C)  : {''.join(map(str, payload['ciphertext_bits']))}\n")
        self.msg_log.insert(tk.END, f"Public Ciphertext Hex: 0x{payload['ciphertext_hex']}\n\n")

        self.statusbar.config(text=f"Message '{plaintext}' encrypted successfully.")

    def _handle_decrypt_message(self):
        """Classically decrypts ciphertext using Bob's candidate key."""
        if not self.current_ciphertext_payload or not self.current_result:
            messagebox.showwarning("No Ciphertext", "Please encrypt a message first.")
            return

        cipher_bits = self.current_ciphertext_payload["ciphertext_bits"]
        bob_key = self.current_result.bob_candidate_key

        decrypted_text = decrypt_message(cipher_bits, bob_key)
        self.recovered_var.set(decrypted_text)

        original_text = self.current_ciphertext_payload["plaintext"]
        if decrypted_text == original_text:
            self.lbl_decrypt_verdict.config(text="[SUCCESS] 100% Message Recovery Match!", fg=self.SUCCESS_COLOR, font=("Segoe UI", 10, "bold"))
        else:
            self.lbl_decrypt_verdict.config(text="[ERROR] Decryption Mismatch!", fg=self.DANGER_COLOR, font=("Segoe UI", 10, "bold"))

        self.msg_log.insert(tk.END, "=== BOB ONE-TIME PAD (XOR) DECRYPTION ===\n")
        self.msg_log.insert(tk.END, f"Ciphertext Bits (C)  : {''.join(map(str, cipher_bits))}\n")
        self.msg_log.insert(tk.END, f"Bob Key Slice (K)    : {''.join(map(str, bob_key[:len(cipher_bits)]))}\n")
        self.msg_log.insert(tk.END, f"Decrypted Bits (M)   : {''.join(map(str, text_to_bits(decrypted_text)))}\n")
        self.msg_log.insert(tk.END, f"Recovered Message    : '{decrypted_text}'\n")

        self.statusbar.config(text="Decryption completed.")

    def _display_graph_image(self, filename: str):
        """Loads and renders a research plot image inside the Graphs tab."""
        filepath = os.path.join("screenshots", filename)
        if not os.path.exists(filepath):
            messagebox.showwarning("Image Not Found", f"Graph file '{filepath}' was not found. Click 'Regenerate All Graphs'.")
            return

        if not HAS_PIL:
            messagebox.showinfo("Graph Location", f"Graph saved at: {os.path.abspath(filepath)}")
            return

        try:
            img = Image.open(filepath)
            img.thumbnail((720, 460), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)

            self.graph_label.config(image=photo, text="")
            self.graph_label.image = photo
            self.statusbar.config(text=f"Displayed: {filename}")
        except Exception as e:
            messagebox.showerror("Display Error", f"Could not load graph: {e}")

    def _handle_regenerate_graphs(self):
        """Regenerates all 4 scientific plots from fresh simulation data."""
        self.statusbar.config(text="Regenerating all 4 graphs with fresh simulation runs... Please wait.")
        self.root.update_idletasks()

        try:
            from experiments.plot_results import generate_all_graphs
            generate_all_graphs()
            messagebox.showinfo("Graphs Regenerated", "All 4 scientific research graphs have been re-calculated and updated in 'screenshots/'!")
            self._display_graph_image("1_qber_vs_noise.png")
            self.statusbar.config(text="All 4 graphs successfully updated.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to regenerate graphs: {e}")
            self.statusbar.config(text="Graph generation failed.")


def start_gui():
    """Launches the Q-Crypt Tkinter GUI."""
    root = tk.Tk()
    app = QCryptGUI(root)
    root.mainloop()


if __name__ == "__main__":
    start_gui()
