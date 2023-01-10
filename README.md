## Parallelized search in PubMed with beautifulsoup
The suggested python code accepts the keywords provided as one column in .xlsx, .xls, or .csv file, searches for every keyword in PubMed, and summarizes the results in both English and Korean.  

### 1. Installation
#### 1-1. Using executable file
Please download file: [web_crawl_pubmed.exe](https://github.com/bsungwoo/pubmed_search/releases/download/v1.0.0/web_crawl_pubmed.exe)  
#### 1-2. Using python code (conda environment) 
```{Plain Text}
conda env create -f environment.yml
```

### 2. Dependencies
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

### 3. Usage
#### 3-1. Using exe file for PubMed search
The command window appears when clicking the exe file.  
The below images (1-2) are examples for inputs (same as above python code usage) and execution results for the exe file. 
1) Input as one column in csv/xls/xlsx file (any keywords for search can be put in each row).  
![image](https://user-images.githubusercontent.com/61150422/211229602-8d68ccb6-4b9d-4eaf-b8f9-37cd7cf150ea.png)
2) Provide inputs for input and output directories, prefix of the output file name, and a keyword to filter the abstract with.  
(not necessary to provide inputs for outname and abstract_filter)  
![image](https://user-images.githubusercontent.com/61150422/211228253-459dfae7-7ada-4b50-b8ea-64065b0eee09.png)  
3) The below image is the output example.  
![image](https://user-images.githubusercontent.com/61150422/211229344-21a26639-626a-4150-b5cf-a890296e0d51.png)
#### 3-2. Using Python code for PubMed search  
indir: the directory for .xlsx, .xls or .csv files that contains keyword in one column (default: '.'; the same directory to web_crawl_pubmed.py file)  
--> Any keyword can be possible including full reference list.  
--> All .xlsx/.xls/.csv files in the directories will be analysed one by one.  
outdir: the directory to save the output file (default: './output')  
outname: the prefix of the output file name (default: 'final_output')  
abstract_filter: select the articles that contain the given words (default: "")  
```{Plain Text}
Example 1 (without filter and default name)
python web_crawl_pubmed.py --indir '.' --outdir './output'

Example 2 (apply filter to select articles with the word 'FDG' and change output file name starting with 'change_name')
python web_crawl_pubmed.py --indir '.' --outdir './output' --outname 'change_name' --abstract_filter 'FDG'

Example 3 (enter inputs separately into command)
python web_crawl_pubmed_input.py
```
