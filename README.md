# influenza_filament_analysis
Scripts designed to take confocal images of filamentous virions and analyse them in useful ways.
BatchFilamentAnalysis will analyse 8-bit single-channel images in FIJI and generate a csv file with the lengths of all filamentous particles for each csv. It assumes nothing will interrupt opening the czi files = i.e. BioFormats is importing in the windowless format.
The analysis scripts require a csv file for each experiment with a column of lengths for each condition, so the csvs for each czi have to be combined. CSVcombiner can be used to combine every csv file in a folder, or it can be done manually. Example csv files show what the formatting should be.
FilamentAnalysisPlots will take the csvs it is given and produce violin plots or bar plots. Currently it will stall on single files, so requires multiple experiments for now (or the same experiment multiple times). It also can make plots with raw data entered into the script and make histograms for validation experiments.
Full details will be available on bioRxiv very shortly.
