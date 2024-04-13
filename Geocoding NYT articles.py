from Tkinter import *
import tkMessageBox    #the * in previous line should already import this but need this line b/c of line 10 and 32
import requests, json, csv, os, arcpy
from nytimesarticle import articleAPI
from geopy.geocoders import Nominatim
from HTMLParser import HTMLParser
from bs4 import BeautifulSoup

arcpy.env.overwriteOutput = True  # Allows access to overwrite existing files
api = articleAPI('8a7bed87ddf84a98bd560ba2eb3ba3fb')  # NYT Article Search API key
inputWorkspace = r'D:\Computer Prog GIS\Amy_Tom_Haoyu'   # Type user's working directory here

# Function to create the GUI
def buildGUI():
    
    # Function to save the user's inputs into a text file
    def save():
        text = E1.get() + "\n" + "glocations, " + E2.get() + "\n" + E3.get() + "\n" + E4.get()  # The .get() returns the user's query inputs that were typed in the entry text boxes as a string
        with open("QueryResults.txt", "w") as f:   # Creates and writes the user inputs into a text file which will be located in the same directory as this script
            f.writelines(text) # Writes the string set to the 'text' variable into the text file

    # Function that creates the pop up message once the GO button is clicked on by the user
    def saveMessage():
        tkMessageBox.showinfo("Query Message", "Success! Query in progress.")

    # Function that executes the 'save' and then 'saveMessage' functions once the GO button is clicked on by the user
    def buttonClicked():
        save()
        saveMessage()
    
    top = Tk(className = "NYTimes Article Search GUI")    # Establishes the GUI and labels it with a title 
    top.minsize(width = 350, height = 100)     # Sets the dimensions of the GUI

    # Sets up the 5 labels seen on the left side of the GUI 
    Label(top, text = "Search Words ***").grid(row=0)     # Searches through Headline, Body, and Byline
    Label(top, text = "Geographic Location (Only one)").grid(row=1)    
    Label(top, text = "Start Date (YYYYMMDD) ***").grid(row=2)
    Label(top, text = "End Date (YYYYMMDD) ***").grid(row=3)

    Label(top, text = "*** = Required Field").grid(row=4)    # Note to the user

    # Sets up text boxes on the right side of the GUI for the user to type their query information into
    E1 = Entry(top)
    E2 = Entry(top)
    E3 = Entry(top)
    E4 = Entry(top)

    E1.grid(row=0, column=1)   
    E2.grid(row=1, column=1)
    E3.grid(row=2, column=1)
    E4.grid(row=3, column=1)

    # Sets up the GO button at the botton of the GUI and specifies that when it is clicked, it calls the buttonClicked function defined above
    Button(top, text = "GO", command = buttonClicked).grid(row=5, column=0)

    # Specifies the end of the GUI
    top.mainloop()

    # Path to where the above text file is located, again it is located in the same directory as this script
    folderPath = 'D:\\Computer Prog GIS\\Amy_Tom_Haoyu\\'
    inputFN = "QueryResults.txt"
    inputFilePath = folderPath + inputFN

    # Reads in the text file and sets all the lines of the text file to the variable named 'fileString'
    f1 = open(inputFilePath, "r")
    fileString = f1.read()
    f1.close()

    # all of these variables are set as global variables so they can be used outside of this 'buildGUI' function
    global queryList
    queryList = fileString.split("\n")  # Creates a list in which each line of the text file is an element in the list 

    global wordSearch
    wordSearch = queryList[0]  # User input keywords
    print wordSearch  # Test

    global searchDateStart
    searchDateStart = queryList[2]  # User input begin date
    print searchDateStart  # Test

    global searchDateEnd
    searchDateEnd = queryList[3]  # User input end date
    print searchDateEnd  # Test

    # Used this dictionary and list in while loop below
    global requiredFieldDict
    global requiredFieldList
    requiredFieldDict = {wordSearch: "Search Words", searchDateStart: "Start Date", searchDateEnd: "End Date"}
    requiredFieldList = [wordSearch, searchDateStart, searchDateEnd]

# Calls the function to create the GUI
buildGUI()

# If one of the required fields in the GUI is left empty by the user, the GUI will reopen (blank) and a message will tell the user to fill in that field
B = True
while B:
    B = False
    for field in requiredFieldList:
        if field == "":
            B = True
            print requiredFieldDict[field], "is a required field, please fill it in."
            buildGUI()
            break

