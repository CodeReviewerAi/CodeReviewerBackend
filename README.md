# functionRetriever
Gets the original functions and calculates a score based on how often the function has been changed. Returns the functions along with the score as a JSON object.

# Todo:
- [ ] Fetch the all of the original functions from all of the https://github.com/hlxsites repositories
- [ ] Fetch how many times they have been changed after the first merge
- [ ] Calculate a score based on how many times they have been changed
- [ ] Return the functions along with the score as a JSON object 

# Things to contemplate 
- Should we only count commits with 'fix' or 'bug' etc. in the message
- Expand to all of the Repositories 
