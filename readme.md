# Theme : Visualisation

### IDEA 

Allow user to upload a CSV file, then give them a bunch of statistics or let them edit the dataset such as filling in empty values, maybe let them choose which values are rendered

### TODO - Backend

- [x] Allow user to upload CSV
- [x] Sanitise CSV input (make sure it isnt a reverse shell etc) - shouldnt matter too much as it is not being directly run
- [x] Create a login/signup with jwt to be able to tie a user with their files
- [x] Check for valid CSV
- [x] Tie users to files via JWT
- [x] Implement a view_csv function which will work for all uploads
- [x] Allow users to delete their csvs
- [x] Implement Basic math functions like mean median and mode
- [ ] Implement graphs
- [ ] Send graphs to the frontend
- [ ] Allow users to save sessions ? - should be simple with a bit of json, dont want to store all the csvs on my server though - maybe implement a cleanup time


### TODO - Frontend
- [-] Create a homepage (done partially)
- [x] Create a view current CSVs page
- [x] Create a nice login page
- [x] Create a nice signup page
- [ ] Clean up the upload csv page
- [ ] Making a loading page
