### Terraform Setup

Contains scripts to create GCP Infra using Terraform. Following resources will be created

 - Cloud Storage Bucket which will be used as data lake.
 - Big Query as Data warehouse.

*pre-requisite:* 
- Make sure to export GCP credentials json, if not done already.
    ```shell
    # create env variable with credentials path
    export GOOGLE_APPLICATION_CREDENTIALS="<path/to/your/service-account-authkeys>.json"

    # Refresh service-account's auth-token for this session
    gcloud auth application-default login
    ```
- Install the terraform on you machine, refer this ![link](https://learn.hashicorp.com/collections/terraform/gcp-get-started) to get started. 


#### Declarations
* `terraform`: configure basic Terraform settings to provision your infrastructure
   * `required_version`: minimum Terraform version to apply to your configuration
   * `backend`: stores Terraform's "state" snapshots, to map real-world resources to your configuration.
      * `local`: stores state file locally as `terraform.tfstate`
   * `required_providers`: specifies the providers required by the current module
* `provider`: adds a set of resource types and/or data sources that Terraform can manage
   * The Terraform Registry is the main directory of publicly available providers from most major infrastructure platforms.
* `resource` is a block to define components of your infrastructure
  * Project modules/resources: google_storage_bucket, google_bigquery_dataset, google_bigquery_table
* `variable` & `locals` are used to define runtime arguments and constants


#### Execution steps
1. `terraform init` Initializes & configures the backend, installs plugins/providers, & checks out an existing configuration from a version control.
    ```shell
    # Initialize state file (.tfstate)
    terraform init
    ```
2. `terraform plan` Matches/previews local changes against a remote state, and proposes an Execution Plan. Provide GCP Project Id when prompted.
    ```shell
    # Check changes to new infra plan
    terraform plan
    ```
3. `terraform apply` Asks for approval to the proposed plan, and applies changes to cloud
    ```shell
    # Create new infra
    terraform apply
    ```
4. `terraform destroy` Removes your stack from the Cloud. Only run this if you want to delete this project.
    ```shell
    # Delete infra after your work, to avoid costs on any running services
    terraform destroy
    ```






