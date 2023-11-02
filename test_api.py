import argparse
import requests
import pandas as pd

def main():
    parser = argparse.ArgumentParser(description='Test the FastAPI API with a text input and one optional csv file containing columns representing ground truths for claim detection and claim verification respectively.')
    parser.add_argument('--input_text', type=str, help='Textual input to identify and verify the claims in.')
    parser.add_argument('--ground-truth-csv', type=str, nargs='?', help='''Path to the optional CSV file containing the ground truth columns for claim detection and claim verification.
                        The claim detection column should be named claim_label and the claim verification should be named is_claim_correct. is_claim needs to have 0s or 1s, and is_correct can have 0s, 1s and 'na'.''')
    
    args = parser.parse_args()

    url = 'http://127.0.0.1:8000/process_text/'

    input_text = args.input_text
    ground_truth_csv = args.ground_truth_csv

    data = {
        "input_text": input_text
    }
    print(data)
    if ground_truth_csv is not None:
        data['file'] = ground_truth_csv

    response = requests.post(url, data=data)

    if response.status_code == 200:
        print("API response:")
        result = response.json()
        if result is not None:
            print(result)
        else:
            print("No result data in the response.")
    else:
        print(f"API request failed with status code {response.status_code}")

if __name__ == "__main__":
    main()