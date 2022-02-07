=============================================
Pyrouet is for PYthon RObUst Embedded Testing
=============================================

:Authors:  - Florian Dupeyron <florian.dupeyron@mugcat.fr>
           - François Beaulier <francois@hyvibe.audio>

*Pyrouet* enables easy design of benches for embedded software and hardware testing and
developpment. It may find usages in CI/CD processes as well as SMT factory tests for electronic products,
integrating more and more software complexity. *Pyrouet*'s early closed-source versions
have been used to test H1 products from HyVibe_, from the PCB flashing and testing after SMT assembly,
to the last functional validation tests, when integrated in a HyVibe Guitar.

.. _HyVibe: https://hyvibe.audio


**Important notice**: This tool is primarly designed to work with **linux based systems**.

Philosophy and status
=====================

.. Note that the below commentary should disappear when the software will be mature enough! :D

*Pyrouet* code is still quite fuzzy. The first milestones of this public version will be to refactor and standardize the code.
**Please do not consider this toolkit stable yet**, as important structural parts may change, leading to major
break and incompatbility issues between versions.

The philosophy used in the development of this software is:

- **Tools first**: This project aims to build a set of tools, instead of having a big chunk of a rock solid software
  architecture that hasn't any kind of flexibility, and cannot foresee all use cases. Each bit should be able to be integrated
  in your very own environment and solutions. This may lead sometimes to "glue code" to interface things together. Think of it
  as similar to *numpy*: it does all kind of stuff, but you may need only some part of it.

- **Minimal dependencies**: This project tries to depend only on mainstream, well maintened projects.

- **Reliability over features**: As this toolkit targets Factories to test PCBs, there is a need of reliability to ensure fast
  tests execution and good reporting. KISS and first principles thinking rules here.

- **Automation friendly**: The ultimate goal of this project is to build fully automatic test benches, that can easily be interfaced
  with some UI monitoring.

Getting started
===============

Please have a look at `the documentation`_.

.. _`the documentation`: docs/index
