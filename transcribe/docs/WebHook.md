

# WebHook


## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**webUrl** | **URI** | The registered URL that will be used to send the POST requests for the registered events to. |  |
|**links** | [**WebHookLinks**](WebHookLinks.md) |  |  [optional] |
|**properties** | [**WebHookProperties**](WebHookProperties.md) |  |  [optional] |
|**self** | **URI** | The location of this entity. |  [optional] [readonly] |
|**displayName** | **String** | The display name of the object. |  |
|**description** | **String** | The description of the object. |  [optional] |
|**events** | [**WebHookEvents**](WebHookEvents.md) |  |  |
|**createdDateTime** | **OffsetDateTime** | The time-stamp when the object was created.  The time stamp is encoded as ISO 8601 date and time format  (\&quot;YYYY-MM-DDThh:mm:ssZ\&quot;, see https://en.wikipedia.org/wiki/ISO_8601#Combined_date_and_time_representations). |  [optional] [readonly] |
|**lastActionDateTime** | **OffsetDateTime** | The time-stamp when the current status was entered.  The time stamp is encoded as ISO 8601 date and time format  (\&quot;YYYY-MM-DDThh:mm:ssZ\&quot;, see https://en.wikipedia.org/wiki/ISO_8601#Combined_date_and_time_representations). |  [optional] [readonly] |
|**status** | **Status** |  |  [optional] |
|**customProperties** | **Map&lt;String, String&gt;** | The custom properties of this entity. The maximum allowed key length is 64 characters, the maximum  allowed value length is 256 characters and the count of allowed entries is 10. |  [optional] |



