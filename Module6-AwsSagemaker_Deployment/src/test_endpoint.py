import json
import boto3

runtime = boto3.client('sagemaker-runtime')
endpoint_name = 'rf-clf-endpoint'


# Example input data
input_data = {
    'features': [[5.1, 3.5, 1.4, 0.2]]
}

response = runtime.invoke_endpoint(
    EndpointName=endpoint_name,
    ContentType='application/json',
    Body=json.dumps(input_data)
)

result = json.loads(response['Body'].read().decode())
print("Inference result:", result)
