from airflow import DAG
from datetime import datetime, timedelta
from cosmos.airflow.task_group import DbtTaskGroup
from cosmos.config import ProjectConfig, ProfileConfig
from cosmos.operators import DbtDocsOperator

default_args = {
    'description': 'A dag to orchestrate dbt with Cosmos',
    'start_date': datetime(2025, 7, 20),
}

dag = DAG(
    dag_id='dbt_data_orchestator',
    default_args=default_args,
    schedule=timedelta(minutes=10),
    catchup=False,
)

# Paths inside the Airflow container (see docker-compose volumes)
DBT_PROJECT_DIR = "/usr/app/superstore_dbt"
DBT_PROFILES_DIR = "/opt/airflow/.dbt"

with dag:
    # Create a TaskGroup that maps your dbt project to individual tasks per model
    project_cfg = ProjectConfig(dbt_project_path=DBT_PROJECT_DIR)
    profile_cfg = ProfileConfig(
        profile_name="superstore_dbt",
        target_name="dev",
        profiles_yml_filepath=f"{DBT_PROFILES_DIR}/profiles.yml",
    )

    dbt_tg = DbtTaskGroup(
        group_id="dbt_build",
        project_config=project_cfg,
        profile_config=profile_cfg,
        # default is to run `dbt build`. You can also set commands=["run"], etc.
    )

    # Optional: generate dbt docs as a separate task that depends on the build
    dbt_docs = DbtDocsOperator(
        task_id="dbt_docs",
        project_dir=DBT_PROJECT_DIR,
        profiles_dir=DBT_PROFILES_DIR,
        profile_config=profile_cfg,
    )

    dbt_tg >> dbt_docs