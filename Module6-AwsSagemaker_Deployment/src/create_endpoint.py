import boto3

sagemaker = boto3.client('sagemaker')
model_name = 'epam-mlehw-model'
role = 'arn:aws:iam::533267173325:role/roleml'
image_uri = '533267173325.dkr.ecr.ap-southeast-2.amazonaws.com/epam_mlehw'
endpoint_config_name = 'epam-mlehw-endpoint-config'
endpoint_name = 'epam-mlehw-endpoint'



def create_aws_model():

    response = sagemaker.create_model(
        ModelName=model_name,
        PrimaryContainer={
            'Image': image_uri
        },
        ExecutionRoleArn=role
    )

    print("Model created:", response)

def create_endpoint_conf():

    response = sagemaker.create_endpoint_config(
        EndpointConfigName=endpoint_config_name,
        ProductionVariants=[
            {
                'VariantName': 'AllTraffic',
                'ModelName': model_name,
                'ServerlessConfig': {
                    'MemorySizeInMB': 2048,
                    'MaxConcurrency': 5
                }
            }
        ]
    )

    print("Endpoint config created:", response)

def create_endpoint():

    response = sagemaker.create_endpoint(
        EndpointName=endpoint_name,
        EndpointConfigName=endpoint_config_name
    )

    print("Endpoint created:", response)


if __name__ == "__main__":
    create_aws_model()
    create_endpoint_conf()
    create_endpoint()