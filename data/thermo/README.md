# QuantumPioneer Species Thermodynamics Dataset

| Column                       | Type   | Units        | Description                                     |
| ---------------------------- | ------ | ------------ | ----------------------------------------------- |
| **`smiles`**                 | string | —            | Canonical SMILES representation of the species  |
| **`H298`**                   | number | J/mol        | Standard enthalpy of formation at 298 K         |
| **`S298`**                   | number | J/(mol·K)    | Standard entropy of formation at 298 K          |
| **`Cp300`**                  | number | J/(mol·K)    | Constant pressure heat capacity at 300 K        |
| **`dlpno_sp_hartree`**       | number | Hartree      | DLPNO-CCSD(T)-F12d single-point energy          |
| **`dft_zpe_scaled_hartree`** | number | Hartree      | Scaled DFT zero-point energy (factor: 0.972387) |
| **`CpInf`**                  | number | J/(mol·K)    | Heat capacity at infinite temperature           |
| **`a0`**                     | number | —            | Zeroth-order Wilhoit polynomial coefficient     |
| **`a1`**                     | number | —            | First-order Wilhoit polynomial coefficient      |
| **`a2`**                     | number | —            | Second-order Wilhoit polynomial coefficient     |
| **`a3`**                     | number | —            | Third-order Wilhoit polynomial coefficient      |
| **`H0`**                     | number | J/mol        | Wilhoit integration constant for enthalpy       |
| **`S0`**                     | number | J/(mol·K)    | Wilhoit integration constant for entropy        |
| **`B`**                      | number | K            | Wilhoit scaled temperature coefficient          |
| **`DHPM`**                   | number | J/mol        | Petersson-to-Melius enthalpy difference         |

## Notes

- All molecular structures are represented using canonical SMILES without atom map numbers

- Thermodynamic properties (H298, S298, Cp300) are calculated from DFT-optimized geometries with
DLPNO-CCSD(T)-F12d single-point calculations

- The standard enthalpy of formation (`H298`) and Wilhoit integration constant for enthalpy (`H0`)
derive from calculations using Petersson-type bond additivity corrections (BACs). Add `DHPM` to
either of these in order to obtain their Melius-type BAC-corrected versions.

## Wilhoit Model

The Wilhoit model provides a physically meaningful representation of temperature-dependent heat capacity, guaranteeing correct limits at zero and infinite temperature. The model is defined by the following equations:

### Heat Capacity

$$
        C_\mathrm{p}(T) = C_\mathrm{p}(0) + \left[ C_\mathrm{p}(\infty) -
        C_\mathrm{p}(0) \right] y^2 \left[ 1 + (y - 1) \sum_{i=0}^3 a_i y^i \right]
$$

where $y \equiv T/(T + B)$ is a scaled temperature ranging from zero to one.

$C_\mathrm{p}(0)$ is the heat capacity at zero temperature, whose value is equal to 33.2579 J/(mol·K) for all species in the dataset.

### Enthalpy

$$
\begin{aligned}
H(T) &= H_0 +
        C_\mathrm{p}(0) T - \Bigg\{
            \left(2 + \sum_{i=0}^3 a_i\right) \left[
                \frac{y}{2} - 1 + \left( \frac{1}{y} - 1 \right) \ln \frac{T}{y}
            \right] \\ &+ 
            y^2 \sum_{i=0}^3 \frac{y^i}{(i+2)(i+3)} \sum_{j=0}^3 f_{ij} a_j
        \Bigg\} \left[ C_\mathrm{p}(\infty) - C_\mathrm{p}(0) \right] T
\end{aligned}
$$

where

$$
f_{ij} = \begin{cases}
    0 & \text{if } i < j, \\
    3 + j & \text{if } i = j, \\
    1 & \text{if } i > j.
\end{cases}
$$

### Entropy

$$
        S(T) = S_0 +
        C_\mathrm{p}(\infty) \ln T - \left[ C_\mathrm{p}(\infty) - C_\mathrm{p}(0) \right]
        \left[ \ln y + \left( 1 + y \sum_{i=0}^3 \frac{a_i y^i}{2+i} \right) y
        \right]
$$
