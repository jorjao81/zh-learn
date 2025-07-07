

# EndpointProperties


## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**loggingEnabled** | **Boolean** | A value indicating whether content logging (audio &amp; transcriptions) is being used for a deployment. |  [optional] |
|**timeToLive** | **String** | How long the endpoint will be kept in the system. Once the endpoint reaches the time to live  after completion (successful or failed) it will be automatically deleted. Not setting this value or setting  to 0 will disable automatic deletion. The longest supported duration is 31 days.  The duration is encoded as ISO 8601 duration (\&quot;PnYnMnDTnHnMnS\&quot;, see https://en.wikipedia.org/wiki/ISO_8601#Durations). |  [optional] |
|**email** | **String** | The email address to send email notifications to in case the operation completes.  The value will be removed after successfully sending the email. |  [optional] |
|**error** | [**EntityError**](EntityError.md) |  |  [optional] |



