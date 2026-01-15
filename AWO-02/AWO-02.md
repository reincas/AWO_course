---
title: "Applied Wave Optics: Wave Equation"
author: "Reinhard Caspary"
date: "Version date: November 27, 2025"
header-includes:
- |
  ```{=latex}
  \usepackage{caption}
  \usepackage{exscale}
  \usepackage{bbold}
  \usepackage{siunitx}
  \sisetup{range-phrase = {-}, range-units = single}
  \DeclareMathOperator{\tr}{tr}
  \usepackage{hyperref}
  \usepackage{url}
  \titlegraphic{
    \vspace{4ex}
	\includegraphics[width=2cm]{by-sa.pdf}\\[1ex]
    \footnotesize
    Except where otherwise noted, this document and its content are licensed under the\\
    \href{https://creativecommons.org/licenses/by-sa/4.0/legalcode.en}{Creative Commons Attribution-ShareAlike 4.0 International license}.\\[.5\baselineskip]
	All sources and vector graphics are available on the GitHub repository \href{https://github.com/reincas/AWO_course}{\texttt{\url{https://github.com/reincas/AWO_course}}}.
  }
  \makeatletter
  \renewcommand{\@makecaption}[2]{}
  \makeatother
  ```
aspectratio: 169
---

# Wave Equation

Identity relation from vector algebra for an arbitrary field $\mathbf{A}$ using the definition $\Delta = \boldsymbol{\nabla} \boldsymbol{\nabla}$:
$$
\boldsymbol{\nabla} \times (\boldsymbol{\nabla} \times \mathbf{A}) = \boldsymbol{\nabla} ( \boldsymbol{\nabla} \mathbf{A}) - \Delta \mathbf{A}
$$
We use it for the electric field and utilize Maxwell's equations:
\begin{align*}
  \Delta \mathbf{E}
  &= -\boldsymbol{\nabla} \times (\boldsymbol{\nabla} \times \mathbf{E}) + \boldsymbol{\nabla} (\boldsymbol{\nabla} \mathbf{E}) \\
  &= \frac{\partial}{\partial t} (\boldsymbol{\nabla} \times \mathbf{B}) + \frac{1}{\varepsilon \varepsilon_0} \boldsymbol{\nabla} (\boldsymbol{\nabla} \mathbf{D}) \\
  &= \mu \mu_0 \frac{\partial}{\partial t} (\boldsymbol{\nabla} \times \mathbf{H}) + \frac{1}{\varepsilon \varepsilon_0} \boldsymbol{\nabla} \varrho \\
  &= \mu \mu_0 \frac{\partial}{\partial t} (\mathbf{j} + \frac{\partial \mathbf{D}}{\partial t}) + 0 \\
  &= \mu \mu_0 \varepsilon \varepsilon_0 \frac {\partial^2}{\partial^2 t}\mathbf{E}
\end{align*}

---

# Wave Equation (cont.)

We get the same result, when we use the magnetic field instead. The wave equation thus reads:
\begin{align*}
  \Delta \mathbf{E} &= \mu \mu_0 \varepsilon \varepsilon_0 \frac {\partial^2}{\partial^2 t}\mathbf{E} \\
  \Delta \mathbf{H} &= \mu \mu_0 \varepsilon \varepsilon_0 \frac {\partial^2}{\partial^2 t}\mathbf{H}
\end{align*}

## Limited Validity

This derivation is only possible for constant values of $\varepsilon$, $\mu$, $\rho$, and $\mathbf{j}$.
In contrast to Maxwell's equations and the continuity equation, the wave equation is therefore restricted to **linear, isotropic, homogenous and temporally static media**.
In particular it is not valid at the interface between two different media.

---

# Harmonic Fields

Harmonic oscillation as solution of the wave equation:
$$
\mathbf{E}_\omega(\mathbf{r},t) = \frac{1}{2} \left[\mathbf{E}(\mathbf{r}) \mathrm{e}^{i \omega t} + \mathbf{E}^\ast(\mathbf{r}) \mathrm{e}^{-i \omega t}\right]
$$
Interpretation as Fourier component of an arbitrary electric field $\mathbf{E}(\mathbf{r},t)$ based on a static spectrum $a(\omega)$:
$$
\mathbf{E}(\mathbf{r},t) = \int\! a(\omega)\, \mathbf{E}_\omega(\mathbf{r},t)\, d\omega
$$

This is useful in linear systems, which do not mix spectral components.
Therefore, it is sufficient to know how the system acts on a general frequency in order to know how it acts on signals with arbitrary temporal shapes.

---

# Harmonic Fields (cont.)

For a single frequency Maxwell's equations simplify to
\begin{align*}
  \boldsymbol{\nabla} \mathbf{D} &= \rho \\
  \boldsymbol{\nabla} \mathbf{B} &= 0 \\
  \boldsymbol{\nabla} \times \mathbf{E} &= -i \omega \mathbf{B} \\
  \boldsymbol{\nabla} \times \mathbf{H} &= \mathbf{j} + i \omega \mathbf{D}
\end{align*}  
The wave equations of harmonic fields are Helmholtz equations:
\begin{align*}
  \Delta \mathbf{E} + \omega^2 \mu \mu_0 \varepsilon \varepsilon_0 \mathbf{E} &= 0 \\
  \Delta \mathbf{H} + \omega^2 \mu \mu_0 \varepsilon \varepsilon_0 \mathbf{H} &= 0
