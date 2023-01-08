import os
import argparse
import requests
import pandas as pd
from bs4 import BeautifulSoup

import parmap
from googletrans import Translator


def summarize_pubmed(result, query, dest_lang='ko'):
    translator = Translator()
    # Extract the title, authors, purpose, and results
    authors = result.select_one('meta[name="citation_authors"]')['content']
    author = authors.split(' ')[0]+' et al.'
    title = result.select_one('meta[name="citation_title"]')['content']
    journal_name = result.select_one('meta[name="citation_publisher"]')['content']
    article_info = result.find("span", class_="cit").text.split(';')
    article_info = article_info[0].split(' ')[0]+';'+article_info[-1].split('.')[0]
    try: article_type = result.find("div", class_='publication-type').text
    except: article_type = "Original"
    pubmed_url = result.select_one('meta[name="citation_abstract_html_url"]')['content']
    abstract_eng = result.find("div", class_='abstract-content selected')

    if abstract_eng is None: abstract_eng, abstract_purp = "", ""
    elif abstract_eng.find("strong", "sub-title") is None:
        abstract_eng = abstract_eng.text.strip().replace('\n', '')
        abstract_purp = [i for i in abstract_eng.split('.') if 'object' in i.lower() or 'objective' in i.lower() or 'aim' in i.lower() or 'purpose' in i.lower()]
        if len(abstract_purp)>0: abstract_purp = abstract_purp[0]
        else: abstract_purp = ""
    else:
        abstract_purp_list = abstract_eng.find_all("p")
        abstract_purp = ""
        for i in abstract_purp_list:
            txt_ck = i.text.lower()
            if 'object' in txt_ck or 'objective' in txt_ck or 'aim' in txt_ck or 'purpose' in txt_ck:
                abstract_purp = i.text.strip().replace('\n', '')
                break
        if abstract_purp=="": abstract_purp = abstract_purp_list[0].text.strip().replace('\n', '')
        abstract_eng = abstract_eng.text.strip().replace('\n', '')        

    abstract_ko = translator.translate(abstract_eng, dest=dest_lang).text
    abstract_purp_ko = translator.translate(abstract_purp, dest=dest_lang).text

    # Append the data to the list
    df = pd.DataFrame([query, authors, author, title, journal_name, article_info, article_type,
                       abstract_purp_ko, abstract_ko, abstract_eng, pubmed_url]).T
    df.columns = ["검색어","저자전체","저자","제목","게재지","서지","유형","연구목적","초록","초록(영문)","URL"]
    return df

def search_pubmed(query):
    # Submit the search form
    response = requests.get("https://pubmed.ncbi.nlm.nih.gov/", {'term':query})
    # Parse the HTML content of the search results page
    result = BeautifulSoup(response.content, "lxml")
    
    if result.select_one('meta[name="citation_authors"]') is not None:        
        df = summarize_pubmed(result, query)
    else:
        try:
            # If error occurs then, move to the first search result
            href = result.find("a", class_="docsum-title")['href']
            response = requests.get('https://pubmed.ncbi.nlm.nih.gov'+href)
            result = BeautifulSoup(response.content, "lxml")
            df = summaraze_pubmed(result, query)
        except: 
            column_names = ["검색어","저자전체","저자","제목","게재지","서지","유형","연구목적","초록","초록(영문)","URL"]  
            df = pd.DataFrame([query]+[""]*(len(column_names)-1)).T
            df.columns = column_names
    return df

def search_pubmed_parallel(querys):
    df = parmap.map(search_pubmed, querys, pm_pbar=True, pm_processes=os.cpu_count())
    df_final = pd.concat(df, axis=0)
    return df_final


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--indir', type=str, default='.')
    parser.add_argument('--outdir', type=str, default='./output')
    parser.add_argument('--outname', type=str, default='final_result')
    parser.add_argument('--abstract_filter', type=str, default='')
    args = parser.parse_args()
    print(f"The provided inputs are {args.indir}, {args.outdir}, {args.outname}, and {args.abstract_filter}")
        
    # Read csv or xlxs file
    read_file_list = [i for i in os.listdir(args.indir) if (i.endswith('.csv') or i.endswith('.xls') or i.endswith('.xlsx'))]
    # Check if there is appropriate file for analysis
    if len(read_file_list)==0: raise ValueError(".csv, .xls, or .xlsx not found in the given directory")
    for read_file in read_file_list:
        print("Analyzing the csv/xls/xlsx file: "+read_file)
        # Read file
        if read_file.endswith(".xlsx"): df_input = pd.read_excel(os.path.join(args.indir,read_file), header=None)
        else: df_input = pd.read_csv(os.path.join(args.indir,read_file), header=None)

        # Parallel search in the pubmed
        df = search_pubmed_parallel(df_input[0].values)
        df.drop_duplicates('검색어', keep='first', inplace=True)
        # Filter the results
        if args.abstract_filter!="": df = df[df['초록(영문)'].str.contains(args.abstract_filter)]
        # Save the results
        if not os.path.exists(args.outdir): os.makedirs(args.outdir)
        df.to_csv(os.path.join(args.outdir, args.outname+'_'+'.'.join(read_file.split('.')[:-1])+'.csv'), index=False, encoding='utf-8-sig')
    print("End of searching PubMed and extracting information")