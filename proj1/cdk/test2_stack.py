from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    #  core,
    aws_iam as iam,
    aws_s3 as s3,
     Duration,
    aws_sns as sns,
    aws_s3_notifications as s3_notifications,
    
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
from cdk.test22 import Test22



# from shared_module import s3_arn

class Test2Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "Test2Queue",
        #     visibility_timeout=Duration.seconds(300),
        # )
        # print(s3_arn)
        # self.source_bucket_name_prefix = 'ossbkp1'
        self.destination_bucket_name_prefix='ossbkp2'
        destbucketarn= self.get_bucket_arn(self.destination_bucket_name_prefix,'us-west-2')
        
        # # role east2
        
        # self.role=iam.Role(
        #         self,
        #         's3_replica_poc_role',
        #         assumed_by=iam.ServicePrincipal('s3.amazonaws.com'),
        #         role_name=f's3-replication-role'
        #     )

        # iam.Policy(
        #         self,
        #         's3_replica_poc_policy',
        #         roles=[
        #             self.role
        #         ],
        #             statements=[
        #                 iam.PolicyStatement(
        #                 actions=["s3:ListBucket",
        #                 "s3:GetReplicationConfiguration",
        #                 "s3:GetObjectVersionForReplication",
        #                 "s3:GetObjectVersionAcl",
        #                 "s3:GetObjectVersionTagging",
        #                 "s3:GetObjectRetention",
        #                 "s3:GetObjectLegalHold",
        #                 "s3:ReplicateObject",
        #                 "s3:ReplicateDelete",
        #                 "s3:ReplicateTags",
        #                 "s3:ObjectOwnerOverrideToBucketOwner"],
        #                 resources=["*"]
        #             )
        #                                 # self.replication_source_policy(self.get_bucket_arn(self.source_bucket_name_prefix,'us-east-2')),
        #                 # self.replication_policy(self.get_bucket_arn(self.destination_bucket_name_prefix,'us-west-2'))
        #                   ]
                
        #     )
            
            
        service_role_s3 = self.create_service_role_s3()
            # replication rule 
        # self.replication_conf = s3.CfnBucket.ReplicationConfigurationProperty(
        #         role=service_role_s3.role_arn,
        #         rules=[
        #             s3.CfnBucket.ReplicationRuleProperty(
        #                 id='rule-replicate-all-data',
        #                 destination=s3.CfnBucket.ReplicationDestinationProperty(
        #                     bucket= destbucketarn
        #                 ),
        #             # prefix='',
        #             status='Enabled',
        #             # priority =,
        #             # source_selection_criteria =,
        #             # filter = ,
        #             # delete_marker_replication =,
                    
        #             )             
        #         ]
        #     )


        
        topic = sns.Topic(self, 'MyTopic')

        
    
        
            # bucket added replication rule 
        bucket=s3.CfnBucket( self, "source-bucket-65166516",bucket_name="source-bucket-65166516",
                        access_control="Private", 
                        bucket_encryption=s3.CfnBucket.BucketEncryptionProperty( 
                            server_side_encryption_configuration=[ 
                                s3.CfnBucket.ServerSideEncryptionRuleProperty( 
                                    server_side_encryption_by_default=s3.CfnBucket.ServerSideEncryptionByDefaultProperty( 
                                        sse_algorithm="AES256" ) ) ] ), 
                        public_access_block_configuration=s3.BlockPublicAccess.BLOCK_ALL,
                        replication_configuration=s3.CfnBucket.ReplicationConfigurationProperty(
                                role=service_role_s3.role_arn,
                                rules=[s3.CfnBucket.ReplicationRuleProperty(
                                        id='rule-replicate-all-data',
                                        destination=s3.CfnBucket.ReplicationDestinationProperty(
                                            bucket="arn:aws:s3:::ossbkp2-us-west-2"
                                        ),
                                    # prefix='',
                                    status='Enabled',
                                    # priority =,
                                    # source_selection_criteria =,
                                    # filter = ,
                                    # delete_marker_replication =,
                                    )]
                                  ),
                        tags= [{'key': 'environment', 'value': 'development'}, {'key': 'component', 'value': 'subscriber'}],
                         versioning_configuration=s3.CfnBucket.VersioningConfigurationProperty(status="Enabled"),
                         
                         notification_configuration = s3.CfnBucket.NotificationConfigurationProperty(
                             topic_configurations=[s3.CfnBucket.TopicConfigurationProperty(
                                event="s3:Replication:*",
                                topic=topic.topic_arn)]
                                             
                         ) )
        

        policy_statement = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=["sns:Publish"],
            resources=[topic.topic_arn],
            conditions={
                "ArnLike": {
                    "aws:SourceArn": bucket.attr_arn
                }
            },
            principals=[
                iam.ServicePrincipal("s3.amazonaws.com")
            ]
        )
        topic.add_to_resource_policy(policy_statement)
            
            
            
            
            
        # s3.CfnBucket(
        #         self,
        #         'Bucket-id',
        #         access_control='Private',
        #         bucket_name=f'{self.source_bucket_name_prefix}-{self.region}',
        #         versioning_configuration = s3.CfnBucket.VersioningConfigurationProperty(
        #             status='Enabled'
        #         ),
        #         replication_configuration=self.replication_conf,
        #         bucket_encryption=s3.CfnBucket.BucketEncryptionProperty(
        #             server_side_encryption_configuration=[s3.CfnBucket.ServerSideEncryptionRuleProperty(
        #                 bucket_key_enabled=True,
        #                 server_side_encryption_by_default=s3.CfnBucket.ServerSideEncryptionByDefaultProperty(
        #                     sse_algorithm="AES256",
                
        #                     # the properties below are optional
        #                     # kms_master_key_id="kmsMasterKeyId"
        #                 )
        #             )]
        #         )
        #     )
    @staticmethod        
    def get_bucket_arn(bucket_name_prefix,region):
        return f'arn:aws:s3:::{bucket_name_prefix}-{region}'.lower()      
            
    def create_service_role_s3(self) -> iam.Role:
            return iam.Role(
                self,
                "s3replicationRole",
                assumed_by=iam.ServicePrincipal("s3.amazonaws.com"),
                managed_policies=[
                    iam.ManagedPolicy(
                        self,
                        "s3-Full-Access",
                        statements=[
                            iam.PolicyStatement(
                                sid="VisualEditor0",
                                actions=[
                                    "s3:*"
                                ],
                                resources=["*"],
                            ),
                            
                        ],
                    )
                ],
            )

            
            
            
            
      