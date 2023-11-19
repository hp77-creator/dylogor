## Dy-log-or
<img src="img_2.png" alt="drawing" width="50"/>

Dylogor is a tool which stores logs from any microservice and 
can help you query about those logs on the basis of various fields
in the log document

An example of log document that is stored in Dylogor:

```json
{
	"level": "error",
	"message": "Failed to connect to DB",
    "resourceId": "server-1234",
	"timestamp": "2023-09-15T08:00:00Z",
	"traceId": "abc-xyz-123",
    "spanId": "span-456",
    "commit": "5e5342f",
    "metadata": {
        "parentResourceId": "server-0987"
    }
}
```

User should be able to query for logs on the basis of the above fields:

- `level`
- `message`
- `resourceId`
- `timestamp`
- `traceId`
- `spanId`
- `commit`
- `metadata.parentResourceId`

## Architecture

### version 1
![img.png](img.png)
This simple approach will give problem when we scale our system, One
scenario, given that writing to DB and Serving to FE is done by the 
same server, there may arise a condition when server might be called 
by our log-sending service and from our FE

### version 2

![img_1.png](img_1.png)

Using Kafka like streaming service to store logs and directly consuming
from there in BE can be a solution which can help us to serve multiple
users at the same time.

ElasticSearch will allow us to scale horizontally by providing more clusters
we can utilize its master-slave architecture to maintain consistency across different
clusters.