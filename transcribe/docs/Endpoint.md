

# Endpoint


## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**links** | [**EndpointLinks**](EndpointLinks.md) |  |  [optional] |
|**properties** | [**EndpointProperties**](EndpointProperties.md) |  |  [optional] |
|**self** | **URI** | The location of this entity. |  [optional] [readonly] |
|**displayName** | **String** | The display name of the object. |  |
|**description** | **String** | The description of the object. |  [optional] |
|**text** | **String** | The text used to adapt a language model for this endpoint. |  [optional] |
|**model** | [**EntityReference**](EntityReference.md) |  |  [optional] |
|**locale** | **String** | The locale of the contained data. |  |
|**customProperties** | **Map&lt;String, String&gt;** | The custom properties of this entity. The maximum allowed key length is 64 characters, the maximum  allowed value length is 256 characters and the count of allowed entries is 10. |  [optional] |
|**lastActionDateTime** | **OffsetDateTime** | The time-stamp when the current status was entered.  The time stamp is encoded as ISO 8601 date and time format  (\&quot;YYYY-MM-DDThh:mm:ssZ\&quot;, see https://en.wikipedia.org/wiki/ISO_8601#Combined_date_and_time_representations). |  [optional] [readonly] |
|**status** | **Status** |  |  [optional] |
|**createdDateTime** | **OffsetDateTime** | The time-stamp when the object was created.  The time stamp is encoded as ISO 8601 date and time format  (\&quot;YYYY-MM-DDThh:mm:ssZ\&quot;, see https://en.wikipedia.org/wiki/ISO_8601#Combined_date_and_time_representations). |  [optional] [readonly] |
|**project** | [**EntityReference**](EntityReference.md) |  |  [optional] |



