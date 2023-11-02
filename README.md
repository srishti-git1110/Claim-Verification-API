# Claim-Verification-API
A FastAPI backend that lets you identify sentences that are claims in a piece of text input, verify those claims, and display the output as a structured table showing which claims are correct and which aren't along with additional information on why a particular claim is correct/incorrect.

## Table of Contents
* [Installation](https://github.com/srishti-git1110/Claim-Verification-API#installation)
* [Usage](https://github.com/srishti-git1110/Claim-Verification-API#usage)
* [Testing](https://github.com/srishti-git1110/Claim-Verification-API#testing)
* [API Endpoints](https://github.com/srishti-git1110/Claim-Verification-API#api-endpoints)
* [Contributing](https://github.com/srishti-git1110/Claim-Verification-API#contributing)
* [License](https://github.com/srishti-git1110/Claim-Verification-API#license)

## Installation
To run the Claim verification API on your local machine, follow these steps:

1. Clone the repository:
```
git clone https://github.com/srishti-git1110/Claim-Verification-API.git
cd Claim-Verification-API
```

2. Create a virtual environment (optional but recommended):
```
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install the project dependencies:
```
pip install -r requirements.txt
pip install uvicorn
```

4. You'll also need an OpenAI API, a SERPAPI, and a ClaimBusterAPI key for this in a .env file in the project's root directory. Make sure to create this file and enter your keys as environment variables.

## Usage
1. Start the FastAPI application using Uvicorn:
```
uvicorn app:app --reload
```
This will launch the API locally at http://127.0.0.1:8000.

2. Open a web browser or use an API testing tool (e.g., Postman or curl) to interact with the API.

## Testing
You can use the provided test_api.py script to test the API with a textual input. Simply run the script from the command line and provide the text as an argument:

```
python test_api.py --input_text "<input_text>"
```

The script will send a POST request to the API and display the results.

## API Endpoints
This API has one main endpoint:

* `POST /process_text`: Upload a text that you want the identify and verify the claims in.

## Contributing
If you'd like to contribute to this project, please follow these steps:

* Fork the repository on GitHub.
* Create a new branch for your feature or bug fix.
* Make your changes and submit a pull request.

Contributions are very much welcome!

## License
This project is licensed under the MIT License - see the LICENSE file for details.

