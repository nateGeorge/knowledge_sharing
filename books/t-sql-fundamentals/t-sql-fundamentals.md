---
marp: true

style: @import url('https://unpkg.com/tailwindcss@^2/dist/utilities.min.css');
---

# T-SQL Fundamentals, Third Edition

by Itzik Ben-Gan

August 2016

---

# Chapter 1 summary

History - SEQUEL from IBM in 1970s, trademark/copyright issue so had to be SQL.

- Today it is common to see RDBMSs that support languages other than a dialect of SQL, such as the CLR integration in SQL Server (e.g. use C# to get at SQL data directly)

Most programming languages are imperative, but SQL is declarative - tell it what you want, not how to do it.


---

# Types of SQL statements

SQL has several categories of statements, including Data Definition Language (DDL), Data Manipulation Language (DML), and Data Control Language (DCL). DDL deals with object definitions and includes statements such as CREATE, ALTER, and DROP. DML allows you to query and modify data and includes statements such as SELECT, INSERT, UPDATE, DELETE, TRUNCATE, and MERGE. It’s a common misunderstanding that DML includes only data-modification statements, but as I mentioned, it also includes SELECT. Another common misunderstanding is that TRUNCATE is a DDL statement, but in fact it is a DML statement. DCL deals with permissions and includes statements such as GRANT and REVOKE. This book focuses on DML.

---

# T-SQL

T-SQL is based on standard SQL, but it also provides some nonstandard/proprietary extensions. Moreover, T-SQL does not implement all of standard SQL. In other words, T-SQL is both a subset and a superset of SQL.

---

# Set theory and predicates

By a “set” we mean any collection M into a whole of definite, distinct objects m (which are called the “elements” of M) of our perception or of our thought.

—Joseph W. Dauben and Georg Cantor (Princeton University Press, 1990)


Loosely speaking, a predicate is a property or an expression that either holds or doesn’t hold—in other words, is either true or false.

# Relational model

The first version of the relational model was proposed by Codd in 1969 in an IBM research report called “Derivability, Redundancy, and Consistency of Relations Stored in Large Data Banks.” A revised version was proposed by Codd in 1970 in a paper called “A Relational Model of Data for Large Shared Data Banks,” published in the journal Communications of the ACM.


The goal of the relational model is to enable consistent representation of data with minimal or no redundancy and without sacrificing completeness, and to define data integrity (enforcement of data consistency) as part of the model.

“Relational” actually pertains to the mathematical term relation. In set theory, a relation is a representation of a set. In the relational model, a relation is a set of related information, with the counterpart in SQL being a table—albeit not an exact counterpart. A key point in the relational model is that a single relation should represent a single set (for example, Customers).

---

# Missing NULL values

One aspect of the relational model is the source of many passionate debates—whether predicates should be restricted to two-valued logic. That is, in two-valued predicate logic, a predicate is either true or false. If a predicate is not true, it must be false. Use of two-valued predicate logic follows a mathematical law called “the law of excluded middle.” However, some say that there’s room for three-valued (or even four-valued) predicate logic, taking into account cases where values are missing. A predicate involving a missing value yields neither true nor false—it yields unknown.

Some people believe that three-valued predicate logic is nonrelational, whereas others believe that it is relational. Codd actually advocated for four-valued predicate logic, saying that there were two different cases of missing values: missing but applicable (A-Values marker), and missing but inapplicable (I-Values marker). An example of “missing but applicable” is when an employee has a mobile phone, but you don’t know what the mobile phone number is. An example of “missing but inapplicable” is when an employee doesn’t have a mobile phone at all.

NULL is not a value but rather a marker for a missing value. Therefore, though unfortunately it’s common, the use of the terminology “NULL value” is incorrect. The correct terminology is “NULL marker” or just “NULL.”

---

# Constraints

Data integrity is achieved through rules called constraints that are defined in the data model and enforced by the RDBMS. The simplest methods of enforcing integrity are assigning an attribute type with its attendant “nullability” (whether it supports or doesn’t support NULLs).

Other examples of constraints include candidate keys, which provide entity integrity, and foreign keys, which provide referential integrity. A candidate key is a key defined on one or more attributes that prevents more than one occurrence of the same tuple (row in SQL) in a relation. A predicate based on a candidate key can uniquely identify a row (such as an employee).

---

# Normalization

1NF
The first normal form says that the tuples (rows) in the relation (table) must be unique and attributes should be atomic. This is a redundant definition of a relation; in other words, if a table truly represents a relation, it is already in first normal form.

You achieve unique rows in SQL by defining a unique key for the table.

Atomicity of attributes is subjective in the same way that the definition of a set is subjective. As an example, should an employee name in an Employees relation be expressed with one attribute (fullname), two (firstname and lastname), or three (firstname, middlename, and lastname)? The answer depends on the application. If the application needs to manipulate the parts of the employee’s name separately (such as for search purposes), it makes sense to break them apart; otherwise, it doesn’t.

2NF

The second normal form involves two rules. One rule is that the data must meet the first normal form. The other rule addresses the relationship between nonkey and candidate-key attributes. For every candidate key, every nonkey attribute has to be fully functionally dependent on the entire candidate key. 


3NF

The third normal form also has two rules. The data must meet the second normal form. Also, all nonkey attributes must be dependent on candidate keys nontransitively. Informally, this rule means that all nonkey attributes must be mutually independent. In other words, one nonkey attribute cannot be dependent on another nonkey attribute.



Informally, 2NF and 3NF are commonly summarized with the sentence, “Every non-key attribute is dependent on the key, the whole key, and nothing but the key—so help me Codd.”


There are higher normal forms beyond Codd’s original first three normal forms that involve compound primary keys and temporal databases


---

# OLTP, DW, DM

online transactional processing (OLTP) and data warehouses (DWs)

DSA: data-staging area

ETL: extract, transform, and load

OLTP for read/write/update
DW or Data Mart for analysis (DW general, DM for specific team)
DSA for moving data from OLTP to DW (ETL)


DW/DM can use star/snowflake schema, which has some duplication of data

---

# Box, Appliance, Cloud

Box - on prem, fully custom

Appliance - on prem, premade/ready to go

Cloud - offsite, managed

Can have multiple instances on one server, e.g. support instance for recreating bugs

---

# SQL DBs

Some DBs created by default with SQL server:

The system databases that the setup program creates include master, Resource, model, tempdb, and msdb. A description of each follows:

Image master The master database holds instance-wide metadata information, the server configuration, information about all databases in the instance, and initialization information.

Image Resource The Resource database is a hidden, read-only database that holds the definitions of all system objects. When you query system objects in a database, they appear to reside in the sys schema of the local database, but in actuality their definitions reside in the Resource database.

Image model The model database is used as a template for new databases. Every new database you create is initially created as a copy of model. So if you want certain objects (such as data types) to appear in all new databases you create, or certain database properties to be configured in a certain way in all new databases, you need to create those objects and configure those properties in the model database. Note that changes you apply to the model database will not affect existing databases—only new databases you create in the future.

Image tempdb The tempdb database is where SQL Server stores temporary data such as work tables, sort and hash table data, row versioning information, and so on. With SQL Server, you can create temporary tables for your own use, and the physical location of those temporary tables is tempdb. Note that this database is destroyed and re-created as a copy of the model database every time you restart the instance of SQL Server.

Image msdb The msdb database is used mainly by a service called SQL Server Agent to store its data. SQL Server Agent is in charge of automation, which includes entities such as jobs, schedules, and alerts. SQL Server Agent is also the service in charge of replication. The msdb database also holds information related to other SQL Server features, such as Database Mail, Service Broker, backups, and more.

---

# Schemas/objects

You can control permissions at the schema level. For example, you can grant a user SELECT permissions on a schema, allowing the user to query data from all objects in that schema. 
You can think of a schema as a container of objects, such as tables, views, stored procedures, and others.

The schema is also a namespace—it is used as a prefix to the object name. For example, suppose you have a table named Orders in a schema named Sales. The schema-qualified object name (also known as the two-part object name) is Sales.Orders. You can refer to objects in other databases by adding the database name as a prefix (three-part object name), and to objects in other instances by adding the instance name as a prefix (four-part object name). If you omit the schema name when referring to an object, SQL Server will apply a process to resolve the schema name, such as checking whether the object exists in the user’s default schema and, if the object doesn’t exist, checking whether it exists in the dbo schema. Microsoft recommends that when you refer to objects in your code you always use the two-part object names.

---

# Coding style

Anything consistent and clean works. Best to use semicolon at the end of statements as MS may be bringing it back.


# Constraints

Can add constraints such as primary key to make rows unique, or unique values

```
ALTER TABLE dbo.Employees
  ADD CONSTRAINT UNQ_Employees_ssn
  UNIQUE(ssn);
```

If doing this with NULLs, need to filter them out when making constraint:

`CREATE UNIQUE INDEX idx_ssn_notnull ON dbo.Employees(ssn) WHERE ssn IS NOT NULL;`

Check constraints can constrain values:

```
ALTER TABLE dbo.Employees
  ADD CONSTRAINT CHK_Employees_salary
  CHECK(salary > 0.00);
```

default values:

```
ALTER TABLE dbo.Orders
  ADD CONSTRAINT DFT_Orders_orderts
  DEFAULT(SYSDATETIME()) FOR orderts;
```

