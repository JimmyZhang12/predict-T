# predict-T

This project is an extension of the The Gem5 Simulator for studying the
interactions between microprocessor and power supply and power delivery
network. This novel framework combines two academic state of the art
simulators with a realisic Verilog AMS model of the power supply, motherboard,
and on chip power delivery networks.



### Structure

The repository contains the following directories:

- *circuit\_model* - Verilog AMS code and Scripts to run the Cadence
VerilogAMS circuit simulation.
- *git_util* - Git hooks and other scripts for managing the repository
- *python* - Python utilities 
  - *mcpat_autogen* - Python code for converting the Gem5 stats to McPAT XML
  - *analysis* - Python utilities for plotting and generating test data
- *runscript* - Folder containing setup scripts and run scripts



### Dependencies

#### Cadence Aug2016
This project is dependent on Cadence AUG2016 and requires a license to enable
the circuit level simulation (NCVerilog/Spectre). Other open source tools at
the moment are not supported however there are plans to eventually replace
this requirement with a free tool.

The Cadence tools can be obtained locally with the following commands:

First sign in to UIUC EWS and load the Cadence AUG2016 module:

`module load cadence/Aug2016`

Second transfer the cadence tools to the local machine with rsync:

`rsync -rvlR /software/cadence-Aug2016
<user>@<remote.machine.url>:/home/<user>/cadence`

Depending on network speed this may take a couple of hours and will use
approximately 70GB of drive space.

#### Architecture Simulators

The project also requires building forked Gem5 and McPAT repositories:
- [McPAT Fork](https://github.com/atsmith3/mcpat)
- [GEM5 Fork](https://github.com/atsmith3/gem5)



### Build & Run

To build and run the project set the paths in `setup.sh`

To build the docker container required by Cadence AUG2016, and set the
environment variables:

`source runscript/setup.sh`

Adjust the paths in `run.sh` to point to the test executables and the input
files, and run the the tests:

`runscript/run.sh`



### Versioning and Features

Version 0.0.0 - Currently not released as an official tool. Needs open source
circuit sim tool support first.



### Future Work

Please see the open issues for the improvements to the project.



### Authors

* **Andrew Smith** - *Base classes, system class, serialization* - [atsmith3](https://github.com/atsmith3)

See also the list of [contributors](https://github.com/atsmith3/predict-T/graphs/contributors) who participated in this project.



### License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
