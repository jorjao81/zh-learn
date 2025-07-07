

# Error

New format which conforms to the new Cognitive Services API guidelines which is available at https://microsoft.sharepoint.com/%3Aw%3A/t/CognitiveServicesPMO/EUoytcrjuJdKpeOKIK_QRC8BPtUYQpKBi8JsWyeDMRsWlQ?e=CPq8ow.  This contains an outer error with error code, message, details, target and an inner error with more descriptive details.

## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**code** | **ErrorCode** |  |  [optional] |
|**details** | [**List&lt;Error&gt;**](Error.md) | Additional supportive details regarding the error and/or expected policies. |  [optional] |
|**message** | **String** | High level error message. |  [optional] |
|**target** | **String** | The source of the error.  For example it would be \&quot;documents\&quot; or \&quot;document id\&quot; in case of invalid document. |  [optional] |
|**innerError** | [**InnerError**](InnerError.md) |  |  [optional] |



