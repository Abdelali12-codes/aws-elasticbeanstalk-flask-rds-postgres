# aws-eb-flask-rds-postgres

## create eb environment with service role

```
eb create env --service-role role-arn
```

* the default name of the role once you create the env using eb cli is aws-elasticbeanstalk-service-role

* the default instance profile (the role attached to the instances) is aws-elasticbeanstalk-ec2-role

## create eb environment with application load balancer

```
eb create env --elb-type application
```

## export eb logs to aws cloudwatch using aws cloudwatch agent

### files to export to cloudwatch

* /var/log/eb-engine.log
* /var/log/eb-hooks.log
* /var/log/web.stdout.log
* /var/log/nginx/access.log
* /var/log/nginx/error.log



## instance log streaming

```
eb logs --cloudwatch-logs enable
```
