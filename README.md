# Web of Science Extractor

**WoS Extractor**: extract data about a query in the Web of Science. 

WoS Extractor minimizes the time spent in the academic research process for the construction of a theoretical framework.

## How to install
```bash
pip install -r requirements.txt
```
## How Download Chrome Driver
Chrome Driver: [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads)

## How to run
The Jupyter Notebook `wos_extractor.ipynb` contains a vignette with an example.

```python
from WoSExtractor import *

# You'll need to insert the path to a browser driver from Selenium
wos = WoSExtractor(path_to_Selenium_driver)

# It returns a dataframe from a Web of Science search query 
df_article = wos.search(search_term)
```

## Authors

* [Edson Souza - Universidade Nove de Julho](https://orcid.org/0000-0002-5891-4767)
* [Jose Storopoli - Universidade Nove de Julho](https://orcid.org/0000-0002-0559-5176)
* [Wonder Alves - Universidade Nove de Julho](https://orcid.org/0000-0003-0430-950X)

