import boto3
import json
import subprocess


def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError

apigws_to_check = []


def run_offat(swagger,id,stage):
    try:
        file = open("swagger_file.json","w+")
        file.write(json.dumps(swagger))
        file.close()
        ans = subprocess.check_output(["offat", "-f","swagger_file.json","-o",id+"_"+stage+"_output.html","-of","html"], text=True)
        print(ans)

    except subprocess.CalledProcessError as e:
        print(f"Command failed with return code {e.returncode}")


def get_api_swagger(client, api_id, stage_name='prod'):
    try:
        # Call the get_export method to get the Swagger definition
        response = client.get_export(
            restApiId=api_id,
            stageName=stage_name,
            exportType='swagger',
            parameters={
                'extensions': 'integrations'  # Optional: Include integrations
            },
            accepts='application/json'
        )
        
        # The Swagger content is in response['body'], which is a stream
        swagger_content = response['body'].read().decode('utf-8')
        return json.loads(swagger_content)
    
    except Exception as e:
        print(f"Error retrieving Swagger for API ID {api_id}: {e}")
        return None



def list_api_gateways(region):
    print("Building client for " + region)

    try:
        client = boto3.client('apigateway',region_name=region)

        # Initialize a paginator for API Gateway 'get_rest_apis' method
        paginator = client.get_paginator('get_rest_apis')
        for page in paginator.paginate():
            for api in page['items']:
                #print(f"API ID: {api['id']}")
                #print(f"API Name: {api['name']}")
                #print(f"API Description: {api.get('description', 'No description')}")
                #print("===")
                try:
                    stages_response = client.get_stages(restApiId=api['id'])
                    stages = stages_response.get('item', [])
                    
                    if stages:
                        print("Stages:")
                        for stage in stages:
                            swagger = get_api_swagger(client,api["id"],stage["stageName"])
                            print(f"  Stage Name: {stage['stageName']}")
                            print(f"  Deployment ID: {stage['deploymentId']}")
                            print(f"  Description: {stage.get('description', 'No description')}")
                            print(f"  Created Date: {stage.get('createdDate')}")
                            print(f"  Last Updated Date: {stage.get('lastUpdatedDate')}")
                            print("---")
                            run_offat(swagger,api["id"],stage["stageName"])
                            apigws_to_check.append({"id":api["id"],"name":api["name"],"description":{api.get('description', 'No description')},"region":region,"swagger":swagger,"stage":stage['stageName']})

                    else:
                        print("No stages found.")
                except Exception as e:
                    print(e)
        else:
            print("     No API Gateways in this region")
    except Exception as e:
        print("     "+str(e))


f_regions = open("regions.json", "r")
regions = json.loads(f_regions.read())["regions"]
f_regions.close()


for region in regions:
    list_api_gateways(region["name"])

apis = open("apis", "w")
apis.write(json.dumps(apigws_to_check,default=set_default))
apis.close()
