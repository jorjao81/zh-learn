

# Operation


## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**id** | **UUID** | The identifier of this Operation. |  |
|**result** | [**OperationResult**](OperationResult.md) |  |  [optional] |
|**error** | [**EntityError**](EntityError.md) |  |  [optional] |
|**self** | **URI** | The location of this entity. |  [optional] [readonly] |
|**lastActionDateTime** | **OffsetDateTime** | The time-stamp when the current status was entered.  The time stamp is encoded as ISO 8601 date and time format  (\&quot;YYYY-MM-DDThh:mm:ssZ\&quot;, see https://en.wikipedia.org/wiki/ISO_8601#Combined_date_and_time_representations). |  [optional] [readonly] |
|**status** | **Status** |  |  [optional] |
|**createdDateTime** | **OffsetDateTime** | The time-stamp when the object was created.  The time stamp is encoded as ISO 8601 date and time format  (\&quot;YYYY-MM-DDThh:mm:ssZ\&quot;, see https://en.wikipedia.org/wiki/ISO_8601#Combined_date_and_time_representations). |  [optional] [readonly] |



