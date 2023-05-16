# Decisions

## Modeling

### Address Model
To start I took a look over the requested input and output. The first thing I
noticed is that the input and output generally had the same format. They were
both a list of "city, street, zip code" but with some additional formatting. So
I started out by writing a model to handle the internal format of the addresses.

### Smarty US Address Models
Once the base model was created I then spent some time looking at the smarty api
docs. There were two possible routes to use for address verification. The first
was for single addresses using a GET request and the second was for multiple
addresses using a POST request. The POST request seemed to be able to handle a
single address as well so I decided to model off of the POST request. I pulled
in the input and output of the POST request into my models.

### Settings Model
While looking over the Smarty docs I also took some time to see how
authentication was performed. Knowing the authentication needed to be easily
configurable I went ahead and setup a Settings model that pulled the required
auth keys from environment variables. To ease use locally I also added in a .env
parser to store the variables in during development.

## Structure
### Foundational structure
Once I had my basic models implemented I began determining how to structure the
code. I decided to split my logic between commands and actions. Commands are the
user interface. They interact with the user and then launch a series of actions
to then return formatted data back. The actions are parts of the logic that deal
with external data, whether reading a file, or hitting an api.

### Testability
By separating these types of IO out we structurally enforce the use of smaller
functions. Any time we cross the boundary between interacting with the user and
interacting with external data we have to create functions in their respective
areas. These smaller functions benefit us greatly when it comes time to unit
test as we have clear small pieces of functionality.

### Data handling
The separation of the actions from the commands leaves us with one more
structural challenge, the passing of data. I had already determined that I would
have a single internal data model that would handle both my input and output.
Now, I needed a way to transform this data between the internal model and the
model expected by the Smarty api. I chose to have external data types know how
to convert to and from the internal address model. This allows us to keep the
internal model simple and prevents bloat in the model as more external models
depend upon it. Each external model also has the benefit of only needing to know about the one
internal model because data can be transformed in and out of the internal model to
transition between different external models.

## Implementing
### Reading the CSV data
Now that my data models and code structure were formed I began creating a rough
implmentation. I started by creating my basic command to read in the csv data.
Once I had the command interface put together I created an action to parse the
data in the csv file into the internal address model. Upon viewing the example data in
the model I quickly realized that there were sometimes spaces before or after
the csv values. I decided to go ahead and do some data sanitization in the model
to strip any leading or trailing spaces so that I could benefit from the same
logic if other file types were ever read.

### Creating the API Call
Once I had the data read in to the internal model I created the additional code
in the Smarty api Models to be created from the internal model. After I had the
data in the Smarty api model I created a quick action to take in the internal
addresses and then call the smarty api using the smarty api model. I then read
the resulting data out into the response Smarty API Model and wrote the
corresponding code to convert back to the internal address model.

### Printing the output
At this point I had a question of whether to do the formatting in the model or
in the command. I ended up going with a bit of a median. I decided that a single
address should be able to format itself but the requested output of the
application was pretty specific to the command. So in the command I call the
model's format for both the input and output addresses and then simply
concatenate them together with the -> symbol.

## Testing and Refining
Now that I had a rough implementation together I began creating unit tests. I
created some tests to verify the basic examples would output correctly. These
tests failed as I had not setup the logic for printing invalid entries. So I
added in a valid field to the internal model and then had the smarty api model
set the field upon conversion to the internal model. I added in some logic to
the format function to handle the valid field being set to false and the output
began outputting correctly. I continued this test driven development approach
through the remaining parts of the application until I had a completely working
happy path implementation.

## API Limits
After having a happy path implementation working I proceeded on to manage the
failure states. Most importantly I began ensuring I did not break the documented
api limits. The smarty api had a limit of 100 addresses per request, so I added
logic to chunk out the requests if I needed to validate more than 100 addresses.
I used the tests I had already implemented to ensure that I did not break the
happy path as I wrote the chunking logic.

The next limit in the smarty api was in the individual fields of the address.
Each field had a max length to be enforced. This meant that we should not send
the address if it does not meet these max length requirements. However, I still
want to return that the address is invalid in this scenario. To accomplish this
I took advantage of the smarty api's input id. The smarty api allows you to
specify an input id that it then echos back out to you in the response. This
allowed me to set the ID before filtering out the addresses that would not be
sent to the api. Upon receiving the response from the Smarty api I then used the
input ids to place the responses in the appropriate indexes to maintain the
order that the addresses were input in with invalid addresses anywhere that was
not returned by the smarty api. Since I had already written unit tests for the
happy path I used those to ensure that the order remained the same upon adding
in the validation logic. I then wrote some additional tests surrounding specific
validation cases.

## Finishing Touches
Now that the application properly handled both happy path and input data
validation I began tidying up the codebase. I ensured that I had test cases on
exceptions I threw as well as on my various branches of input data logic.
Finally I performed some final documentation and formatting of the codebase.
