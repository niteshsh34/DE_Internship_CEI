## Theory 
### Q1. Why is Spark preferred over MapReduce?
**Limitations of MapReduce**
- Stores intermediate data on disk, making execution slower.
- High disk I/O increases processing time.
- Not suitable for iterative tasks like Machine Learning.
- Requires more complex code.
- Does not support real-time or interactive processing.
  
**Advantages of Spark**
- Uses in-memory computing for faster execution.
- Supports both batch and real-time processing.
- Provides easy APIs in Python, Scala, Java, and R.
- Includes built-in libraries for SQL, Machine Learning, Graph Processing, and Streaming.

---

### Q2. How does In-Memory Computing improve performance?
Spark keeps intermediate data in memory (RAM) instead of writing it to disk after every step. Since Machine Learning algorithms repeatedly process 
the same data, this reduces disk I/O and makes execution much faster than traditional MapReduce.

---

### Q5. Difference between `.na.drop()` and `.na.fill()`
- **`.na.drop()`** removes rows that contain null values.
- **`.na.fill()`** replaces null values with a specified value instead of removing the row.
Example:
```python
df.na.fill({"status": "Unknown"}).show()
```

---

### Q7. What is DataFrame Immutability?
Spark DataFrames are immutable, which means they cannot be changed after they are created. Any operation like filtering, dropping columns, or renaming 
columns creates a new DataFrame while keeping the original one unchanged.

---

### Q9. Why handle null values before aggregation?
Null values can affect functions like `sum()`, `avg()`, `min()`, and `max()`, leading to inaccurate or incomplete results. Cleaning null values before 
aggregation helps produce more reliable results.

---

### Q11. What is Shuffle in Spark?
Shuffle is the process of moving data between partitions during operations like `groupBy()`, `join()`, or `reduceByKey()`. It is called a **wide 
transformation** because data is exchanged across partitions, which increases network communication and execution time.

---

### Q14. Risk of using `inferSchema=True`
If the dataset contains inconsistent or invalid values (especially dates), `inferSchema=True` may detect incorrect data types or convert values to `NULL`. 
For messy datasets, defining the schema manually is usually a better option.
