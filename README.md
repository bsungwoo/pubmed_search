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
indir: the directory for .xlsx, .xls or .csv files (default: '.'; the same directory to web_crawl_pubmed.py file)  
--> All .xlsx/.xls/.csv files in the directories will be analysed one by one.  
outdir: the directory to save the output file (default: './output')  
outname: the output file name (default: 'final_output')  
abstract_filter: select the articles that contain the given words (default: "")  
```{Plain Text}
Example 1 (without filter and default name)
python web_crawl_pubmed.py --indir '.' --outdir './output'

Example 2 (apply filter to select articles with the word 'FDG' and change output file name starting with 'change_name')
python web_crawl_pubmed.py --indir '.' --outdir './output' --outname 'change_name' --abstract_filter 'FDG'

Example 3 (enter inputs separately into command)
python web_crawl_pubmed_input.py
```
#### exe file for PubMed search
Please download file: [web_crawl_pubmed.exe](https://github.com/bsungwoo/pubmed_search/releases/download/v1.0.0/web_crawl_pubmed.exe)  
