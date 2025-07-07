

# DatasetProperties


## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**textNormalizationKind** | **TextNormalizationKind** |  |  [optional] |
|**acceptedLineCount** | **Integer** | The number of lines accepted for this data set. |  [optional] [readonly] |
|**rejectedLineCount** | **Integer** | The number of lines rejected for this data set. |  [optional] [readonly] |
|**duration** | **String** | The total duration of the datasets if it contains audio files. The duration is encoded as ISO 8601 duration  (\&quot;PnYnMnDTnHnMnS\&quot;, see https://en.wikipedia.org/wiki/ISO_8601#Durations). |  [optional] [readonly] |
|**email** | **String** | The email address to send email notifications to in case the operation completes.  The value will be removed after successfully sending the email. |  [optional] |
|**error** | [**EntityError**](EntityError.md) |  |  [optional] |



