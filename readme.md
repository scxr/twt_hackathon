# Theme : Visualisation

### IDEA 

Allow user to upload a CSV file, then give them a bunch of statistics or let them edit the dataset such as filling in empty values, maybe let them choose which values are rendered

### Problems

I have no clue how to do a single piece of frontend o.o *Codepen here I come*

### TODO - Backend

- [x] Allow user to upload CSV
- [x] Sanitise CSV input (make sure it isnt a reverse shell etc) - shouldnt matter too much as it is not being directly run
- [x] Create a login/signup with jwt to be able to tie a user with their files
- [x] Check for valid CSV
- [x] Tie users to files via JWT
- [ ] Implement Basic math functions like mean median and mode
- [ ] Implement graphs
- [ ] Send graphs to the frontend
- [ ] Allow users to save sessions ? - should be simple with a bit of json, dont want to store all the csvs on my server though - maybe implement a cleanup time


### TODO - Frontend
- [ ] Literally everything :(