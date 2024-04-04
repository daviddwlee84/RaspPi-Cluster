# Prefect

> * [daviddwlee84/Prefect-Integrations: Show case of buttons (Streamlit) trigger pipeline and monitor executions in Prefect.](https://github.com/daviddwlee84/Prefect-Integrations)

* [PrefectHQ/prefect: Prefect is a workflow orchestration tool empowering developers to build, observe, and react to data pipelines](https://github.com/PrefectHQ/prefect)

Integration

* [PrefectHQ/prefect-dask: Prefect integrations with the Dask execution framework.](https://github.com/PrefectHQ/prefect-dask)
* [PrefectHQ/prefect-ray: Prefect integrations with Ray](https://github.com/PrefectHQ/prefect-ray)
* [Dask & Ray - Prefect Docs](https://docs.prefect.io/latest/guides/dask-ray-task-runners/?h=parallel+execution)

Other

* [PrefectHQ/prefect-recipes: Snippets and templates representing common Customer Success patterns](https://github.com/PrefectHQ/prefect-recipes)
* [biglocalnews/prefect-flow-template: A template repository with all the fundamentals needed to develop and deploy a Python data-processing routine for Prefect pipelines.](https://github.com/biglocalnews/prefect-flow-template)

## Concept

### Task Runner

* [**Task Runners - Prefect Docs**](https://docs.prefect.io/latest/concepts/task-runners/)
    * SequentialTaskRunner
    * ConcurrentTaskRunner
    * DaskTaskRunner
    * RayTaskRunner
* [rpeden/prefect-multiprocess: A multi-process task runner for Prefect](https://github.com/rpeden/prefect-multiprocess)

### Dependency: Flow

* [Flows - Prefect Docs](https://docs.prefect.io/latest/concepts/flows/)
* [Prefect Flow Dependencies Guide — Restack](https://www.restack.io/docs/prefect-knowledge-prefect-flow-dependencies)
* [Task Dependencies in Prefect - Examples — Restack](https://www.restack.io/docs/prefect-knowledge-prefect-task-dependencies-examples)

### Parallelism vs. Concurrency

* [Prefect Concurrency Explained — Restack](https://www.restack.io/docs/prefect-knowledge-prefect-concurrency-guide)

### Blocks

* [Blocks - Prefect Docs](https://docs.prefect.io/latest/concepts/blocks/)

### Results (States)

[Results - Prefect Docs](https://docs.prefect.io/latest/concepts/results/)

1. pass return_state to a task will make it return state

## How To

* [Big Data - Prefect Docs](https://docs.prefect.io/latest/guides/big-data/?h=cache#optimizing-your-python-code-with-prefect-for-big-data)

> 1. Remove task introspection with [`quote`](https://docs.prefect.io/latest/api-ref/prefect/utilities/annotations/#prefect.utilities.annotations.quote) to save time running your code.
>    * Simple wrapper to mark an expression as a different type so it will not be coerced by Prefect. For example, if you want to return a state from a flow without having the flow assume that state.
>    * quote will also instruct prefect to ignore introspection of the wrapped object when passed as flow or task parameter. Parameter introspection can be a significant performance hit when the object is a large collection, e.g. a large dictionary or DataFrame, and each element needs to be visited. This will disable task dependency tracking for the wrapped object, but likely will increase performance.
> 2. Write task results to cloud storage such as S3 using a block to save memory.
> 3. Save data to disk within a flow rather than using results.
> 4. Cache task results to save time and compute.
> 5. Compress results written to disk to save space.
> 6. Use a task runner for parallelizable operations to save time.

---

* [**You Probably Don’t Need a DAG | Workflow Best Practices & Misconceptions | Prefect**](https://www.prefect.io/blog/you-probably-dont-need-a-dag)
* [Interactive Workflows - Prefect Docs](https://docs.prefect.io/latest/guides/creating-interactive-workflows/) => Let user determine what to do next

---

* [Getting Started with Prefect | Task Orchestration & Data Workflows - YouTube](https://www.youtube.com/watch?v=D5DhwVNHWeU)
* [Introduction to Workflow Orchestration with Prefect- Kevin Kho | SciPy 2022 - YouTube](https://www.youtube.com/watch?v=XL4wgLUp-VA)
