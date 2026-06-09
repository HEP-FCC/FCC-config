# ILD@FCC-ee

_ILD remains an open and evolving concept -> join us and help shape its future!_

## Getting Started: Simulation and Reconstruction

To begin working with the ILD software, follow the [ILD Simulation and Reconstruction Tutorial](https://key4hep.github.io/key4hep-doc/main/tutorials/key4hep-tutorials/gaudi_ild_reco/README.html).

> **Important:** While the default model `ILD_l5_o1_v02` is designed for the _International Linear Collider (ILC)_, dedicated models for _FCC-ee_ are available and must be **actively selected** in your steering script or the command line:
>
> - `--detectorModel ILD_FCCee_v01`
> - `--detectorModel ILD_FCCee_v02`

## Geometry and Detector Models

The geometry descriptions for ILD@FCC-ee are hosted within the **k4geo** repository. You can find the compact XML descriptions and model details here:

- [ILD@FCC-ee Geometries](https://github.com/key4hep/k4geo/tree/main/FCCee/ILD_FCCee/compact)

## Steering and Configuration

Configurations are maintained in the ILDConfig repository:

- [ILD Configurations](https://github.com/iLCSoft/ILDConfig/tree/master/StandardConfig/production)

> **Important:** The previous reconstruction framework based on `Marlin` does not support the ILD@FCC-ee models.

## Join the Community

The ILD Concept Group is an active collaboration. We encourage new contributors to attend our meetings and participate in technical discussions:

- **Meetings:** Keep track of upcoming General Meetings on the [ILD Indico](https://agenda.linearcollider.org/category/243/).
