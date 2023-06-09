from aws_cdk import (
    # Duration,
    Stack,
    aws_iam as iam,
    aws_lambda as _lambda,
    # aws_sqs as sqs,
    aws_events as events,
    aws_events_targets as targets,
)
from constructs import Construct

class OssStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        opensearch_backup_role = self.create_service_role_opensearch()

        my_policy2 = iam.PolicyStatement(
                    # sid= ["VisualEditor1"],
                    effect=iam.Effect.ALLOW,
                    actions=[
                     
                       "s3:GetObject",
                        "s3:PutObject",
                        "s3:DeleteObject"
                    ],
                    resources=["arn:aws:s3:::ossbkp2/*"]
                )
        
        opensearch_backup_role.add_to_policy(my_policy2)

        my_policy3 = iam.PolicyStatement(
                    # sid= ["VisualEditor1"],
                    effect=iam.Effect.ALLOW,
                    actions=[
                         "s3:ListBucket",
                    ],
                    resources=["arn:aws:s3:::ossbkp2"]
                )
               
        opensearch_backup_role.add_to_policy(my_policy3)


        service_rolelambda = self.create_service_rolelambda()


        lambda_layer = _lambda.LayerVersion(
               self, 'LambdaLayer',
               code= _lambda.Code.from_asset('lambda/layer') ,
               compatible_runtimes=[_lambda.Runtime.PYTHON_3_9],
               description='lambda Library',
               layer_version_name='LambdaLayer'
           )


        my_lambda = _lambda.Function(
            self, 
            'FusionLambdaFunction',
            description='Deploying Lambda Function Infrastrcture',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset('lambda/code'),
            layers=[lambda_layer],
            role= service_rolelambda,
            handler='hello.handler',
            environment={  
                        #    "bucket_name": alertbucket.bucket_name,
                            # "exerole": service_role_emr.role_arn,
                            # "ddbtablename": alertdynaomodb.table_name,
                            # "application": emr.attr_application_id,
                            # "app_id": emr.logical_id

                    }
             )
        

        #  # Create the EventBridge rule
        # event_rule = events.Rule(self, 'MyEventRule',
        #                          event_pattern=events.EventPattern(
        #                              detail_type=['MyEvent'],
        #                              schedule = =events.Schedule.rate(cdk.Duration.minutes(1)),
        #                              source=['my.event.source']
        #                          ))

         # Create the EventBridge rule
        event_rule = events.Rule(self, 'MyCronRule',
                                 schedule=events.Schedule.cron(
                                     hour='0/12',
                                     minute='0'
                                 ))

        # Add the Lambda function as a target for the EventBridge rule
        event_rule.add_target(targets.LambdaFunction(my_lambda))
        





    def create_service_rolelambda(self) -> iam.Role:
            return iam.Role(
                self,
                "Oopensearch-Backup-Lambda-Role",
                assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
                managed_policies=[
                    iam.ManagedPolicy(
                        self,
                        "PassRole_For_Lambda",
                        statements=[
                            iam.PolicyStatement(
                                sid="VisualEditor0",
                                actions=[
                                     "iam:PassRole"
                                ],
                                resources=["*"],
                            ),
                        ],                         
                    )
                ],
            )



    def create_service_role_opensearch(self) -> iam.Role:
            return iam.Role(
                self,
                "opensearch-snapshot-role",
                assumed_by=iam.ServicePrincipal("es.amazonaws.com"),
                managed_policies=[
                    iam.ManagedPolicy(
                        self,
                        "PassRole_For_opensearch",
                        statements=[
                            iam.PolicyStatement(
                                sid="VisualEditor0",
                                actions=[
                                     "iam:PassRole"
                                ],
                                resources=["arn:aws:iam::276301730779:role/opensearch-snapshot-role"],
                            ),

                            iam.PolicyStatement(
                                sid="VisualEditor1",
                                actions=[
                                     "es:ESHttpPut"
                                ],
                                resources=["arn:aws:es:region:276301730779:domain/domain-name/*"],
                            ),
                        ],
                        
                        
                    )
                ],
            )


