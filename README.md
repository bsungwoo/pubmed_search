## Parallelized search in PubMed with beautifulsoup
The suggested python code accepts the keywords provided as one column in .xlsx or .csv file, searches for every keyword in PubMed, and summarizes the results in both English and Korean.

### Installation of conda environment
```{Plain Text}
conda env create -f environment.yml
```

### Dependencies
Refer to environment.yml
```{Plain Text}
pandas 1.4.3  
openpyxl 3.0.10  
requests 2.28.1  
beautifulsoup4 4.11.1  
parmap 1.6.0  
tqdm 4.64.1  
googletrans 3.1.0a0  
```
### Usage
#### Input variables  
indir: the directory for the .xlsx for .csv file (default: '.'; the same directory to web_crawl_pubmed.py file)  
outdir: the directory to save the output file (default: './output')  
```{Plain Text}
python web_crawl_pubmed.py --indir '.' --outdir './output'
```
