

# EndpointLinks


## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**restInteractive** | **URI** | The REST endpoint for short requests up to 15 seconds. |  [optional] [readonly] |
|**restConversation** | **URI** | The REST endpoint for requests up to 60 seconds. |  [optional] [readonly] |
|**restDictation** | **URI** | The REST endpoint for requests up to 60 seconds, supporting dictation of punctuation marks. |  [optional] [readonly] |
|**webSocketInteractive** | **URI** | The Speech SDK endpoint for short requests up to 15 seconds with a single final result. |  [optional] [readonly] |
|**webSocketConversation** | **URI** | The Speech SDK endpoint for long requests with multiple final results. |  [optional] [readonly] |
|**webSocketDictation** | **URI** | The Speech SDK endpoint for long requests with multiple final results, supporting dictation of  punctuation marks. |  [optional] [readonly] |
|**logs** | **URI** | The audio and transcription logs for this endpoint.  See operation \&quot;Endpoints_ListLogs\&quot; for more details. |  [optional] [readonly] |



