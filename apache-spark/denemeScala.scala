// Databricks notebook source
val a=34

// COMMAND ----------

val b = 10

// COMMAND ----------

a*b

// COMMAND ----------

val irisdf = spark.read.format("csv").option("header","true").option("inferSchema","true").load("/FileStore/tables/Iris.csv")

// COMMAND ----------

irisdf.show()

// COMMAND ----------

display(irisdf.limit(20))

// COMMAND ----------


