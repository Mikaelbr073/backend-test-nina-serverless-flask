from flask import Flask, request
import boto3

dynamodb_client = boto3.client('dynamodb')
PRODUCTS_TABLE = os.environ['PRODUCTS_TABLE'] 

def create_midia(body):
    # extrai as informações do objeto S3 da solicitação
    _id = body['_id']
    key = body['key']
    bucket = body['bucket']

    url = f'https://{bucket}.s3.amazonaws.com/{key}'

    # atualiza o item na tabela DynamoDB
    response = dynamodb.update_item(
        Table=PRODUCTS_TABLE,
        Key={
            '_id': _id    # tip: set post _id as object metadata in S3
        },
        UpdateExpression='SET medias = medias + :media',
        ExpressionAttributeValues={
            ':media': [url]
        },
        ReturnValues='UPDATED_NEW'
    )

    return response
