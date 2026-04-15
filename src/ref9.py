from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


plt.rcParams.update(
    {
        "font.family": "serif",
        "mathtext.fontset": "cm",
        "font.size": 11,
    }
)


SEED = 42
STEPS = 300
MIGRATION_START = 85
CTA_ACTIVATION = 190


def logistic(value: float | np.ndarray) -> float | np.ndarray:
    return 1.0 / (1.0 + np.exp(-value))


def simulate_proxy_run(seed: int = SEED, steps: int = STEPS) -> dict[str, list[float] | int]:
    rng = np.random.default_rng(seed)
    coordination_gap = 2.85
    backlog = 1.45
    raw_trust = 0.018

    hamiltonian_trace: list[float] = []
    trust_trace: list[float] = []
    latent_trace: list[float] = []
    cta_trace: list[float] = []

    for step in range(steps):
        latent_strength = float(logistic((step - MIGRATION_START) / 18.0))
        cta_interface = float(logistic((step - CTA_ACTIVATION) / 14.0))
        semantic_annealing = float(np.exp(-((step - (MIGRATION_START + 28)) / 24.0) ** 2))

        noise_scale = 0.24 * (1.0 - latent_strength) + 0.11 * (latent_strength * (1.0 - cta_interface)) + 0.05 * cta_interface
        shock = float(noise_scale * rng.normal())

        control_gain = 0.085 + 0.10 * latent_strength + 0.12 * cta_interface
        drift = 0.022 * (1.0 - latent_strength) - control_gain * coordination_gap + 0.17 * semantic_annealing * (1.0 - coordination_gap / 3.1)

        coordination_gap = max(0.42, coordination_gap + drift + shock)
        backlog = max(0.18, backlog + 0.24 * abs(shock) + 0.04 * (1.0 - latent_strength) - (0.045 + 0.09 * latent_strength + 0.12 * cta_interface) * backlog)
        volatility = 0.25 + 0.92 * abs(shock)

        hamiltonian = 168.0 + 43.0 * coordination_gap + 30.0 * backlog + 17.0 * volatility + 12.0 * (1.0 - latent_strength) + 4.5 * rng.normal()

        if hamiltonian_trace:
            improvement = max(hamiltonian_trace[-1] - hamiltonian, 0.0)
            trust_drift = 0.00010 * improvement + 0.00010 * latent_strength + 0.00020 * cta_interface - 0.00040 * abs(shock)
        else:
            trust_drift = 0.00008

        raw_trust = float(np.clip(raw_trust + trust_drift, 0.0, 0.125))

        hamiltonian_trace.append(float(hamiltonian))
        trust_trace.append(raw_trust)
        latent_trace.append(latent_strength)
        cta_trace.append(cta_interface)

    return {
        "seed": seed,
        "steps": steps,
        "migration_start": MIGRATION_START,
        "cta_activation": CTA_ACTIVATION,
        "H": hamiltonian_trace,
        "tau_raw": trust_trace,
        "latent_strength": latent_trace,
        "cta_interface": cta_trace,
    }


def draw_figure(data: dict[str, list[float] | int], output_path: Path) -> None:
    hamiltonian = np.array(data["H"], dtype=float)
    raw_trust = np.array(data["tau_raw"], dtype=float)
    steps = np.arange(int(data["steps"]))
    migration_start = int(data["migration_start"])
    cta_activation = int(data["cta_activation"])

    fig, ax_h = plt.subplots(figsize=(10.6, 7.2))
    ax_tau = ax_h.twinx()

    ax_h.axvspan(0, migration_start, color="#f5e6c8", alpha=0.35)
    ax_h.axvspan(migration_start, cta_activation, color="#dfe9f6", alpha=0.32)
    ax_h.axvspan(cta_activation, len(steps), color="#dff1de", alpha=0.28)

    ax_h.plot(steps, hamiltonian, color="#1f77b4", linewidth=2.4)
    ax_tau.plot(steps, raw_trust, color="#2ca02c", linewidth=2.5, linestyle=(0, (4, 2)))

    for marker in (migration_start, cta_activation):
        ax_h.axvline(marker, color="0.55", linestyle="--", linewidth=1.6)

    ax_h.text(41, 337, "Legacy\ncoordination", ha="center", va="center", fontsize=15, fontstyle="italic")
    ax_h.text(138, 337, "Latent Torus\nmigration", ha="center", va="center", fontsize=15, fontstyle="italic")
    ax_h.text(246, 337, "CTA-governed\nLatent Torus", ha="center", va="center", fontsize=15, fontstyle="italic")

    ax_h.annotate(
        "CTA public interface\nactivated",
        xy=(cta_activation, 215),
        xytext=(212, 285),
        color="#1b7f3b",
        fontsize=12,
        ha="left",
        arrowprops={"arrowstyle": "->", "color": "#1b7f3b", "lw": 1.5},
    )

    ax_h.set_title("Proxy Trace of Hamiltonian Reduction and Raw Trust Accumulation", fontsize=20)
    ax_h.set_xlabel("Time Step", fontsize=19)
    ax_h.set_ylabel(r"Social Hamiltonian $H$", color="#1f77b4", fontsize=19)
    ax_tau.set_ylabel(r"Mean Raw Trust Stock $\widetilde{\tau}$", color="#2ca02c", fontsize=19)

    ax_h.tick_params(axis="x", labelsize=14)
    ax_h.tick_params(axis="y", labelcolor="#1f77b4", labelsize=14)
    ax_tau.tick_params(axis="y", labelcolor="#2ca02c", labelsize=14)

    ax_h.set_xlim(-2, len(steps) + 2)
    ax_h.set_ylim(175, 350)
    ax_tau.set_ylim(0.015, 0.13)

    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    output_path = base_dir / "thesis_fig_socio_economic.png"
    data_path = base_dir / "thesis_fig_socio_economic_data.json"
    data = simulate_proxy_run()
    draw_figure(data, output_path)
    data_path.write_text(json.dumps(data, indent=2))
    print(output_path)
    print(data_path)


if __name__ == "__main__":
    main()
