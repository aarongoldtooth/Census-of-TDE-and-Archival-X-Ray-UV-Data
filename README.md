# Census of TDE and Archival X-Ray/UV Data
Repository for research documents used in "A Census of Archival X-ray Spectra for Modeling Tidal Disruption Events"

The documentation here is used to create a catalog of known Tidal Disruption Events (TDEs) as well as figures used to decribe the dataset therein.

---
## Contents:

1. TDE input files
   - TDE_List.tsv
      - contains TDE name, TDE host name, and TDE discovery date information.
   - TDE Observations folder
      - contains individual TDE subfolders each with instances (if available) of XMM-Netwon, Chandra, and Swift observational information.
   - TDE_Output_Data.tsv
      - contains observational data extracted from the TDE Observations folders.
   - priority_tde_indicies.txt
      - contains the indecies for priority TDE candidates.
   - Full New TDE Catalog (Published)
      - .tsv version of our full new TDE catalog.
   
  
3. TDE code files (Available in .ipynb and .py formats)
   - TDE Catalog.ipynb/TDECatalogMaker.py
      - input: TDE_List.tsv, TDE Observations folder
      - returns: TDE_Output_Data.csv
   - Priority TDE Filter.ipynb/PriorityTDEFilter.py
      - input: TDE_List.tsv, TDE_Output_Data.csv
      - returns: priority_tde_indicies.txt
   - TDE Timelines.ipynb/TDETimelineMaker.py
      - input: TDE Observations folder
      - output: TDE_Timeline_Plots.pdf
   - TDE Exposure Time Redshift Plots.ipynb/TDERedshiftExpTimePlotter.py
      - input: TDE_Output_Data.csv, priority_tde_indicies.txt
      - output: tde_exp_times_vs_redshift.pdf
  
3. TDE code output files
   - TDE_Output_Data.csv
   - priority_tde_indicies.txt
   - TDE Timeline Plots.pdf
   - tde_exp_times_vs_redshift.pdf
   
4. Full New TDE Catalog (Published).xl
    -  Excel version of our full new TDE catalog. Also contains information on the priority TDEs in a seperate tab.

---
## Running Code

### Dependencies
Python version 3.9.12

Third Party modules can be found in 'requirements.txt'

### Installation/Running

In order to save time and effort on the part of the user, there is Jupyter Notebook called TDE_main.ipynb that will run each of the four TDE .py files in the proper order and create the necessary output files. Therefore, TDE_main.ipynb is the only file that is needed to preproduce the research documents used in our paper "A Census of Archival X-ray Spectra for Modeling Tidal Disruption Events".

However, if you would like to run certain code files independently, the instructions for file handling and requirements are listed below:

In order to run the .ipynp/.py files, first ensure that the TDE input files (see 1. above) are available in the same folder as the .ipynp/.py files.

To ensure proper file handling and processing due to prior output file dependencies, the following .ipynp/.py files below should be run in the following order:

1. TDE Catalog.ipynb/TDECatalogMaker.py
   - input: TDE_List.tsv, TDE Observations folder
   - returns: TDE Output Data.csv
2. Priority TDE Filter.ipynb/PriorityTDEFilter.py
   - input: TDE_List.tsv, TDE_Output_Data.csv
   - returns: priority_tde_indicies.txt
3. TDE Exposure Time Redshift Plots.ipynb/TDERedshiftExpTimePlotter.py
   - input: Full New TDE Catalog (published).tsv, priority_tde_indicies.txt
   - output: tde_exp_times_vs_redshift.pdf

Note: TDE Timelines.ipynb/TDETimelineMaker.py is not dependent on other .ipynp/.py output files/information and can be safely run independently of the above files.

---
## Contributing

Issue Tracker: https://github.com/aarongoldtooth/Census-of-TDE-and-Archival-X-Ray-UV-Data/issues

---
## License

MIT License: https://github.com/aarongoldtooth/Census-of-TDE-and-Archival-X-Ray-UV-Data/blob/main/LICENSE

---
## Citation
Repository DOI:

Paper DOI:

---
## Contact
Aaron Goldtooth [orcid](https://orcid.org/0000-0001-9695-4121)
   - email: gold1992(at_sign)arizona.edu
