### Execution

Creating GCP Infra using Terraform. Following resources will be created

 - Cloud Staorage Bucket which will be used as data lake.
 - Big Query as Data warehouse.



```shell
# create env variable with credentials path
export GOOGLE_APPLICATION_CREDENTIALS="<path/to/your/service-account-authkeys>.json"

# Refresh service-account's auth-token for this session
gcloud auth application-default login
```

```shell
# Initialize state file (.tfstate)
terraform init

# Check changes to new infra plan
terraform plan -var="project=<your-gcp-project-id>"
```

```shell
# Create new infra
terraform apply -var="project=<your-gcp-project-id>"
```

```shell
# Delete infra after your work, to avoid costs on any running services
terraform destroy
```

