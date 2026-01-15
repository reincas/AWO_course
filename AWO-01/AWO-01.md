---
title: "Applied Wave Optics: Maxwell Equations"
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
  \titlegraphic{
    \vspace{4ex}
	\includegraphics[width=2cm]{by-sa.pdf}\\[1ex]
    \footnotesize
    Except where otherwise noted, this document and its content are licensed under the\\
    \href{https://creativecommons.org/licenses/by-sa/4.0/legalcode.en}{Creative Commons Attribution-ShareAlike 4.0 International license}.
  }
  \makeatletter
  \renewcommand{\@makecaption}[2]{}
  \makeatother
  ```
aspectratio: 169
---

# Maxwell's equations

The most general differential form of Maxwell's equations is
\begin{alignat*}{2}
\boldsymbol{\nabla} \mathbf{D}        &= \rho                                          &\qquad& \text{Gauss's law} \\
\boldsymbol{\nabla} \mathbf{B}        &= 0                                             &\qquad& \text{Gauss's law for magnetism} \\
\boldsymbol{\nabla} \times \mathbf{E} &= -\partial \mathbf{B} / \partial t             &\qquad& \text{Faraday's law} \\
\boldsymbol{\nabla} \times \mathbf{H} &= \mathbf{j} + \partial \mathbf{D} / \partial t &\qquad& \text{Ampère-Maxwell law}
\end{alignat*}

with the electric field vector $\mathbf{E}\ [\mathrm{V/m}]$ and its material dependent form, the displacement field $\mathbf{D}\ [\mathrm{As/m^2}]$
as well as the magnetic field vector $\mathbf{H}\ [\mathrm{A/m}]$ and its material dependent form, the magnetic induction $\mathbf{B}\ [\mathrm{Vs/m^2}]$.
The scalar electrical charge density is $\rho\ [\mathrm{C/m^3}]$
and the local flux of electrical charges is taken into account by the current density vector $\mathbf{j}\ [\mathrm{A/m^2}]$.

---

# Polarisation

The material dependent relationship between $\mathbf{D}$ and $\mathbf{E}$ is
$$
\mathbf{D}(\mathbf{E}) = \varepsilon_0 \mathbf{E} + \mathbf{P}(\mathbf{E})
$$
with the permittivity $\varepsilon_0 = 8.854 \cdot 10^{-12}\ \mathrm{\frac{As}{Vm}}$ and the polarisation vector $\mathbf{P}$. Its Taylor expansion gives
$$
\mathbf{P}(\mathbf{E})|_{\mathbf{E}=0} = \mathbf{P}_0 + \varepsilon_0 \chi_e^{(1)}\mathbf{E} + \varepsilon_0 \chi_e^{(2)}\mathbf{E}^2 + \ldots
$$
where the first term is a **static** polarisation, characteristic for ferroelectric materials, the second term describes the **linear** behaviour and all following terms **non-linear** dependencies with the electric susceptibility tensors $\chi_\mathrm{e}^{(n)}$.

---

# Magnetisation

The material dependent relationship between $\mathbf{H}$ and $\mathbf{B}$ is
$$
\mathbf{B}(\mathbf{H}) = \mu_0 \mathbf{H} + \mu_0 \mathbf{M}(\mathbf{H})
$$
with the permeability $\mu_0 = 4\pi \cdot 10^{-7}\ \mathrm{\frac{Vs}{Am}}$ and the magnetisation vector $\mathbf{M}$. Its Taylor expansion gives
$$
\mathbf{M}(\mathbf{H})|_{\mathbf{H}=0} = \mathbf{M}_0 + \chi_m^{(1)} \mathbf{H} + \chi_m^{(2)} \mathbf{H}^2 + \ldots
$$
where the first term is a **static** magnetisation, characteristic for ferromagnetic materials, the second term describes the **linear** behaviour and all following terms **non-linear** dependencies with the magnetic susceptibility tensors $\chi_m^{(n)}$.

---

# Linear Case

For isotropic materials, all susceptibilities are scalars and the linear cases simplify to
\begin{align*}
\mathbf{D} &= \varepsilon \varepsilon_0 \mathbf{E} \\
\mathbf{B} &= \mu \mu_0 \mathbf{H}
\end{align*}
with the two dimensionless scalar quantities called **relative permittivity** $\varepsilon=1+\chi_\mathrm{e}^{(1)}$ and **relative permeability** $\mu=1+\chi_m^{(1)}$.

## Note

We always assume this case in the following.

---

# Continuity Equation

Identity relation from vector algebra for an arbitrary field $\mathbf{A}$:
$$
\boldsymbol{\nabla} (\boldsymbol{\nabla} \times \mathbf{A}) = 0
$$
It must therefore also be true for the magnetic field and wie can utilize Maxwell's equations:
\begin{align*}
\boldsymbol{\nabla} (\boldsymbol{\nabla} \times \mathbf{H})
&= \boldsymbol{\nabla} \left(\mathbf{j} + \frac{\partial \mathbf{D}}{\partial t} \right) \\
&= \boldsymbol{\nabla} \mathbf{j} +  \frac{\partial }{\partial t} \boldsymbol{\nabla} \mathbf{D} \\
&= \boldsymbol{\nabla} \mathbf{j} +  \frac{\partial \varrho}{\partial t} \overset{!}{=} 0 \\
\boldsymbol{\nabla} \mathbf{j} &= -\frac{\partial \varrho}{\partial t}
\end{align*}
This is the continuity equation for electrical charges in its differential (local) form.

---

# Continuity Equation (cont.)

The meaning of the continuity equation becomes more obvious, when it is integrated:
$$
\int_{\partial V} \mathbf{j}\, d\mathbf{A} = -\frac{dQ}{dt}
$$

The left hand side is the total electrical current through the surface of a volume $V$ and the right hand side the temporal variation of the total electrical charge $Q = \int\! \rho\, dV$ inside this volume.

![caption text](img_continuity.svg){width=566px}

Maxwell's equations guarantee that both quantities are identical.

---

# Parallel Fields at Interfaces

Interface between two different materials:

![caption text](img_StokesInterface.svg){width=1580px}

Differentials for a line integration along the path $\partial A$:
\begin{alignat*}{2}
  1 \to 2 &: \quad d\mathbf{r} = -\hat{\mathbf{n}} \times \hat{\mathbf{e}} \ dx \\
  2 \to 3 &: \quad d\mathbf{r} =  \hat{\mathbf{e}} \ dx \\
  3 \to 4 &: \quad d\mathbf{r} = \hat{\mathbf{n}} \times \hat{\mathbf{e}} \ dx \\
  4 \to 1 &: \quad d\mathbf{r} =  -\hat{\mathbf{e}} \ dx
\end{alignat*}

---

# Parallel Fields at Interfaces (cont.)

Stokes theorem from vector analysis:
$$
\int\limits_A (\boldsymbol{\nabla} \times \mathbf{E}) d\mathbf{A}
= \oint\limits_{\partial A} \mathbf{E}\ d\mathbf{r}
$$
We shrink the area $A\to0$, and use the fact that for $\Delta\ell\to0$ the line integrals $2\to3$ and $4\to1$ are identical, but with opposite sign:
$$
\lim_{A \to 0}\int\limits_A (\boldsymbol{\nabla} \times \mathbf{E}) d\mathbf{A} 
= \lim_{\Delta h, \Delta\ell \to 0}
\left[- \int\limits_1^2 (\hat{\mathbf{n}} \times \hat{\mathbf{e}}) \mathbf{E}_1\ dx
+ \int\limits_3^4 (\hat{\mathbf{n}} \times \hat{\mathbf{e}}) \mathbf{E}_2\ dx \right]
$$
Now we insert Faraday's law on the left and on the right the scalar triple products extract the field components parallel to the interface:
$$
-i\omega \lim_{A \to 0} \int\limits_A \mathbf{B}\ d\mathbf{A}
= \lim_{\Delta h, \Delta\ell \to 0}
\left[-\int\limits_1^2\! E_{1\parallel}\ dx
+ \int\limits_3^4\! E_{2\parallel}\ dx \right]
$$

---

# Parallel Fields at Interfaces (cont.)

The left side is obviously zero and on the right side we use the fact that for $\Delta\ell\to0$ the fields can be treated as constant:
$$
0 = (E_{1\parallel} - E_{2\parallel})\ \Delta\ell
$$

We get the same result when we carry out this calculation for the magnetic field and thus end with the following boundary conditions for field components parallel to the interface plane:
\begin{align*}
  E_{1\parallel} &= E_{2\parallel} \\
  H_{1\parallel} &= H_{2\parallel}
\end{align*}

---

# Normal Fields at Interfaces

Interface between two different materials:

![caption text](img_GaussInterface.svg){width=1580px}

Differentials for an integration over the surface $\partial V$:
\begin{alignat*}{2}
  \text{top base} &: \quad d\mathbf{A} = \hat{\mathbf{e}}\ dA \\
  \text{lateral} &: \quad d\mathbf{A} = \hat{\mathbf{n}}\ dA \\
  \text{bottom base} &: \quad d\mathbf{A} = -\hat{\mathbf{e}}\ dA
\end{alignat*}

---

# Normal Fields at Interfaces (cont.)

Gauss's theorem from vector analysis:
$$
\int \limits_{V} \boldsymbol{\nabla}\mathbf{D}\ dV = \oint \limits_{\partial V} \mathbf{D}\ d\mathbf{A}
$$
We shrink the volume $V\to0$, and use the fact that in this case the lateral surface integrals in both materials vanish, because the field is constant:
$$
\lim_{V \to 0} \int\limits_{V} \boldsymbol{\nabla}\mathbf{D}\ dV
= \lim_{\Delta A, \Delta h \to 0}
\left[\int\limits_{\Delta A_1}\!\mathbf{D}_1\hat{\mathbf{e}}\ dA
  - \int\limits_{\Delta A_2}\!\mathbf{D}_2\hat{\mathbf{e}}\ dA \right]
$$
Now we insert Gauss's law on the left and on the right the scalar products extract the component of the displacement field perpendicular to the interface:
$$
\lim_{V \to 0} \int\limits_V\!\varrho\ dV
= \lim_{\Delta A, \Delta h \to 0}
\left[\int\limits_{\Delta A\vphantom{A_1}}\!D_{1\perp} dA - \int\limits_{\Delta A}\!D_{2\perp} dA \right]
$$

---

# Normal Fields at Interfaces (cont.)

The left side is obviously zero and on the right side we use the fact that for $\Delta A\to0$ the fields can be treated as constant:
$$
0 = (D_{1\perp} - D_{2\perp})\ \Delta A
$$

We get the same result when we carry out this calculation for the magnetic induction and thus end with the following boundary conditions for field components perpendicular to the interface plane:
\begin{alignat*}{2}
  D_{1\perp} &= D_{2\perp} & \qquad \varepsilon_1 E_{1\perp} &= \varepsilon_2 E_{2\perp} \\
  B_{1\perp} &= B_{2\perp} & \qquad \mu_1 H_{1\perp} &= \mu_2 H_{2\perp}
\end{alignat*}

