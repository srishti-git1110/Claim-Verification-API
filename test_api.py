import argparse
import requests
import pandas as pd

def main():
    parser = argparse.ArgumentParser(description='Test the FastAPI API with a text input and one optional csv file containing columns representing ground truths for claim detection and claim verification respectively.')
    parser.add_argument('input_text', type=str, help='Textual input to identify and verify the claims in.')
    parser.add_argument('--ground-truth-csv', type=str, help='''Path to the optional CSV file containing the ground truth columns for claim detection and claim verification.
    The claim detection column should be named is_claim and the claim verification should be named is_correct. is_claim needs to have 0s or 1s, and is_correct can have 0s, 1s and nulls.'''
    
    args = parser.parse_args()
    url = 'http://127.0.0.1:8000/process-text/'

    input_text = args.input_text
    ground-truth-csv = None
    if args.ground-truth-csv:
        ground_truth_df = pd.read_csv(args.ground-truth-csv)

    # Prepare the data to send to the API
    data = {
        "input_string": input_text
    }

    if ground-truth-csv is not None:
        data['ground_truth_df'] = ground_truth_df.to_csv(index=False)

    response = requests.post(url, json=data)

    if response.status_code == 200:
        print("API response:")
        result = response.json().get("result")
        if result is not None:
            print(result)
        else:
            print("No result data in the response.")
    else:
        print(f"API request failed with status code {response.status_code}")

if __name__ == "__main__":
    main()