try:   # Run entire script unless a KeyError is encountered
    geoLocation = queryList[1].split(", ")     # Separates the fq type parameter of "glocations" and the user's location query input so that they can be indexed and later referenced individually 
    HLURLnoLoc = {}  # Initialize empty dictionary to store headline:URL pairs when user specifies no location
    header = ["Lon", "Lat", "Title", "URL"] # Specify the column names of the outputted csv file 

    if geoLocation[1] == "":  # If no location is specified by user
        print "No location specified"       
        articles = api.search(q = wordSearch, begin_date = searchDateStart, end_date = searchDateEnd, fl = ['web_url', 'lead_paragraph', 'abstract', 'source', 'headline'])    # ArticleSearch API query
        accessKey = articles['response']['docs']  # Create variable that accesses keys of nested dictionaries from Article Search results

        # If no results are found for the ArticleSearch API query, kill the script
        if len(accessKey) == 0:
            print "No articles found."
            quit()  
            
        for ele in accessKey:  # Loop through each element in the Article Search nested dictionaries
            webURL = ele['web_url']  # Access web URL key in nested dictionary and assign to variable
            headline = ele['headline']['main']  # Access main headline in nested dictionary and assign to variable
            HLURLnoLoc[headline] = webURL  # Updates empty dictionary with headline:URL pairs
            print headline  # Test
            print webURL  # Test

        url = 'https://geoparser.io/api/geoparser' # URL for Geoparser.io service
        headers = {'Authorization': 'apiKey 96371282185817752'} # API key for Geoparser

        HLURLVals = HLURLnoLoc.values()  # Access dictionary URL values as a list and assign to variable

        csvName = "newspaperResults.csv" # Specify the csv name
        testCsv = os.path.join(inputWorkspace, csvName) # Joining the working directory and csv
        f = open(testCsv, 'wb') # Open the csv and write 
        w = csv.writer(f, delimiter = ',') # Tell the program that the csv file is comma deliminated
        w.writerow(header) # Write the header
        
        t = 0  # Initialize count
        for val in HLURLVals:  # For loop to extract URLs so the HTML parser can be used to find place names within the website's text
            r = requests.get(val)  # Create response object to make requests for HTML text from website
            HTML = BeautifulSoup(r.text, 'html.parser')  # Create object to parse HTML text from webpage using Beautiful Soup and HTMLParser standard library
            articleTxt = [''.join(s.findAll(text=True)) for s in HTML.findAll('p')]  # Create list, find all HTML text elements, create for loop to find all paragraph elements ('p') in HTML, then join text to empty string. This converts all HTML text to string within list

            lstVal = [val]  # Create list of URL values
            for ch in lstVal: # For loop to iterate through each letter in list of URL characters
                if ch[23:28] == 'video':  # If characters within specified URL index values = 'video', return index 0
                    artSlice = articleTxt[0]  # Slice list of article text to get first line of video description
                else:  
                    artSlice = articleTxt[1:10]   # For all other scenarios, index for first 9 lines of the article after the first line
                    
            GPinput = ''  # Initialize empty string

            for item in artSlice:  # For loop to extract each line of body text and join them in an empty string
                GPinput = GPinput + ''.join(item)  # Join each line of body text to empty string
                data = {'inputText': GPinput}  # Passing HTML text into Geoparser API
                resp = requests.post(url, headers=headers, data=data)  # Create another response object to make request for Geoparser output
                parsed_json = json.loads(resp.text)  # Decode json output from Geoparser

            # If no location name were found in extracted article text, outputs information on New York Time HQ building
            if parsed_json['features'] == []: 
                coordinateList = [[-73.9904, 40.7562], "New York Times building", "NY", "US"]
                print coordinateList
                placeCoordinates = coordinateList[0]   # Puts the Longitude, Latidue element in 'coordinatList' into their own list

            # If location name was found in extracted article text, outputs information on that location
            else:
                placeCoordinates = parsed_json['features'][0]['geometry']['coordinates']  # Index for coordinates of location in article
                placeName = parsed_json['features'][0]['properties']['name']  # Index for name of location in article
                placeADM1 = parsed_json['features'][0]['properties']['admin1']  # Index for first-level administrative district of location in article
                placeCountry = parsed_json['features'][0]['properties']['country']  # Index for country of location in article
                LocFound = [placeCoordinates[0], placeCoordinates[1], placeName, placeADM1, placeCountry]
                print LocFound

            urls = HLURLnoLoc.values()[t].encode('utf-8')  # Converts from unicode to ascii
            titles = HLURLnoLoc.keys()[t].encode('utf-8')  # Converts from unicode to ascii 
            geocodeList = [placeCoordinates[0], placeCoordinates[1], titles, urls]   # List of Longitude, Latitude, Title, URL values that will be inserted into the csv 
            print geocodeList
            w.writerow(geocodeList)   # Writes values in 'geocodeList' into the csv
            t += 1   # Increases count by 1 so that the encoding lines above will apply to the next article in the for loop
        f.close()

    else:  # If user specifies location
        geoLocDict = {geoLocation[0]:geoLocation[1]}   # key = glocations, value = location the user inputted
        print geoLocDict
        articles = api.search(q = wordSearch, fq = geoLocDict, begin_date = searchDateStart, end_date = searchDateEnd, fl = ['web_url', 'lead_paragraph', 'abstract', 'source', 'headline'])   # ArticleSearch API query
        accessKey = articles['response']['docs']  # Create variable that accesses keys of nested dictionaries from Article Search results

        # If no results are found for the ArticleSearch API query, kill the script
        if len(accessKey) == 0:
            print "No articles found."
            quit()  

        geolocator = Nominatim()  # Create geocoding object using Geopy module
        place = geoLocDict.values()   # Values of 'geoLocDict' dictionary as specified above
        location = geolocator.geocode(place)  # Input user specified location into the geolocator 
        
        lon = location.raw['lon']  # Gets longitude of user specified location
        lat = location.raw['lat']  # Gets latitude of user specified location

        csvName = 'newspaperResults.csv'   # Specify the csv name
        testCsv = os.path.join(inputWorkspace, csvName)   # Joining the working directory and csv
        f = open(testCsv, 'wb')   # Open the csv and write 
        w = csv.writer(f, delimiter = ',')   # Tell the program that the csv file is comma deliminated
        w.writerow(header)   # Write the header
        
        Dict = {}  # Create empty dictionary
        for ele in accessKey:  # Loop through each element in the Article Search nested dictionaries
            articleURL = ele['web_url']  # Access web URL key in nested dictionary and assign to variable
            mainHL = ele['headline']['main']  # Access main headline in nested dictionary and assign to variable
            Dict[mainHL] = articleURL  # Update output dictionary

        # Goes through all outputted articles and writes their information into the csv
        t = 0    # Initialize t
        while t < len(accessKey):
            urls = Dict.values()[t].encode('utf-8')   # Converts from unicode to ascii
            titles = Dict.keys()[t].encode('utf-8')   # Converts from unicode to ascii
            rows = [lon, lat, titles, urls]     # List of Longitude, Latitude, Title, URL values that will be inserted into the csv
            print rows
            w.writerow(rows)  # Writes values in 'rows' list into the csv
            t += 1   # Increases count by 1 so that the encoding lines above will apply to the next article in the while loop

        f.close()  # Close csv file

    arcpy.env.workspace = r'D:\Computer Prog GIS\Amy_Tom_Haoyu'  # Set workspace to same working directory as 'inputWorkspace' 
    output = 'News Paper Article Locations'  # Assign layer title to variable
    arcpy.MakeXYEventLayer_management(testCsv, 'Lon', 'Lat', output)  # Display XY coordinates from CSV file

    saved = 'result.lyr'  # Assign file name of geocoded articles to variable
    arcpy.SaveToLayerFile_management(output, saved)  # Save the XY point data to new layer file

    mxd = arcpy.mapping.MapDocument('empty.mxd')  # Assign this empty map document to variable
    df = arcpy.mapping.ListDataFrames(mxd)[0]  # Activate and assign data frame we're working with to variable
    lyr = arcpy.mapping.Layer('result.lyr')  # Assign the geocoded article result data to layer object
    basemap = arcpy.mapping.Layer('Basemap.lyr')  # Assign basemap layer to variable
    ref = arcpy.mapping.Layer('Reference.lyr')  # Assign reference layer to variable
    template = arcpy.mapping.Layer('template.lyr')  # Assign symbology template layer to variable
    arcpy.management.ApplySymbologyFromLayer(lyr, template)  # Apply symbology from template layer to geocoded article results layer
    arcpy.mapping.AddLayer(df, lyr)  # Add results layer to data frame
    arcpy.mapping.AddLayer(df, ref, 'BOTTOM')  # Add reference layer to data frame above basemap layer
    arcpy.mapping.AddLayer(df, basemap, 'BOTTOM')  # Add basemap layer to bottom of active data frame
    labelLyr = arcpy.mapping.ListLayers(mxd, '', df)[0]  # Activate and assign geocoded article results layer to variable
    labelLyr.showLabels = True  # Turn on labels for results layer
    arcpy.RefreshActiveView()
    arcpy.RefreshTOC()
    mxd.saveACopy('Final.mxd')  # Save a copy of the output map document as a final map document for viewing

    print "Success!"

except KeyError:  # If a KeyError is thrown at any point during the script, run this code instead
    print "Please check your input dates and make sure they are properly formatted."
