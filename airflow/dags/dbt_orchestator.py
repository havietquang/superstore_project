from airflow import DAG
from datetime import datetime, timedelta

from cosmos.airflow.task_group import DbtTaskGroup
from cosmos.config import ProjectConfig, ProfileConfig,RenderConfig
from cosmos.operators import DbtDocsOperator

default_args = {
    "description": "A DAG to orchestrate dbt with Cosmos",
    "start_date": datetime(2025, 7, 20),
}

with DAG(
    dag_id="dbt_data_orchestrator",
    default_args=default_args,
    schedule=timedelta(minutes=10),
    catchup=False,
) as dag:

    # Paths inside Airflow container
    DBT_PROJECT_DIR = "/opt/airflow/dbt/superstore_dbt"

    project_cfg = ProjectConfig(
        dbt_project_path=DBT_PROJECT_DIR
    )

    profile_cfg = ProfileConfig(
        profile_name="superstore_dbt",
        target_name="dev",
        profiles_yml_filepath="/opt/airflow/.dbt/profiles.yml",
    )

    dbt_build = DbtTaskGroup(
        group_id="dbt_build",
        project_config=project_cfg,
        profile_config=profile_cfg,
        render_config=RenderConfig(
        emit_datasets=False
    ),
    )

    dbt_docs = DbtDocsOperator(
        task_id="dbt_docs",
        project_dir=DBT_PROJECT_DIR,
        profile_config=profile_cfg,
    )

    dbt_build >> dbt_docs
