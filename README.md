# Back-end test - deadline 10/04 at 12h
As part of the interview process, we would like you to build a CRUD application. This will allow us to evaluate your understanding of Python and AWS services.

**You should send the repository link to team@ninamob.com before the deadline, even if it's incomplete.**

## Dependencies
|  Package   |  Version  |
| :--------: | :-------: |
|   python   | >= 3.8 |

## Test

1. Build and deploy an AWS API using the Serverless Framework, Lambda functions, and DynamoDB for a CRUD system that manages market products. **It's very important to show your knowledge of the Serverless Framework**.

2. The products should have media attachments. Create and Delete media endpoints should be included, and uploaded media should be stored on an S3 Bucket, with the URL saved in the product's 'medias' array field.
    * Obs: The [Create product](/src/api/create_product.py) and [Insert Media](src/api/insert_media.py) functions have already been implemented as examples, but you may need to modify them to fit your specific requirements.

3. Each product must have the following schema, and you have to make sure the API doesn't allow different objects and that it returns the proper HTTP codes:

```json
Product object schema

{
  "_id": "string",
  "name": "string",
  "description": "string",
  "category": "string",
  "brand": "string",
  "price": "number",
  "inventory": {
    "total": "number",
    "available": "number"
  },
  "images": ["string"],
  "created_at": "Date",
  "updated_at": "Date"
}
```

## Deployment

In order to deploy your application to the AWS Cloud, simply run:

```
make build
make deploy
```

When you are done with the challenge, please remove the resources and clean the stack by running:

```
make remove
make clean
```

## Recommended tools

We encourage you to read the documentation of the tools used in this task:

- [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [Serverless](https://www.serverless.com/framework/docs/)

## **Environment**

### Serverless Framework

### Dependencies
|  Package   |  Version  |
| :--------: | :-------: |
|   serverless | latest |

### Setting up Serverless

1. Install ```serverless framework```: https://www.serverless.com/framework/docs/getting-started

### AWS
You are required to create an [AWS account](https://aws.amazon.com) if you don't have one yet.

### Dependencies
|  Package   |  Version  |
| :--------: | :-------: |
|   aws-cli   |  latest |

### Setting up AWS

1. Install ```aws-cli```: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
2. Configure credentials on your local machine, by running:

```bash
$ aws configure
AWS Access Key ID [None]: <Your-Access-Key-ID>
AWS Secret Access Key [None]: <Your-Secret-Access-Key-ID>
Default region name [None]: us-west-1
Default output format [None]: json
```
View [CLI Config](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html) for reference.

3. Create AWS credentials including the following IAM policies: ```AWSLambdaFullAccess```, ```AmazonS3FullAccess```, ```AmazonAPIGatewayAdministrator``` and ```AWSCloudFormationFullAccess```.

Run:
```sh
aws iam attach-user-policy --policy-arn arn:aws:iam::aws:policy/AWSLambdaFullAccess --user-name <username>

aws iam attach-user-policy --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess --user-name <username>

aws iam attach-user-policy --policy-arn arn:aws:iam::aws:policy/AmazonAPIGatewayAdministrator --user-name <username>

aws iam attach-user-policy --policy-arn arn:aws:iam::aws:policy/AWSCloudFormationFullAccess --user-name <username>
```
