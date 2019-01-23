-- Remove vehicles that are still available for sale, and commercial vehicles.
DELETE
FROM cars
WHERE avail = 'Available' OR veh_type IN ('Truck', 'Bus/Mini Bus', 'Van', 'Others');

-- Some rows have depreciation = 0. Update depreciation figures.
-- For cars without depreciation figures and eligible for the PARF Rebate
UPDATE cars
SET final_depre = (price - arf / 2) / coe_left * 365
WHERE depre = 0 AND cat LIKE '%PARF Car%';

-- For cars without depreciation figures and not eligible for the PARF Rebate
UPDATE cars
SET final_depre = price / coe_left * 365
WHERE depre = 0 AND cat NOT LIKE '%PARF Car%';

-- For cars with depreciation figures from sgCarMart
UPDATE cars
SET final_depre = depre
WHERE depre != 0;

-- Removal of vehicles priced at $0
DELETE
FROM cars
WHERE price = 0;

-- Removal of OPC
DELETE
FROM cars
WHERE cat LIKE “%OPC Car%”;

-- Calculate the number of days each vehicle took to be sold
UPDATE cars
SET days_to_sell = julianday(date_sold) - julianday(date_posted);

-- Create new column 'make' in which we will store the car's make, after extracting it from the make_model column.
UPDATE cars
SET make = substr(trim(make_model),1,instr(trim(make_model)||' ',' ')-1);

-- Some cars such as 'Alfa Romeo' are problematic, since only the first word of the make is returned e.g. 'Alfa'.
-- Gather a list of unique makes.
SELECT DISTINCT make
FROM cars
ORDER BY make;

-- Update the makes that need fixing.
UPDATE cars
SET make = 'Alfa Romeo'
WHERE make = 'Alfa';

UPDATE cars
SET make = 'Aston Martin'
WHERE make = 'Aston';

UPDATE cars
SET make = 'Land Rover'
WHERE make = 'Land';

-- Create a new column 'segment' in the table and apply to the brands their respective segments.
UPDATE cars
SET segment = 'Exotic'
WHERE make IN ('Aston Martin', 'Ferrari', 'Lamborghini', 'McLaren');

UPDATE cars
SET segment = 'Ultra Luxury'
WHERE make IN ('Bentley', 'Land Rover', 'Maserati', 'Porsche', 'Rolls-Royce');

UPDATE cars
SET segment = 'Luxury'
WHERE make IN ('Audi', 'BMW', 'Jaguar', 'Jeep', 'Lexus', 'Lotus', 'Mercedes-Benz', 'Mitsuoka', 'Volvo');

UPDATE cars
SET segment = 'Mid Level'
WHERE make IN ('Alfa Romeo', 'Chrysler', 'Infiniti', 'MINI', 'Opel', 'Saab', 'Volkswagen');

UPDATE cars
SET segment = 'Economy'
WHERE make IN ('Chevrolet', 'Citroen', 'Fiat', 'Ford', 'Honda', 'Hyundai', 'Kia', 'Mazda', 'Mitsubishi', 'Nissan', 'Peugeot', 'Renault', 'Skoda', 'Ssangyong', 'Subaru', 'Suzuki', 'Toyota');

UPDATE cars
SET segment = 'Budget'
WHERE make IN ('Chery', 'Daihatsu', 'Geely', 'Perodua', 'Proton');

-- Add 'premium_ad' column to label ads as premium (1) or not (0).
UPDATE cars
SET premium_ad = CASE
	WHEN cat LIKE '%Premium Ad Car%' THEN 1
	ELSE 0
END;

-- Label listings as sold by direct owners (1) or not (0).
UPDATE cars
SET direct_owner = CASE
	WHEN cat LIKE '%Direct Owner Sale%' THEN 1
	ELSE 0
END;

-- Clean up empty columns containing descriptive text to prevent errors from popping up during the tf-idf analysis.
UPDATE cars
SET features = 'nil'
WHERE features IN ('-','');

UPDATE cars
SET features = 'nil'
WHERE features IS NULL;

UPDATE cars
SET acc = 'nil'
WHERE acc IN ('-','');

UPDATE cars
SET acc = 'nil'
WHERE acc IS NULL;

UPDATE cars
SET description = 'nil'
WHERE description IN ('-','');

UPDATE cars
SET description = 'nil'
WHERE description IS NULL;
