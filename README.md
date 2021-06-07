For this project, Miguel Morales and I (Jennifer Li) were interested in what factors effect the price of a home on the housing website Zillow.com. We looked at each property currently listed for sale on Zillow.com in the San Francisco, CA as of June 2021, and also looked at properties in San Francisco, CA that have sold within the last month (May 2021-June 2021) because we were interested in the range of San Francisco's notoriously high housing prices. We looked the following factors, such as it's location, listing company/agent, amount of bedrooms/bathrooms, building type (condo, apartment, home, newly constructed, etc.), total square footage, and price per sq. ft., to see if there was a trend of one or more factors increasing or decreasing the price that the property was listed for.

**Located in the /code/ folder (The .ipynb versions of each file is included in this folder as well to reproduce data.):**

* Zillow-Scraper-Sold.py: This file was used to collect data from Zillow.com by scraping and parsing through each webpage for San Francisco, CA properties listed as sold in the past month (May 2021-June 2021) and converting them to a .csv file to make the data more easily accessible throughout this project.
* * Zillow-Scraper.py: This file was used to collect data from Zillow.com by scraping and parsing through each webpage for San Francisco, CA properties currently listed for sale and converting them to a .csv file to make the data more easily accessible throughout this project.
  * The data was collected by running this file and loading each page from 20 pages for each of the following URLS:
    * www.zillow.com/san-francisco-ca/sold/
    * www.zillow.com/san-francisco-ca/sale/

* For-Sale_Analysis.py: This file includes the code used for our final written report.
* Sold_Analysis.py: This file includes the code used for our final written report.

**Located in the /data/ folder:**

* sold.csv: This file includes homes that have sold on Zillow.com in the past month (May 2021-June 2021), their address including zip code, the company that listed the property on Zillow.com, the price the property sold for, the amount of bedrooms and bathrooms the property has, the square footage of the property (sq. ft.), and the price per sq. ft.

* for_sale.csv: This file includes homes that are currently listed on Zillow.com for sale, and includes their address including zip code, listing agent and their company, price per month, amount of bedrooms and bathrooms, the square footage of the property, the building type (condo, apartment, home), and the price per sq. ft.

**Located in the /notebooks/ folder:**

* Zillow_SF.ipynb: This file includes our final written report with its accompanying code and output.
