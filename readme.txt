# Step 1: Create the virtual environment
python3 -m venv venv

# Step 2: Activate the environment
source venv/bin/activate

# Step 3: Install necessary packages from the requirements file
pip install -r requirements.txt

# Step 4: Run the p-center optimization project
python run.py

# step 5: download both stats 

#a)download "Canada, provinces, territories, census divisions (CDs), census subdivisions (CSDs) and dissemination areas (DAs)"
#put into DAdata

https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/details/download-telecharger.cfm?Lang=E
or 
https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/details/download-telecharger/comp/GetFile.cfm?Lang=E&FILETYPE=CSV&GEONO=006

#b) put into PopulationData
https://www12.statcan.gc.ca/census-recensement/alternative_alternatif.cfm?l=eng&dispext=zip&teng=lda_000b21a_e.zip&k=%20%20%20192424&loc=//www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/files-fichiers/lda_000b21a_e.zip
or
https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/files-fichiers/lda_000b21a_e.zip
