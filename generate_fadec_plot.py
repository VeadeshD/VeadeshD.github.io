import numpy as np
import matplotlib.pyplot as plt

# Simulate FADEC PID Control Step Response for Ion Thruster Voltage Regulation
t = np.linspace(0, 50, 1000) # Time in nanoseconds

# Simulated hardware step response with slight overshoot and quick settling (underdamped but tuned)
# y(t) = 1 - e^(-zeta * w * t) * (cos(wd * t) + (zeta / sqrt(1 - zeta^2)) * sin(wd * t))
zeta = 0.6
w = 0.3
wd = w * np.sqrt(1 - zeta**2)

voltage_target = 500  # 500V target for the thruster
response = voltage_target * (1 - np.exp(-zeta * w * t) * (np.cos(wd * t) + (zeta / np.sqrt(1 - zeta**2)) * np.sin(wd * t)))

# Add high-frequency ADC noise
noise = np.random.normal(0, 5, 1000)
raw_adc_signal = response + noise

# Simulate the Digital Moving-Average Filter (the one implemented in SystemVerilog)
window_size = 15
filtered_signal = np.convolve(raw_adc_signal, np.ones(window_size)/window_size, mode='same')
filtered_signal[:window_size//2] = raw_adc_signal[:window_size//2] # Fix edges

# Configure deep dark mode plotting to match the portfolio aesthetic
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
fig.patch.set_facecolor('#050505')
ax.set_facecolor('#050505')

# Plot the lines
ax.plot(t, raw_adc_signal, color='#7000ff', alpha=0.3, label='Raw ADC Telemetry (Noisy)', linewidth=1)
ax.plot(t, filtered_signal, color='#00f0ff', label='FPGA DSP Filtered Signal', linewidth=2.5)
ax.axhline(voltage_target, color='white', linestyle='--', alpha=0.5, label='Target Voltage (500V)')

# Add grid and labels
ax.grid(color='white', linestyle=':', alpha=0.1)
ax.set_title('FADEC SystemVerilog Hardware PID Response (Nanoseconds)', color='white', pad=20, fontsize=14, fontweight='bold')
ax.set_xlabel('Time (ns)', color='#a0a0a0', fontsize=12)
ax.set_ylabel('Thruster Bus Voltage (V)', color='#a0a0a0', fontsize=12)
ax.legend(loc='lower right', facecolor='#050505', edgecolor='#333333')

# Clean up borders
for spine in ax.spines.values():
    spine.set_color('#333333')

plt.tight_layout()
plt.savefig('fadec_plot.jpg', format='jpg', facecolor='#050505')
print("fadec_plot.jpg generated successfully.")
