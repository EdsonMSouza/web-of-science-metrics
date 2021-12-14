# Web of Science Extractor

**WoS Extractor**: extract data about a query in the Web of Science. 

WoS Extractor minimizes the time spent in the academic research process for the construction of a theoretical framework.

## How to install
```bash
pip install -r requirements.txt
```
## How Download Chrome Driver
This version is based in Windows 10 system. To others systems, access the link below.  
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


## How to cite this content

```
DE SOUZA, Edson Melo; STOROPOLI, Jose; ALVES, Wonder (2019, November 25). Web of Science Metrics.
Available in: https://github.com/EdsonMSouza/web_of_science_metrics
```

Or BibTeX for LaTeX:

```latex
@misc{desouza2019WOS,
  author = {DE SOUZA, Edson Melo and STOROPOLI, Jose and ALVES, Wonder},
  title = {Web of Science Metrics},
  url = {https://github.com/EdsonMSouza/web_of_science_metrics},
  year = {2019},
  month = {November}
}
```

## License

[![CC BY-SA 4.0][cc-by-sa-shield]][cc-by-sa]

This work is licensed under a
[Creative Commons Attribution-ShareAlike 4.0 International License][cc-by-sa].

[![CC BY-SA 4.0][cc-by-sa-image]][cc-by-sa]

[cc-by-sa]: http://creativecommons.org/licenses/by-sa/4.0/

[cc-by-sa-image]: https://licensebuttons.net/l/by-sa/4.0/88x31.png

[cc-by-sa-shield]: https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg
