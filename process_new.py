def process_new(car_id):
    
    # We then use bs4's BeautifulSoup() function to extract the raw html of the webpage. We also extract the title of the website as this will be useful in filtering out non-valid IDs.
    url = 'https://www.sgcarmart.com/used_cars/info.php?ID=' + car_id
    response = get(url)
    page_html = BeautifulSoup(response.text,'html.parser')
    page_title = page_html.find('title').text
    
    # Next we grab from the full html a section (div class) called main_left. This html section contains the key data that we will be scraping.
    try:
        main_left = page_html.find('div', attrs = {'id':'main_left'})
    except:
        None
    
    # Now an if statement is used to include only vehicles that are available for sale. 
    # The first page_title condition filters out non-valid IDs which when accessed, returns a webpage with the title of 'Buy Used Car & Used Vehicle & Used Cars Singapore - sgCarMart'.
    # The second condition searches for listings for which the vehicles are available. Sold vehicles and expired listings are excluded.

    if(page_title != 'Buy Used Car & Used Vehicle & Used Cars Singapore - sgCarMart' and
    str(main_left.find('strong', text = 'Availability').find_parent('tr').find_all('td')[1].text.replace('\n','')) == 'Available'):       
        
        # We then scrape the various fields of the listings
        # To clean up the formatting of numerical data, we either used a series of quick and dirty .replace() functions, or used regex for items that had more complex variations in formatting. 
        
        # 1. Availability - now set as 'Available' and may be updated to 'Sold' in the future by the subsequent update() function.
        avail = str(main_left.find('strong', text = 'Availability').find_parent('tr').find_all('td')[1].text.replace('\n',''))

        # 2. Make and Model - e.g. Toyota Vios
        make_model = page_html.find('a', class_ = 'link_redbanner').text

        # 3. Price
        try:
            price = int(main_left.find('strong', text = 'Price').find_parent('tr').find_all('strong')[1].text.replace('$','').replace(',',''))
        except:
            price = 0
            
        # 4. Annual Depreciation
        try:
            depre = int(main_left.find('strong', text = 'Depreciation').find_parent('tr').find_all('td')[1].text.replace('$','').replace(',','').replace(' /yrView models with similar depreciation',''))
        except:
            depre = 0

        # 5. Registration Date
        try:
            reg_date = main_left.find('strong', text = 'Reg Date').find_parent('tr').find_all('td')[1].text
            reg_date = re.findall(r"\d+.+\(", reg_date)[0].replace('(','')
            reg_date = datetime.strptime(reg_date,'%d-%b-%Y')
        except:
            reg_date = 0

        # 6. Year of Manufacture 
        try:
            manu_yr = int(main_left.find('strong', text = 'Manufactured').find_parent('tr').find_all('td')[1].text)
        except:
            manu_yr = 0
            
        # 7. Mileage (in kilometres)
        try:
            mileage = main_left.find('strong', text = 'Mileage').find_parent('tr').find_all('td')[1].text
            mileage = int(re.findall(r"\d+.\d+ k", mileage)[0].replace(' k','').replace(',',''))
        except:
            mileage = 0
            
        # 8. Transmission - Auto or Manual
        try:
            tranny = main_left.find('strong', text = 'Transmission').find_parent('tr').find_all('td')[1].text
        except:
            tranny = ''
            
        # 9. Engine Capacity (in cc)
        try:
            eng_cap = int(main_left.find('strong', text = 'Engine Cap').find_parent('tr').find_all('td')[1].text.replace(',','').replace(' cc',''))
        except:
            eng_cap = 0
            
        # 10. Road Tax / Year
        try:
            road_tax = int(main_left.find('strong', text = 'Road Tax').find_parent('tr').find_all('td')[1].text.replace(',','').replace('$','').replace(' /yr',''))
        except:
            road_tax = ''

        # 11. Power (in bhp)
        try:
            power = main_left.find('strong', text = 'Power').find_parent('tr').find_all('td')[1].text
            power = int(re.findall(r"\d+ bhp", power)[0].replace(' k','').replace(' bhp',''))
        except:
            power = ''

        # 12. Curb Weight (in kg)
        try:
            weight = int(main_left.find('strong', text = 'Curb Weight').find_parent('tr').find_all('td')[1].text.replace(',','').replace(' kg',''))
        except:
            weight = 0
            
        # 13. Features - descriptive field, e.g. 'reverse camera and dual zone climate control'; chunk of text and not tags
        try:
            features = main_left.find('strong', text = 'Features').find_parent('tr').find_all('td')[1].text
        except:
            features = ''
            
        # 14. Accessories - descriptive field, e.g. 'carbon fibre spoiler and custom bodykit'; chunk of text and not tags
        try:
            acc = main_left.find('a', text = 'Accessories').find_parent('tr').find_all('td')[1].text
        except:
            acc = ''
            
        # 15. Description - descriptive field, e.g. 'accident free and parked under shelter'; chunk of text and not tags
        try:
            desc = main_left.find('strong', text = 'Description').find_parent('tr').find_all('td')[1].text
        except:
            desc = ''
            
        # 16. COE Period Left (in days) - number of days in a month taken to be 30
        try:
            coe_left = main_left.find('strong', text = 'Reg Date').find_parent('tr').find_all('td')[1].text
            try:
                yrs = int(re.findall(r"\d+(?=yr)",coe_left)[0])
            except:
                yrs = 0
            try:
                mths = int(re.findall(r"\d+(?=mth)",coe_left)[0])
            except:
                mths = 0
            try:
                days = int(re.findall(r"\d+(?=day)",coe_left)[0])
            except:
                days = 0
            coe_left = yrs * 365 + mths * 30 + days
        except:
            coe_left= 0
            
        # 17. COE Price Paid
        try:
            coe_price = int(main_left.find('a', text = 'COE').find_parent('tr').find_all('td')[1].text.replace('$','').replace(',',''))
        except:
            coe_price = 0
            
        # 18. Open Market Value (OMV)
        try:
            omv = int(main_left.find('strong', text = 'OMV').find_parent('tr').find_all('td')[1].text.replace('$','').replace(',',''))
        except:
            omv = 0
            
        # 19. Additional Registration Fee (ARF)
        try:
            arf = int(main_left.find('strong', text = 'ARF').find_parent('tr').find_all('td')[1].text.replace('$','').replace(',',''))
        except:
            arf = 0
            
        # 20. Number of Past Owners
        try:
            owners = int(main_left.find('strong', text = 'No. of Owners').find_parent('tr').find_all('td')[1].text)
        except:
            owners = 0
            
        # 21. Vehicle Type - e.g. 'Sports Car', 'Luxury Sedan'. Each car can only have one vehicle type.
        try:
            veh_type = main_left.find('strong', text = 'Type of Veh').find_parent('tr').find_all('td')[1].text
        except:
            veh_type = ''
            
        # 22. Car Category - e.g. 'low mileage', 'direct owner' and 'auction'. Each car can belong to multiple categories.
        try:
            cat = main_left.find('strong', text = 'Category').find_parent('tr').find_all('td')[1].text
        except:
            cat = ''
            
        # 23. Date Posted
        date = main_left.find('div', id = 'usedcar_postdate').text
        date = re.findall(r"(?<=Posted on: )\w+-\w+-\w+",date)[0]
        date = datetime.strptime(date,'%d-%b-%Y')

        # 24. Date Updated - date updated is the date on which the seller has edited the listing. Not to be confused with the date on which the vehicle data in our local database was updated by the script.
        try:
            updated = main_left.find('div', id = 'usedcar_postdate').text
            updated = re.findall(r"(?<=Updated on: )\w+-\w+-\w+",updated)[0]
            updated = datetime.strptime(updated,'%d-%b-%Y')
        except:
            updated = 0
            
        # 25. Tags - contains permutations of the make, model and manufacturing year. E.g. "Mazda 3, mazda 3, 2014 Mazda 3, 2014 mazda 3, Mazda, Mazda 3, mazda 3, Used Mazda", with tags separated with commas.
        try:
            tags = main_left.find('div', id = 'cartags').text.replace('Tags: ','')
        except:
            tags = ''
        
        # 26. Date Sold - To initialise as 0; not scraped from webpage html.
        date_sold = 0
        
        # 27. Last Edited - To initialise as 0; not scraped from webpage html. Refers to the date on which the script had updated the vehicle's data in our local database. 
        last_edited = 0

        return([int(car_id), avail, make_model, price, depre, reg_date, manu_yr, mileage, tranny, eng_cap, road_tax, power, weight, features, acc, desc,
              coe_left, coe_price, omv, arf, owners, veh_type, cat, date, updated, tags, date_sold, last_edited])
    else:
        return None
