import os
import boto3
from flask import Flask, jsonify, make_response, json, request
from datetime import datetime

dynamodb_client = boto3.client('dynamodb')
PRODUCTS_TABLE = os.environ['PRODUCTS_TABLE'] 

#CRUD CREATE, READ, UPDATE, DELETE

def create_product(body):
    _id = body['_id']
    name = body['name']
    description = body['description']
    category = body['category']
    brand = body['brand']
    price = body['price']
    total = body['inventory']['total']
    available = body['inventory']['available']
    images = body.get('images', [])

    if not _id or not name or not description or not category or not brand or not price or not total or not available or not images:
        return jsonify({'error': 'Please provide all required fields'}), 400


    now = datetime.utcnow().isoformat()

    dynamodb_client.put_item(
        TableName=PRODUCTS_TABLE, Item={
            '_id': {'S': _id},
            'name': {'S': name},
            'description': {'S': description},
            'category': {'S': category},
            'brand': {'S': brand},
            'price': {'N': str(price)},
            'total': {'N': str(total)},  
            'available': {'N': str(available)},
            'images': {'SS': images},
            'created_at': {'S': now},
            'updated_at': {'S': now}
        }
    )

    return jsonify({
        '_id': _id,
        'name': name,
        'description': description,
        'category': category,
        'brand': brand,
        'price': price,
        'inventory': {
            'total': total,
            'available': available
        },
        'images': [images],
        'created_at': now,
        'updated_at': now

    })

def get_product(product_id):

    result = dynamodb_client.get_item(
        TableName=PRODUCTS_TABLE, Key={'_id': {'S': product_id}}
    )

    item = result.get('Item')
    if not item:
        return jsonify({'error': 'product does not exist'}), 404

    return jsonify(
        {
            '_id': item.get('_id').get('S'),
            'name': item.get('name').get('S'),
            'description': item.get('description').get('S'),
            'category': item.get('category').get('S'),
            'brand': item.get('brand').get('S'),
            'price': item.get('price').get('N'),
            'inventory': {
                'total': item.get('total').get('N'),
                'available': item.get('available').get('N')
            },
            'images': item.get('images').get('SS'),
            'created_at': item.get('created_at').get('S'),
            'updated_at': item.get('updated_at').get('S'),
        }
    )

def delete_product(product_id):

    result_validation = dynamodb_client.get_item(
        TableName=PRODUCTS_TABLE, Key={'_id': {'S': product_id}}
    )
    item = result_validation.get('Item')

    if not item:
        return jsonify({
            'error': 'product does not exist'
        }), 400
    else:
        result = dynamodb_client.delete_item(
            TableName=PRODUCTS_TABLE, Key={'_id': {'S': product_id}}
        )
        return jsonify({
            'Success': 'Product deleted successfully'
        }), 200


def list_all_product():
    result = dynamodb_client.scan(TableName=PRODUCTS_TABLE)
    items = result.get('Items', [])

    products = []
    for item in items:
        product = {
            '_id': item.get('_id').get('S'),
            'name': item.get('name').get('S'),
            'description': item.get('description').get('S'),
            'category': item.get('category').get('S'),
            'brand': item.get('brand').get('S'),
            'price': item.get('price').get('N'),
            'inventory': {
                'total': item.get('total').get('N'),
                'available': item.get('available').get('N')
            },
            'images': item.get('images').get('SS'),
            'created_at': item.get('created_at').get('S'),
            'updated_at': item.get('updated_at').get('S'),
        }
        products.append(product)

    return jsonify(products)

def update_product(product_id, update_data):
    item = dynamodb_client.get_item(TableName=PRODUCTS_TABLE, Key={'_id': {'S': product_id}}).get('Item')
    
    if not item:
        return jsonify({'error': 'product does not exist'}), 404

    # Cria um dicionário com as atualizações a serem realizadas
    update_expression = "set "
    expression_attribute_values = {}
    for key, value in update_data.items():
        update_expression += f" {key} = :{key},"
        expression_attribute_values[f":{key}"] = {'S': value}

    # Remove a vírgula extra no final da expressão de atualização
    update_expression = update_expression.rstrip(',')

    # Atualiza o item na tabela DynamoDB
    dynamodb_client.update_item(
        TableName=PRODUCTS_TABLE,
        Key={'_id': {'S': product_id}},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values
    )

   
    return get_product(product_id)

def update_product(product_id, update_data):

    # Verifica se o produto existe
    result = dynamodb_client.get_item(
        TableName=PRODUCTS_TABLE, Key={'_id': {'S': product_id}}
    )

    item = result.get('Item')
    if not item:
        return jsonify({'error': 'product does not exist'}), 404

    # Atualiza o item no DynamoDB
    now = datetime.utcnow().isoformat()
    dynamodb_client.update_item(
        TableName=PRODUCTS_TABLE,
        Key={'_id': {'S': product_id}},
        UpdateExpression='SET #name = :name, #description = :description, #category = :category, #brand = :brand, #price = :price, #total = :total, #available = :available, #images = :images, #updated_at = :updated_at',
        ExpressionAttributeNames={
            '#name': 'name',
            '#description': 'description',
            '#category': 'category',
            '#brand': 'brand',
            '#price': 'price',
            '#total': 'total',
            '#available': 'available',
            '#images': 'images',
            '#updated_at': 'updated_at',
        },
        ExpressionAttributeValues={
            ':name': {'S': update_data['name']},
            ':description': {'S': update_data['description']},
            ':category': {'S': update_data['category']},
            ':brand': {'S': update_data['brand']},
            ':price': {'N': str(update_data['price'])},
            ':total': {'N': str(update_data['inventory']['total'])},
            ':available': {'N': str(update_data['inventory']['available'])},
            ':images': {'SS': update_data.get('images', [])},
            ':updated_at': {'S': now},
        }
    )

    # Retorna o item atualizado
    updated_item = dynamodb_client.get_item(
        TableName=PRODUCTS_TABLE, Key={'_id': {'S': product_id}}
    )['Item']
    return jsonify({
        '_id': updated_item['_id']['S'],
        'name': updated_item['name']['S'],
        'description': updated_item['description']['S'],
        'category': updated_item['category']['S'],
        'brand': updated_item['brand']['S'],
        'price': float(updated_item['price']['N']),
        'inventory': {
            'total': int(updated_item['total']['N']),
            'available': int(updated_item['available']['N']),
        },
        'images': updated_item.get('images', {}).get('SS', []),
        'created_at': item['created_at']['S'],
        'updated_at': updated_item['updated_at']['S'],
    })
