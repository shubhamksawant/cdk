from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    #  core,
    aws_iam as iam,
    aws_s3 as s3,
     Duration,
    aws_sqs as sqs,
    aws_dynamodb as dynamodb,
    aws_opensearchservice as opensearchservice,
    aws_emrserverless as emrserverless,
    aws_scheduler as scheduler,
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_secretsmanager as secrets
)
from constructs import Construct

# from shared_module import s3_arn
class Test22(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        
            # bucket added replication rule 
        bucket=s3.CfnBucket( self, "bkp-bucket",bucket_name="ossbkp2-us-west-2",
                        access_control="Private", 
                        bucket_encryption=s3.CfnBucket.BucketEncryptionProperty( 
                            server_side_encryption_configuration=[ 
                                s3.CfnBucket.ServerSideEncryptionRuleProperty( 
                                    server_side_encryption_by_default=s3.CfnBucket.ServerSideEncryptionByDefaultProperty( 
                                        sse_algorithm="AES256" ) ) ] ), 
                        public_access_block_configuration=s3.BlockPublicAccess.BLOCK_ALL,
                         versioning_configuration=s3.CfnBucket.VersioningConfigurationProperty(status="Enabled"))
            
        # s3_arn=bucket.arn
            
            
            