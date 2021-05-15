# Codecademy Data Science Path: Final Portfolio Project - Run to the Hills
This work is the final portfolio project for *Codecademy Data Scientist path*.

### Files and Folders

The repository includes the following files:
- **apple_health_export.zip:** *zip archive containing an `export.xml` from my Health Kit. It does not contain all the files that are available in a normal Health Kit export, just the one I have used.*
- **healthkit.py:** *Python module with classes and functions for importing data from `export.xml`.*
- **Import Apple Health.ipynb:** *Jupyter Notebook with tools for converting `export.xml` to Python objects. `HKdata.pickle` is created by this workbook, you can use it to create a pickle file with your data (see below for instructions).*
- **Final Portfolio Project.ipynb:** *Jupyter Notebook with final portfolio project, it contains analysis, models and conclusions. Health Kit data used here are loaded from `HKdata.pickle`.*
- **CC-DSpathFP39.yml:** *Conda environment for this final project.*
- **img**: folders with images used in notebooks.

### Install Conda

[<img style="position: relative; bottom: 3px;" src="https://docs.conda.io/en/latest/_images/conda_logo.svg" alt="Conda" width="80"/>](https://docs.conda.io/en/latest/) is required for creating the development environment (it is suggested to install [Miniconda](https://docs.conda.io/en/latest/miniconda.html)).

From terminal navigate to the repository base directory.\
Use the following command in your terminal to create an environment named `CC-DSpathFP39`.
```
conda env create -f CC-DSpathFP39.yml
```

### Dataset

`HKdata.zip` contains a pickle file that is used by `Final Portfolio Project.ipynb`.\
`HKdata.pickle` is larger than *100 MB* when unzipped.
Also the folder that contains `export.xml` is larger than *100 MB* so you will find `apple_health_export.zip` instead.\
Files over this threshold are not accepted in normal pushes to
[<img style="position: relative; bottom: 2px;" src=https://upload.wikimedia.org/wikipedia/commons/thumb/5/54/GitHub_Logo.png/800px-GitHub_Logo.png alt="GitHub" width="60"/>](https://docs.github.com/en/github/managing-large-files/conditions-for-large-files) (for this reason the unzipped file and folder are listed in this repo's *.gitignore*).\
**Remember to unzip `HKdata.zip` before running the `Final Portfolio Project.ipynb` notebook.**\
**Remember also to unzip `apple_health_export.zip` if you want to run the `Import Apple Health.ipynb` notebook.**

### Use Your Own Health Kit Records
Follows the instructions on [Apple's support](https://support.apple.com/guide/iphone/share-health-and-fitness-data-iph27f6325b2/ios) to export a *.zip* file with your data from *Health Kit*.\
Unzip that folder and copy it inside this project root folder. Then check that the `xml_file_path`variable in `Import Apple Health.ipynb` is set to the right path.\
You can now run `Import Apple Health.ipynb` to update `HKdata.pickle` with your data. There is a simple widget in `Import Apple Health.ipynb` to explore them.

You are set to go!

If you run `Final Portfolio Project.ipynb` you should see your data instead of mine.

### Run Jupyter Notebooks
From terminal navigate to the repository base directory.\
Use the following command to activate the environment `CC-DSpathFP39`.
```
conda activate CC-DSpathFP39
```
Then open jupyter and select a notebook.
```
jupyter notebook
```
