# Petfinder-api
## Description
The Petfinder API is a versatile web application enabling users to access comprehensive information about animals available in shelters. Users can conveniently bookmark their favorite animals. Moreover, within the database, users can fine-tune their search criteria to find animals that closely match their preferences.

## Setup

  You will need to obtain your own key from this webiste:

    https://www.petfinder.com/developers/
    
  Clone the repository to your own device. Make sure to click on "SSH".
  
     git clone git@github.com:baileynield/Petfinder-api.git

  Create a virtual environment

     python -m venv .env

  Activate the virtual environment
  
     source .venv/bin/activate

  Install the requirements file

    pip install -r requirements.txt

  Create a database in pgadmin
  Create Alembic Revision

    alembic revision --autogenerate -m "Create tables"
    alembic upgrade head

  Use uvicorn to run the applcation making sure you are using an available port. Go to the location in your web browser. It should look something like this:

    http://127.0.0.1:8000/docs

  ## Aknowledgments
  Thank you to Petfinder Api for providing the information used about the specific animals!

  
  
