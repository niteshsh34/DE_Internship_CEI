# Week 6 - Apache Spark Theory Answers

## Q1. Explain the roles of the Driver, Cluster Manager, and Executor in a Spark application.
### Driver
The **Driver** is the main process of a Spark application. It is responsible for creating the SparkSession, converting the user's code into tasks, scheduling those tasks, and collecting the final results from executors. It also maintains metadata about RDDs and DataFrames.
### Cluster Manager
The **Cluster Manager** is responsible for managing the cluster's resources. It allocates CPU and memory to Spark applications and launches executors on worker nodes. Common cluster managers include Spark Standalone, YARN, Kubernetes, and Mesos.
### Executor
An **Executor** is a worker process that runs on worker nodes. Executors execute the tasks assigned by the Driver, store cached data in memory, perform computations, and return the results back to the Driver.

---

## Q2. How does Spark's Lazy Evaluation strategy improve performance when chain-processing large datasets?
Spark follows **Lazy Evaluation**, which means that transformations are not executed immediately. Instead, Spark records all transformations in a **Directed Acyclic Graph (DAG)** and waits until an action (such as `show()`, `count()`, or `collect()`) is called.
This improves performance because:
- Spark combines multiple transformations into a single optimized execution plan.
- It avoids unnecessary intermediate computations.
- It reduces disk I/O and network communication.
- It enables query optimization through the Catalyst Optimizer.
As a result, Spark processes large datasets more efficiently.

---

## Q4. What is the difference between CSV and Parquet in terms of storage (row-based vs. columnar) and why does it matter for performance?
### CSV
- Row-based storage format.
- Stores data as plain text.
- Larger file size.
- Slower to read and process.
- Does not store schema information.
- Limited compression.
### Parquet
- Columnar storage format.
- Stores data column by column.
- Smaller file size due to efficient compression.
- Stores schema information automatically.
- Optimized for analytical queries.
### Why does it matter?
Since Parquet stores data by columns, Spark reads only the required columns instead of the entire dataset. This significantly reduces disk I/O, memory usage, and query execution time. In contrast, CSV requires reading complete rows even if only a few columns are needed.

---

## Q7. How does Spark use the Lineage Graph (DAG) to provide fault tolerance if a worker node fails?
Spark maintains a **Lineage Graph (DAG)** that records every transformation applied to the data.
If a worker node fails and some partitions are lost:
1. Spark identifies the missing partitions.
2. It refers to the lineage graph.
3. It recomputes only the lost partitions by re-executing the required transformations.
4. The remaining data is not recomputed.
This approach provides efficient fault tolerance without requiring frequent backups or checkpoints.

---

## Q9. Explain the concept of Predicate Pushdown in Parquet and how it affects the amount of data loaded into memory.
**Predicate Pushdown** is an optimization technique used by Spark when reading Parquet files.
Instead of reading the entire dataset and then filtering it, Spark pushes the filter condition down to the Parquet storage layer.
For example:
```python
df.filter(col("age") > 30)
```
Spark examines Parquet metadata and skips row groups that cannot satisfy the condition.
### Benefits
- Reads only the required data.
- Reduces disk I/O.
- Loads less data into memory.
- Improves query execution speed.
- Reduces CPU usage.

---

## Q11. What is the difference between Transformations and Actions? Provide two examples of each.
### Transformations
Transformations create a new DataFrame or RDD from an existing one. They are **lazy**, meaning they are not executed immediately.
**Examples**
- `filter()`
- `select()`
### Actions
Actions trigger the execution of all pending transformations and either return a result or write data.
**Examples**
- `show()`
- `count()`
### Difference
| Transformations | Actions |
|-----------------|----------|
| Executed lazily | Trigger execution |
| Return a new DataFrame/RDD | Return a value or save data |
| Build the execution plan | Execute the execution plan |

---

## Q13. In Spark Architecture, what is the difference between Client Mode and Cluster Mode?
### Client Mode
- The Driver program runs on the user's local machine.
- Executors run on the cluster.
- If the client machine disconnects or crashes, the Spark application may stop.
- Commonly used for development and testing.
### Cluster Mode
- The Driver runs inside the cluster.
- Executors also run on cluster nodes.
- The application continues running even if the client disconnects.
- Commonly used for production workloads.
### Difference
| Client Mode | Cluster Mode |
|-------------|--------------|
| Driver runs on client machine | Driver runs inside the cluster |
| Suitable for development | Suitable for production |
| Application depends on client availability | Application continues even if client disconnects |
| Easier for debugging | Better fault tolerance and reliability |

---

## Q15. When exploring a dataset, why is it safer to use `.show(5)` instead of `.collect()` on a multi-terabyte dataset?
The `.show(5)` function displays only the first five rows of a DataFrame, whereas `.collect()` retrieves **every row** from all executors and stores them in the Driver's memory.
Using `.collect()` on a multi-terabyte dataset can:
- Cause an **OutOfMemory (OOM)** error.
- Crash the Driver program.
- Slow down the application due to excessive data transfer over the network.
Using `.show(5)` is much safer because:
- It retrieves only a small number of rows.
- It consumes very little memory.
- It is ideal for quickly inspecting data without risking application failure.
Therefore, `.show(5)` is the recommended method for exploring large datasets.
