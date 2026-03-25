# Heuristic-Driven p-Center Optimal Facility Locator

A geospatial optimization engine built in **Python** using the **PuLP** library to solve the **Minimax (p-center)** distance problem. This tool features a high-fidelity data pipeline for normalizing **Statistics Canada** datasets with population weighting and integrates **OpenStreetMap** primitives to translate mathematical models into actionable site-selection visualizations.

## Core Features
* **Geospatial Intelligence:** Uses `OSMnx` to ingest real-world road network data.
* **Demographic Weighting:** Processes StatCan Census data to ensure facility placement is optimized for actual population density.
* **Mathematical Optimization:** Formulates a Mixed-Integer Linear Programming (MILP) problem to minimize the maximum travel distance for any user.
* **Automated Visualization:** Generates high-resolution mapping of optimal coordinates against the urban road graph.

---

## Setup and Data Acquisition

Before running the solver, you must manually acquire the demographic datasets from Statistics Canada.

### 1. Download Census Profile Data
Create a directory named `PopulationData` in the project root. Download the "Canada, provinces, territories, census divisions (CDs), census subdivisions (CSDs) and dissemination areas (DAs)" dataset and place the CSV inside:
* **Download Page:** [StatCan Census Profiles](https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/details/download-telecharger.cfm?Lang=E)
* **Direct Download:** [CSV File Link](https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/details/download-telecharger/comp/GetFile.cfm?Lang=E&FILETYPE=CSV&GEONO=006)

### 2. Download Boundary Shapefiles
Create a directory named `data/DAdata` in the project root. Download the Dissemination Area boundary files and place the unzipped contents inside:
* **Download Page:** [StatCan Boundary Files](https://www12.statcan.gc.ca/census-recensement/alternative_alternatif.cfm?l=eng&dispext=zip&teng=lda_000b21a_e.zip&k=%20%20%20192424&loc=//www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/files-fichiers/lda_000b21a_e.zip)
* **Direct Download:** [ZIP File Link](https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/files-fichiers/lda_000b21a_e.zip)

---

## Installation & Execution

Follow these steps to initialize the environment and execute the optimization model.

```bash
# Step 1: Create the virtual environment
python3 -m venv venv

# Step 2: Activate the environment
source venv/bin/activate

# Step 3: Install necessary packages from the requirements file
pip install -r requirements.txt

# Step 4: Run the p-center optimization project
python run.py