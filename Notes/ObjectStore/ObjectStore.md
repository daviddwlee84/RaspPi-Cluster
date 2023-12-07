# Object Store

## Concept

Object storage differs from file and block storage in that data is stored in an "object" rather than in a block that makes up a file. There is no directory structure in object storage, everything is stored in a flat address space. The simplicity of object storage makes it scalable but also limits its functionality.

Unlike file systems, object storage does not support POSIX I/O calls: open, close, read, write and search for a file. Instead, they have only two basic operations: PUT and GET.

PUT creates a new object and fills it with data. As a result, the data in the existing object cannot be changed, so all objects in the repository are immutable. When you create a new object, the repository returns its unique identifier. This is usually a UUID, which has no internal meaning like a filename.
GET retrieves the contents of an object based on the object identifier (UUID). To edit an object in the repository, you need to create a copy of it and make changes to it. While doing so, you must keep track of which object identifiers correspond to the more recent version of the data.

## Links

* [HDFS vs Cloud-based Object storage(S3) - Blog | luminousmen](https://luminousmen.com/post/hdfs-vs-cloud-based-object-storage-s3)
* [HDFS vs. Cloud Storage: Pros, cons and migration tips | Google Cloud Blog](https://cloud.google.com/blog/products/storage-data-transfer/hdfs-vs-cloud-storage-pros-cons-and-migration-tips)
* [Cloud object storage vs HDFS (Hadoop Distributed File System) | Starburst](https://www.starburst.io/learn/data-fundamentals/cloud-object-storage-vs-hdfs/)
* [Object Storage vs. HDFS - Which is Better? | Triniti](https://www.triniti.com/data-warehousing-object-storage-vs-hdfs)
* [Top 5 Reasons for Choosing S3 over HDFS | Databricks Blog](https://www.databricks.com/blog/2017/05/31/top-5-reasons-for-choosing-s3-over-hdfs.html)
