

# WebHookProperties


## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**error** | [**EntityError**](EntityError.md) |  |  [optional] |
|**apiVersion** | **String** | The API version the web hook was created in. This defines the shape of the payload in the callbacks.  If the payload type is not supported anymore, because the shape changed and the API version using it is removed (after deprecation),  the web hook will be disabled. |  [optional] [readonly] |
|**secret** | **String** | A secret that will be used to create a SHA256 hash of the payload with the secret as HMAC key.  This hash will be set as X-MicrosoftSpeechServices-Signature header when calling back into the registered URL. |  [optional] |



