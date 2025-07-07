

# InnerError

New Inner Error format which conforms to Cognitive Services API Guidelines which is available at https://microsoft.sharepoint.com/%3Aw%3A/t/CognitiveServicesPMO/EUoytcrjuJdKpeOKIK_QRC8BPtUYQpKBi8JsWyeDMRsWlQ?e=CPq8ow.  This contains required properties ErrorCode, message and optional properties target, details(key value pair), inner error(this can be nested).

## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**code** | **DetailedErrorCode** |  |  [optional] |
|**details** | **Map&lt;String, String&gt;** | Additional supportive details regarding the error and/or expected policies. |  [optional] |
|**message** | **String** | High level error message. |  [optional] |
|**target** | **String** | The source of the error.  For example it would be \&quot;documents\&quot; or \&quot;document id\&quot; in case of invalid document. |  [optional] |
|**innerError** | [**InnerError**](InnerError.md) |  |  [optional] |



