### Problem Statement

We are given a one-dimensional chain with:
- Lattice constant: \( a \)
- Optical vibration mode with dispersion relation: \( \omega = \omega_0 - \gamma k^2 \)
- Condition: \( \gamma\left(\frac{\pi}{a}\right)^2 \ll \omega_0 \)

We need to find expressions for:
a. The density of states (DOS).
b. The heat capacity at high and low temperatures.

### Part a: Density of States (DOS)

#### Step 1: Understand the Dispersion Relation
The given dispersion relation is:
\[ \omega = \omega_0 - \gamma k^2 \]
This describes an optical mode where the frequency decreases with increasing \( k \) (since \( \gamma > 0 \)).

#### Step 2: Solve for \( k \) in Terms of \( \omega \)
Rearrange the dispersion relation to express \( k \):
\[ \omega_0 - \omega = \gamma k^2 \]
\[ k^2 = \frac{\omega_0 - \omega}{\gamma} \]
\[ k = \sqrt{\frac{\omega_0 - \omega}{\gamma}} \]

#### Step 3: Determine the Range of \( \omega \)
From the condition \( \gamma\left(\frac{\pi}{a}\right)^2 \ll \omega_0 \), the maximum \( k \) is \( \frac{\pi}{a} \) (edge of the first Brillouin zone for a 1D chain). The corresponding minimum frequency \( \omega_{\text{min}} \) is:
\[ \omega_{\text{min}} = \omega_0 - \gamma \left(\frac{\pi}{a}\right)^2 \]
Given the condition \( \gamma\left(\frac{\pi}{a}\right)^2 \ll \omega_0 \), \( \omega_{\text{min}} \) is very close to \( \omega_0 \), so \( \omega \) ranges from \( \omega_{\text{min}} \) to \( \omega_0 \).

#### Step 4: Calculate the Density of States \( g(\omega) \)
In 1D, the density of states is given by:
\[ g(\omega) = \frac{L}{\pi} \left| \frac{dk}{d\omega} \right| \]
From \( k = \sqrt{\frac{\omega_0 - \omega}{\gamma}} \):
\[ \frac{dk}{d\omega} = \frac{d}{d\omega} \left( \frac{\omega_0 - \omega}{\gamma} \right)^{1/2} = \frac{1}{2} \left( \frac{\omega_0 - \omega}{\gamma} \right)^{-1/2} \cdot \left( -\frac{1}{\gamma} \right) = -\frac{1}{2 \sqrt{\gamma (\omega_0 - \omega)}} \]
Thus:
\[ \left| \frac{dk}{d\omega} \right| = \frac{1}{2 \sqrt{\gamma (\omega_0 - \omega)}} \]
So the DOS is:
\[ g(\omega) = \frac{L}{\pi} \cdot \frac{1}{2 \sqrt{\gamma (\omega_0 - \omega)}} = \frac{L}{2 \pi \sqrt{\gamma (\omega_0 - \omega)}} \]

#### Final Answer for Part a:
The density of states is:
\[ g(\omega) = \frac{L}{2 \pi \sqrt{\gamma (\omega_0 - \omega)}} \]

### Part b: Heat Capacity at High and Low Temperatures

#### General Approach
The heat capacity \( C_V \) can be calculated from the density of states using:
\[ C_V = \int d\omega \, g(\omega) \, \frac{\partial}{\partial T} \left( \frac{\hbar \omega}{e^{\hbar \omega / k_B T} - 1} \right) \]
At high and low temperatures, we can make approximations.

#### High-Temperature Limit (\( k_B T \gg \hbar \omega_0 \))
In the high-temperature limit, the Bose-Einstein distribution can be approximated as:
\[ \frac{1}{e^{\hbar \omega / k_B T} - 1} \approx \frac{k_B T}{\hbar \omega} \]
Thus:
\[ \frac{\partial}{\partial T} \left( \frac{\hbar \omega}{e^{\hbar \omega / k_B T} - 1} \right) \approx \frac{\partial}{\partial T} (k_B T) = k_B \]
So:
\[ C_V \approx \int d\omega \, g(\omega) \, k_B \]
Substitute \( g(\omega) \):
\[ C_V \approx k_B \int_{\omega_{\text{min}}}^{\omega_0} \frac{L}{2 \pi \sqrt{\gamma (\omega_0 - \omega)}} d\omega \]
Let \( x = \omega_0 - \omega \), \( dx = -d\omega \), limits reverse:
\[ C_V \approx \frac{L k_B}{2 \pi \sqrt{\gamma}} \int_{0}^{\gamma (\pi/a)^2} \frac{dx}{\sqrt{x}} \]
\[ \int \frac{dx}{\sqrt{x}} = 2 \sqrt{x} \]
Evaluate:
\[ C_V \approx \frac{L k_B}{2 \pi \sqrt{\gamma}} \cdot 2 \sqrt{\gamma (\pi/a)^2} = \frac{L k_B}{\pi \sqrt{\gamma}} \cdot \sqrt{\gamma} \cdot \frac{\pi}{a} = \frac{L k_B}{a} \]
Since \( N = L/a \) (number of unit cells in 1D chain):
\[ C_V \approx N k_B \]
This is the classical Dulong-Petit law, expected for high temperatures.

#### Low-Temperature Limit (\( k_B T \ll \hbar \omega_{\text{min}} \))
At low temperatures, only frequencies near \( \omega_{\text{min}} \) contribute significantly. However, since \( \omega_{\text{min}} \approx \omega_0 \) (from the given condition), and \( \hbar \omega_0 \gg k_B T \), the occupation number is exponentially small:
\[ \frac{1}{e^{\hbar \omega / k_B T} - 1} \approx e^{-\hbar \omega / k_B T} \]
Thus:
\[ \frac{\partial}{\partial T} \left( \frac{\hbar \omega}{e^{\hbar \omega / k_B T} - 1} \right) \approx \frac{\partial}{\partial T} \left( \hbar \omega e^{-\hbar \omega / k_B T} \right) = \frac{\hbar^2 \omega^2}{k_B T^2} e^{-\hbar \omega / k_B T} \]
So:
\[ C_V \approx \int d\omega \, g(\omega) \, \frac{\hbar^2 \omega^2}{k_B T^2} e^{-\hbar \omega / k_B T} \]
Substitute \( g(\omega) \):
\[ C_V \approx \frac{L}{2 \pi \sqrt{\gamma}} \int_{\omega_{\text{min}}}^{\omega_0} \frac{\hbar^2 \omega^2}{k_B T^2} \frac{e^{-\hbar \omega / k_B T}}{\sqrt{\omega_0 - \omega}} d\omega \]
Since \( \omega \approx \omega_0 \) dominates, let \( \omega = \omega_0 - x \), \( x \ll \omega_0 \):
\[ C_V \approx \frac{L \hbar^2 \omega_0^2}{2 \pi \sqrt{\gamma} k_B T^2} \int_{0}^{\gamma (\pi/a)^2} \frac{e^{-\hbar \omega_0 / k_B T} e^{\hbar x / k_B T}}{\sqrt{x}} dx \]
The integral is dominated by the exponential decay, leading to:
\[ C_V \propto e^{-\hbar \omega_0 / k_B T} \]
Thus, the heat capacity is exponentially suppressed at low temperatures.

#### Final Answer for Part b:
- At high temperatures (\( k_B T \gg \hbar \omega_0 \)): \( C_V \approx N k_B \)
- At low temperatures (\( k_B T \ll \hbar \omega_0 \)): \( C_V \propto e^{-\hbar \omega_0 / k_B T} \)