\end{align*}
Any solution to this harmonic wave equation and any linear superposition of such solutions is a physically valid electric or magnetic field inside a linear, isotropic, homogeneous and static medium.
<!---
An important example is the radiation emitted by a dipole antenna (Hertzian dipole).
-->

---

# Plane Waves

The 4D Fourier component of an arbitrary electrical field $\mathbf{E}(\mathbf{r},t)$ in Cartesian coordinates is another solution of the wave equation:
$$
\mathbf{E}_{\mathbf{k},\omega}(\mathbf{r}, t) =  \frac{1}{2} \left[\hat{\mathbf{E}}\, \mathrm{e}^{i(\omega t - \mathbf{k} \mathbf{r})} + \hat{\mathbf{E}}^\ast \mathrm{e}^{-i(\omega t - \mathbf{k}\mathbf{r})}\right]
$$
with the wave vector $\mathbf{k}$. This Fourier component allows to define the field based of a static spatio-temporal spectrum $a(\mathbf{k},\omega)$:
$$
\mathbf{E}(\mathbf{r},t) = \iiiint a(\mathbf{k},\omega)\, \mathbf{E}_{\mathbf{k},\omega}(\mathbf{r}, t)\, d\mathbf{k}\, d\omega
$$

These Fourier components are called **plane waves**.
They are periodic and infinite in time and space and are thus not representing a physically valid entity by itself.
Nevertheless, the plain wave is a very useful tool for the theoretical investigation of optical systems.
Linear superpositions of plain wave solutions provide the solution for any arbitrary wave form.

---

# Plane Waves (cont.)

The direction of the wave vector $\mathbf{k}$ is identical to the direction of the wave propagation.
The spatial period of the wave in this direction is called wavelength:
$$
\lambda = \frac{2\pi}{k}
$$
with the wave number $k = |\mathbf{k}|$.

The spectral function $\mathbf{k}(\omega)$ of the wave vector is called **dispersion relation**.
It is the only material dependent part defining the propagation characteristics of any electromagnetic wave in a specific material. It is directly linked to the propagation speed $c=\omega/k$ of the respective spectral component.

---

# Complex Wave Number

We expand the definition of the real wave number into the full complex space:
$$
k \to k - i\alpha
$$
The definition of the plane wave needs a tiny modification then:
$$
\mathbf{E}_{\mathbf{k},\omega}(\mathbf{r}, t) =  \frac{1}{2} \left[\hat{\mathbf{E}}\, \mathrm{e}^{i(\omega t - \mathbf{k} \mathbf{r})} + \hat{\mathbf{E}}^\ast \mathrm{e}^{-i(\omega t - \mathbf{k}^\ast\mathbf{r})}\right]
$$
The meaning of this modification becomes clear when we take a closer look on the spatial development of the field amplitude.
If we assume an x-polarised electric field propagating in z-direction:
$$
E_x\,\mathrm{e}^{-ikz} \to E_x\,\mathrm{e}^{-ikz - \alpha z} = E_x\,\mathrm{e}^{-\alpha z} \cdot \mathrm{e}^{-ikz}
$$
The factor $\alpha$ may thus be interpreted as a **small signal** attenuation (or gain) of the wave magnitude.

---

# Field Impedance

The rotation of an x-polarised plain wave propagating in z-direction (standard choice)
$$
\boldsymbol{\nabla} \times \mathbf{E}
= \begin{pmatrix} \partial / \partial x \\ \partial / \partial y \\ \partial / \partial z \end{pmatrix}
\times \begin{pmatrix} E_x \\ 0 \\ 0 \end{pmatrix}
$$
is non-zero only for the y-component, because its x-component is zero anyway and since the partial derivative of the field in y-direction is zero (plane wave), the z-component of the rotation is zero as well.

Faraday's law therefore reduces to a scalar expression:
\begin{align*}
  \frac{\partial E_x}{\partial z} &= -i \omega B_y \\
  -i k E_x &= - i \omega \mu \mu_0 H_y
\end{align*}

---

# Field Impedance (cont.)

The magnitudes of the electric and magnetic fields of an electromagnetic wave are thus not independent.
They are always perpendicular to each other and to the propagation direction.
Using the speed of light (dispersion relation in vacuum)
$$
c = \frac{\omega}{k} = \sqrt{\frac{1}{\mu \mu_0\, \varepsilon \varepsilon_0}}
$$
we can calculate the **field impedance** $Z$:
$$
Z = \frac{E}{H} = \frac{E_x}{H_y} = \mu \mu_0 \frac{\omega}{k} = \sqrt{\frac{\mu \mu_0}{\varepsilon \varepsilon_0}}
$$
The vacuum impedance $Z_0$ is a useful universal constant:
$$
Z_0 = \sqrt{\frac{\mu_0}{\varepsilon_0}} = 377\ \Omega
$$

---

# Refractive Index

Using the speed of light in vacuum
$$
c_0 = \sqrt{\frac{1}{\mu_0 \varepsilon_0}}
$$
we calculate the refractive index $n$, which is defined as the relative speed of light in a medium:
$$
n = \frac{c}{c_0} = \sqrt{\mu \varepsilon}
$$
For non-magnetic media ($\mu=1$) this simplifies to $n=\sqrt{\varepsilon}$ and the field impedance to $Z = Z_0/n$.
