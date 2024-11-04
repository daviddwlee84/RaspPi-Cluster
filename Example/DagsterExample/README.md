# Dagster Example (Dagster University - Dagster Essentials)

* [**Dagster Essentials**](https://courses.dagster.io/courses/dagster-essentials)

```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple dagster

dagster project from-example --example project_dagster_university_start --name dagster_university

cd dagster_university
cp .env.example .env
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -e ".[dev]"

dagster dev --host 0.0.0.0
```

* [dagster-io/project-dagster-university: an ephemeral project repo for the DU Dagster project](https://github.com/dagster-io/project-dagster-university)
