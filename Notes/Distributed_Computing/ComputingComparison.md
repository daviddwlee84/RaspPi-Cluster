# Distributed Computing Comparison

## Overview

* Batch Computing - e.g. MapReduce
* Stream Computing - e.g. Live vote counting
    * Load balance
* Data Graph - e.g. PageRank

### Batch vs. Stream Computing

Batch Computing|Stream Computing
---------------|----------------
Offline|Real time
Preserve data, then process once|Input one, process one
User-drived request|Data-drived request
Pull to get result|Push to generate result

## Batch Computing

## Stream Computing

### Load Balace

#### Allocation strategies

### Collecting System Structure

#### Agent

#### Collector

#### Store

### Famous Framework of Stream Computing

* Storm of Twitter
* S4 of Yahoo
* Kafka of LinkedIn
* TimeStream of Microsoft
* Hstreaming of Hadoop
* StreamBase of IBM

## Data Graph

### Distributed Idea

#### Gather (Reduce)

#### Apply

#### Scatter

### BSP Mode (Bulk Synchronous Parallel)

* iteration of superstep
* a barrier between each superstep

### SSP (Stale Synchronous Parallel)

### Famous Framework of Graph Computing

* Hadoop-Titan
* GraphLab of CMU
* GraphX of Spark
* Pregel of Google
