import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
response=requests.get('https://www.imdb.com/chart/top/?ref_=nv_mv_250', headers=headers)
text = response.text
soup = BeautifulSoup(text, 'html.parser')
movie_heads= soup.find_all('h3', attrs={'class': 'ipc-title__text'})
year=soup.find_all('span', attrs={'class': 'sc-be6f1408-8 fcCUPU cli-title-metadata-item'})
df1=[]
df2=[]
for index, movie_head in enumerate(movie_heads, start=0):
        if index > 250:
            break
        name=movie_head.text.strip().replace("IMDb Charts","")
        if name:  # Check if name is not empty
            df1.append({'Movie': name})
for info in year:
        year_match = re.search(r'\d{4}', info.text)
        if year_match:
            year=year_match.group()
            df2.append({'Year': year})
combined_df = pd.concat([pd.DataFrame(df1), pd.DataFrame(df2)], axis=1)      
# combined_df = combined_df[combined_df['Movie'] != '']  # Remove rows with empty 'Movie' column
combined_df.to_excel('movie_list.xlsx', index=False)
