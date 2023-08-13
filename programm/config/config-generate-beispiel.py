import configparser

# CREATE OBJECT
config_file = configparser.ConfigParser()

# ADD SECTION
config_file.add_section("K01")
# ADD SETTINGS TO SECTION
config_file.set("K01", "typ", "n26")
config_file.set("K01", "iban", "DE02120300000000202051")
config_file.set("K01", "bic", "BYLADEM1001")
config_file.set("K01", "dateiname_suche", "n26")

# ADD SECTION
config_file.add_section("K02")
# ADD SETTINGS TO SECTION
config_file.set("K02", "typ", "migros")
config_file.set("K02", "iban", "CH0208401000051138778")
config_file.set("K02", "bic", "MIGRCHZZXXX")
config_file.set("K02", "dateiname_suche", "migros")

# SAVE CONFIG FILE
with open(r"config.ini", 'w') as configfileObj:
    config_file.write(configfileObj)
    configfileObj.flush()
    configfileObj.close()

print("Config file 'config.ini' created")

# PRINT FILE CONTENT
read_file = open("config.ini", "r")
content = read_file.read()
print("Content of the config file are:\n")
print(content)
read_file.flush()
read_file.close()
