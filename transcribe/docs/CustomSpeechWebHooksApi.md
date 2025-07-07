# CustomSpeechWebHooksApi

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**webHooksCreate**](CustomSpeechWebHooksApi.md#webHooksCreate) | **POST** /webhooks | Creates a new web hook. |
| [**webHooksCreateWithHttpInfo**](CustomSpeechWebHooksApi.md#webHooksCreateWithHttpInfo) | **POST** /webhooks | Creates a new web hook. |
| [**webHooksDelete**](CustomSpeechWebHooksApi.md#webHooksDelete) | **DELETE** /webhooks/{id} | Deletes the web hook identified by the given ID. |
| [**webHooksDeleteWithHttpInfo**](CustomSpeechWebHooksApi.md#webHooksDeleteWithHttpInfo) | **DELETE** /webhooks/{id} | Deletes the web hook identified by the given ID. |
| [**webHooksGet**](CustomSpeechWebHooksApi.md#webHooksGet) | **GET** /webhooks/{id} | Gets the web hook identified by the given ID. |
| [**webHooksGetWithHttpInfo**](CustomSpeechWebHooksApi.md#webHooksGetWithHttpInfo) | **GET** /webhooks/{id} | Gets the web hook identified by the given ID. |
| [**webHooksList**](CustomSpeechWebHooksApi.md#webHooksList) | **GET** /webhooks | Gets the list of web hooks for the authenticated subscription. |
| [**webHooksListWithHttpInfo**](CustomSpeechWebHooksApi.md#webHooksListWithHttpInfo) | **GET** /webhooks | Gets the list of web hooks for the authenticated subscription. |
| [**webHooksPing**](CustomSpeechWebHooksApi.md#webHooksPing) | **POST** /webhooks/{id}:ping | Sends a ping event to the registered URL. |
| [**webHooksPingWithHttpInfo**](CustomSpeechWebHooksApi.md#webHooksPingWithHttpInfo) | **POST** /webhooks/{id}:ping | Sends a ping event to the registered URL. |
| [**webHooksTest**](CustomSpeechWebHooksApi.md#webHooksTest) | **POST** /webhooks/{id}:test | Sends a request for each registered event type to the registered URL. |
| [**webHooksTestWithHttpInfo**](CustomSpeechWebHooksApi.md#webHooksTestWithHttpInfo) | **POST** /webhooks/{id}:test | Sends a request for each registered event type to the registered URL. |
| [**webHooksUpdate**](CustomSpeechWebHooksApi.md#webHooksUpdate) | **PATCH** /webhooks/{id} | Updates the web hook identified by the given ID. |
| [**webHooksUpdateWithHttpInfo**](CustomSpeechWebHooksApi.md#webHooksUpdateWithHttpInfo) | **PATCH** /webhooks/{id} | Updates the web hook identified by the given ID. |



## webHooksCreate

> WebHook webHooksCreate(webHook)

Creates a new web hook.

If the property secret in the configuration is present and contains a non-empty string, it will be used to create a SHA256 hash of the payload with  the secret as HMAC key. This hash will be set as X-MicrosoftSpeechServices-Signature header when calling back into the registered URL.                When calling back into the registered URL, the request will contain a X-MicrosoftSpeechServices-Event header containing one of the registered event  types. There will be one request per registered event type.                After successfully registering the web hook, it will not be usable until a challenge/response is completed. To do this, a request with the event type  challenge will be made with a query parameter called validationToken. Respond to the challenge with a 200 OK containing the value of the validationToken  query parameter as the response body. When the challenge/response is successfully completed, the web hook will begin receiving events.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechWebHooksApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("http://localhost");
        
        // Configure API key authorization: api_key
        ApiKeyAuth api_key = (ApiKeyAuth) defaultClient.getAuthentication("api_key");
        api_key.setApiKey("YOUR API KEY");
        // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
        //api_key.setApiKeyPrefix("Token");

        // Configure API key authorization: token
        ApiKeyAuth token = (ApiKeyAuth) defaultClient.getAuthentication("token");
        token.setApiKey("YOUR API KEY");
        // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
        //token.setApiKeyPrefix("Token");

        CustomSpeechWebHooksApi apiInstance = new CustomSpeechWebHooksApi(defaultClient);
        WebHook webHook = new WebHook(); // WebHook | The details of the new web hook.
        try {
            WebHook result = apiInstance.webHooksCreate(webHook);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechWebHooksApi#webHooksCreate");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Reason: " + e.getResponseBody());
            System.err.println("Response headers: " + e.getResponseHeaders());
            e.printStackTrace();
        }
    }
}
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **webHook** | [**WebHook**](WebHook.md)| The details of the new web hook. | |

### Return type

[**WebHook**](WebHook.md)


### Authorization

[api_key](../README.md#api_key), [token](../README.md#token)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **201** | The response contains information about the entity as payload and its location as header. |  * Location - The location of the created resource. <br>  |
| **0** | An error occurred. |  -  |

## webHooksCreateWithHttpInfo

> ApiResponse<WebHook> webHooksCreate webHooksCreateWithHttpInfo(webHook)

Creates a new web hook.

If the property secret in the configuration is present and contains a non-empty string, it will be used to create a SHA256 hash of the payload with  the secret as HMAC key. This hash will be set as X-MicrosoftSpeechServices-Signature header when calling back into the registered URL.                When calling back into the registered URL, the request will contain a X-MicrosoftSpeechServices-Event header containing one of the registered event  types. There will be one request per registered event type.                After successfully registering the web hook, it will not be usable until a challenge/response is completed. To do this, a request with the event type  challenge will be made with a query parameter called validationToken. Respond to the challenge with a 200 OK containing the value of the validationToken  query parameter as the response body. When the challenge/response is successfully completed, the web hook will begin receiving events.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechWebHooksApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("http://localhost");
        
        // Configure API key authorization: api_key
        ApiKeyAuth api_key = (ApiKeyAuth) defaultClient.getAuthentication("api_key");
        api_key.setApiKey("YOUR API KEY");
        // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
        //api_key.setApiKeyPrefix("Token");

        // Configure API key authorization: token
        ApiKeyAuth token = (ApiKeyAuth) defaultClient.getAuthentication("token");
        token.setApiKey("YOUR API KEY");
        // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
        //token.setApiKeyPrefix("Token");

        CustomSpeechWebHooksApi apiInstance = new CustomSpeechWebHooksApi(defaultClient);
        WebHook webHook = new WebHook(); // WebHook | The details of the new web hook.
        try {
            ApiResponse<WebHook> response = apiInstance.webHooksCreateWithHttpInfo(webHook);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechWebHooksApi#webHooksCreate");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Response headers: " + e.getResponseHeaders());
            System.err.println("Reason: " + e.getResponseBody());
            e.printStackTrace();
        }
    }
}
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **webHook** | [**WebHook**](WebHook.md)| The details of the new web hook. | |

### Return type

ApiResponse<[**WebHook**](WebHook.md)>


### Authorization

[api_key](../README.md#api_key), [token](../README.md#token)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **201** | The response contains information about the entity as payload and its location as header. |  * Location - The location of the created resource. <br>  |
| **0** | An error occurred. |  -  |


## webHooksDelete

> void webHooksDelete(id)

Deletes the web hook identified by the given ID.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechWebHooksApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("http://localhost");
        
        // Configure API key authorization: api_key
        ApiKeyAuth api_key = (ApiKeyAuth) defaultClient.getAuthentication("api_key");
        api_key.setApiKey("YOUR API KEY");
        // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
        //api_key.setApiKeyPrefix("Token");

        // Configure API key authorization: token
        ApiKeyAuth token = (ApiKeyAuth) defaultClient.getAuthentication("token");
        token.setApiKey("YOUR API KEY");
        // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
        //token.setApiKeyPrefix("Token");

        CustomSpeechWebHooksApi apiInstance = new CustomSpeechWebHooksApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the web hook.
        try {
            apiInstance.webHooksDelete(id);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechWebHooksApi#webHooksDelete");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Reason: " + e.getResponseBody());
            System.err.println("Response headers: " + e.getResponseHeaders());
            e.printStackTrace();
        }
    }
}
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **id** | **UUID**| The identifier of the web hook. | |

### Return type


null (empty response body)

### Authorization

[api_key](../README.md#api_key), [token](../README.md#token)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **204** | The web hook was successfully deleted. |  -  |
| **0** | An error occurred. |  -  |

## webHooksDeleteWithHttpInfo

> ApiResponse<Void> webHooksDelete webHooksDeleteWithHttpInfo(id)

Deletes the web hook identified by the given ID.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechWebHooksApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("http://localhost");
        
        // Configure API key authorization: api_key
        ApiKeyAuth api_key = (ApiKeyAuth) defaultClient.getAuthentication("api_key");
        api_key.setApiKey("YOUR API KEY");
        // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
        //api_key.setApiKeyPrefix("Token");

        // Configure API key authorization: token
        ApiKeyAuth token = (ApiKeyAuth) defaultClient.getAuthentication("token");
        token.setApiKey("YOUR API KEY");
        // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
        //token.setApiKeyPrefix("Token");

        CustomSpeechWebHooksApi apiInstance = new CustomSpeechWebHooksApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the web hook.
        try {
            ApiResponse<Void> response = apiInstance.webHooksDeleteWithHttpInfo(id);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechWebHooksApi#webHooksDelete");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Response headers: " + e.getResponseHeaders());
            System.err.println("Reason: " + e.getResponseBody());
            e.printStackTrace();
        }
    }
}
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **id** | **UUID**| The identifier of the web hook. | |

### Return type


ApiResponse<Void>

### Authorization

[api_key](../README.md#api_key), [token](../README.md#token)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **204** | The web hook was successfully deleted. |  -  |
| **0** | An error occurred. |  -  |


## webHooksGet

> WebHook webHooksGet(id)

Gets the web hook identified by the given ID.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechWebHooksApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("http://localhost");
        
        // Configure API key authorization: api_key
        ApiKeyAuth api_key = (ApiKeyAuth) defaultClient.getAuthentication("api_key");
        api_key.setApiKey("YOUR API KEY");
        // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
        //api_key.setApiKeyPrefix("Token");

        // Configure API key authorization: token
        ApiKeyAuth token = (ApiKeyAuth) defaultClient.getAuthentication("token");
        token.setApiKey("YOUR API KEY");
        // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
        //token.setApiKeyPrefix("Token");

        CustomSpeechWebHooksApi apiInstance = new CustomSpeechWebHooksApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the web hook.
        try {
            WebHook result = apiInstance.webHooksGet(id);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechWebHooksApi#webHooksGet");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Reason: " + e.getResponseBody());
            System.err.println("Response headers: " + e.getResponseHeaders());
            e.printStackTrace();
        }
    }
}
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **id** | **UUID**| The identifier of the web hook. | |

### Return type

[**WebHook**](WebHook.md)


### Authorization

[api_key](../README.md#api_key), [token](../README.md#token)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | OK |  * Retry-After - The minimum number of seconds to wait before accessing the resource created in this operation. <br>  |
| **0** | An error occurred. |  -  |

## webHooksGetWithHttpInfo

> ApiResponse<WebHook> webHooksGet webHooksGetWithHttpInfo(id)

Gets the web hook identified by the given ID.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechWebHooksApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("http://localhost");
        
        // Configure API key authorization: api_key
        ApiKeyAuth api_key = (ApiKeyAuth) defaultClient.getAuthentication("api_key");
        api_key.setApiKey("YOUR API KEY");
        // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
        //api_key.setApiKeyPrefix("Token");

        // Configure API key authorization: token
        ApiKeyAuth token = (ApiKeyAuth) defaultClient.getAuthentication("token");
        token.setApiKey("YOUR API KEY");
        // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
        //token.setApiKeyPrefix("Token");

        CustomSpeechWebHooksApi apiInstance = new CustomSpeechWebHooksApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the web hook.
        try {
            ApiResponse<WebHook> response = apiInstance.webHooksGetWithHttpInfo(id);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechWebHooksApi#webHooksGet");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Response headers: " + e.getResponseHeaders());
            System.err.println("Reason: " + e.getResponseBody());
            e.printStackTrace();
        }
    }
}
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **id** | **UUID**| The identifier of the web hook. | |

### Return type

ApiResponse<[**WebHook**](WebHook.md)>


### Authorization

[api_key](../README.md#api_key), [token](../README.md#token)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | OK |  * Retry-After - The minimum number of seconds to wait before accessing the resource created in this operation. <br>  |
| **0** | An error occurred. |  -  |


## webHooksList

> PaginatedWebHooks webHooksList(skip, top, filter)

Gets the list of web hooks for the authenticated subscription.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechWebHooksApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("http://localhost");
        
        // Configure API key authorization: api_key
        ApiKeyAuth api_key = (ApiKeyAuth) defaultClient.getAuthentication("api_key");
        api_key.setApiKey("YOUR API KEY");
        // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
        //api_key.setApiKeyPrefix("Token");

        // Configure API key authorization: token
        ApiKeyAuth token = (ApiKeyAuth) defaultClient.getAuthentication("token");
        token.setApiKey("YOUR API KEY");
        // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
        //token.setApiKeyPrefix("Token");

        CustomSpeechWebHooksApi apiInstance = new CustomSpeechWebHooksApi(defaultClient);
        Integer skip = 56; // Integer | Number of datasets that will be skipped.
        Integer top = 56; // Integer | Number of datasets that will be included after skipping.
        String filter = "filter_example"; // String | A filtering expression for selecting a subset of the available hooks.              Supported properties: displayName, description, createdDateTime, lastActionDateTime, status and webUrl.              - Operators:                - eq, ne are supported for all properties.                - gt, ge, lt, le are supported for createdDateTime and lastActionDateTime.                - and, or, not are supported.              - Example:                filter=displayName eq 'test'
        try {
            PaginatedWebHooks result = apiInstance.webHooksList(skip, top, filter);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechWebHooksApi#webHooksList");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Reason: " + e.getResponseBody());
            System.err.println("Response headers: " + e.getResponseHeaders());
            e.printStackTrace();
        }
    }
}
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **skip** | **Integer**| Number of datasets that will be skipped. | [optional] |
| **top** | **Integer**| Number of datasets that will be included after skipping. | [optional] |
| **filter** | **String**| A filtering expression for selecting a subset of the available hooks.              Supported properties: displayName, description, createdDateTime, lastActionDateTime, status and webUrl.              - Operators:                - eq, ne are supported for all properties.                - gt, ge, lt, le are supported for createdDateTime and lastActionDateTime.                - and, or, not are supported.              - Example:                filter&#x3D;displayName eq &#39;test&#39; | [optional] |

### Return type

[**PaginatedWebHooks**](PaginatedWebHooks.md)


### Authorization

[api_key](../README.md#api_key), [token](../README.md#token)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | OK |  * Retry-After - The minimum number of seconds to wait before accessing the resource created in this operation. <br>  |
| **0** | An error occurred. |  -  |

## webHooksListWithHttpInfo

> ApiResponse<PaginatedWebHooks> webHooksList webHooksListWithHttpInfo(skip, top, filter)

Gets the list of web hooks for the authenticated subscription.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechWebHooksApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("http://localhost");
        
        // Configure API key authorization: api_key
        ApiKeyAuth api_key = (ApiKeyAuth) defaultClient.getAuthentication("api_key");
        api_key.setApiKey("YOUR API KEY");
        // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
        //api_key.setApiKeyPrefix("Token");

        // Configure API key authorization: token
        ApiKeyAuth token = (ApiKeyAuth) defaultClient.getAuthentication("token");
        token.setApiKey("YOUR API KEY");
        // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
        //token.setApiKeyPrefix("Token");

        CustomSpeechWebHooksApi apiInstance = new CustomSpeechWebHooksApi(defaultClient);
        Integer skip = 56; // Integer | Number of datasets that will be skipped.
        Integer top = 56; // Integer | Number of datasets that will be included after skipping.
        String filter = "filter_example"; // String | A filtering expression for selecting a subset of the available hooks.              Supported properties: displayName, description, createdDateTime, lastActionDateTime, status and webUrl.              - Operators:                - eq, ne are supported for all properties.                - gt, ge, lt, le are supported for createdDateTime and lastActionDateTime.                - and, or, not are supported.              - Example:                filter=displayName eq 'test'
        try {
            ApiResponse<PaginatedWebHooks> response = apiInstance.webHooksListWithHttpInfo(skip, top, filter);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechWebHooksApi#webHooksList");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Response headers: " + e.getResponseHeaders());
            System.err.println("Reason: " + e.getResponseBody());
            e.printStackTrace();
        }
    }
}
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **skip** | **Integer**| Number of datasets that will be skipped. | [optional] |
| **top** | **Integer**| Number of datasets that will be included after skipping. | [optional] |
| **filter** | **String**| A filtering expression for selecting a subset of the available hooks.              Supported properties: displayName, description, createdDateTime, lastActionDateTime, status and webUrl.              - Operators:                - eq, ne are supported for all properties.                - gt, ge, lt, le are supported for createdDateTime and lastActionDateTime.                - and, or, not are supported.              - Example:                filter&#x3D;displayName eq &#39;test&#39; | [optional] |

### Return type

ApiResponse<[**PaginatedWebHooks**](PaginatedWebHooks.md)>


### Authorization

[api_key](../README.md#api_key), [token](../README.md#token)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | OK |  * Retry-After - The minimum number of seconds to wait before accessing the resource created in this operation. <br>  |
| **0** | An error occurred. |  -  |


## webHooksPing

> void webHooksPing(id)

Sends a ping event to the registered URL.

The request body of the POST request sent to the registered web hook URL is of the same shape as in the GET request for a specific hook.  The Swagger Schema ID of the model is WebHookV3.                The request will contain a X-MicrosoftSpeechServices-Event header with the value ping. If the web hook was registered with  a secret it will contain a X-MicrosoftSpeechServices-Signature header with an SHA256 hash of the payload with  the secret as HMAC key. The hash is base64 encoded.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechWebHooksApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("http://localhost");
        
        // Configure API key authorization: api_key
        ApiKeyAuth api_key = (ApiKeyAuth) defaultClient.getAuthentication("api_key");
        api_key.setApiKey("YOUR API KEY");
        // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
        //api_key.setApiKeyPrefix("Token");

        // Configure API key authorization: token
        ApiKeyAuth token = (ApiKeyAuth) defaultClient.getAuthentication("token");
        token.setApiKey("YOUR API KEY");
        // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
        //token.setApiKeyPrefix("Token");

        CustomSpeechWebHooksApi apiInstance = new CustomSpeechWebHooksApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the web hook to ping.
        try {
            apiInstance.webHooksPing(id);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechWebHooksApi#webHooksPing");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Reason: " + e.getResponseBody());
            System.err.println("Response headers: " + e.getResponseHeaders());
            e.printStackTrace();
        }
    }
}
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **id** | **UUID**| The identifier of the web hook to ping. | |

### Return type


null (empty response body)

### Authorization

[api_key](../README.md#api_key), [token](../README.md#token)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **202** | Started trying to send a ping request to the web hook. |  * Retry-After - The minimum number of seconds to wait before accessing the resource created in this operation. <br>  |
| **0** | An error occurred. |  -  |

## webHooksPingWithHttpInfo

> ApiResponse<Void> webHooksPing webHooksPingWithHttpInfo(id)

Sends a ping event to the registered URL.

The request body of the POST request sent to the registered web hook URL is of the same shape as in the GET request for a specific hook.  The Swagger Schema ID of the model is WebHookV3.                The request will contain a X-MicrosoftSpeechServices-Event header with the value ping. If the web hook was registered with  a secret it will contain a X-MicrosoftSpeechServices-Signature header with an SHA256 hash of the payload with  the secret as HMAC key. The hash is base64 encoded.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechWebHooksApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("http://localhost");
        
        // Configure API key authorization: api_key
        ApiKeyAuth api_key = (ApiKeyAuth) defaultClient.getAuthentication("api_key");
        api_key.setApiKey("YOUR API KEY");
        // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
        //api_key.setApiKeyPrefix("Token");

        // Configure API key authorization: token
        ApiKeyAuth token = (ApiKeyAuth) defaultClient.getAuthentication("token");
        token.setApiKey("YOUR API KEY");
        // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
        //token.setApiKeyPrefix("Token");

        CustomSpeechWebHooksApi apiInstance = new CustomSpeechWebHooksApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the web hook to ping.
        try {
            ApiResponse<Void> response = apiInstance.webHooksPingWithHttpInfo(id);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechWebHooksApi#webHooksPing");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Response headers: " + e.getResponseHeaders());
            System.err.println("Reason: " + e.getResponseBody());
            e.printStackTrace();
        }
    }
}
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **id** | **UUID**| The identifier of the web hook to ping. | |

### Return type


ApiResponse<Void>

### Authorization

[api_key](../README.md#api_key), [token](../README.md#token)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **202** | Started trying to send a ping request to the web hook. |  * Retry-After - The minimum number of seconds to wait before accessing the resource created in this operation. <br>  |
| **0** | An error occurred. |  -  |


## webHooksTest

> void webHooksTest(id)

Sends a request for each registered event type to the registered URL.

The payload will be generated from the last entity that would have invoked the web hook. If no entity is present for none of the registered event types,  the POST will respond with 204. If a test request can be made, it will respond with 200.  The request will contain a X-MicrosoftSpeechServices-Event header with the respective registered event type.  If the web hook was registered with a secret it will contain a X-MicrosoftSpeechServices-Signature header with an SHA256 hash of the payload with  the secret as HMAC key. The hash is base64 encoded.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechWebHooksApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("http://localhost");
        
        // Configure API key authorization: api_key
        ApiKeyAuth api_key = (ApiKeyAuth) defaultClient.getAuthentication("api_key");
        api_key.setApiKey("YOUR API KEY");
        // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
        //api_key.setApiKeyPrefix("Token");

        // Configure API key authorization: token
        ApiKeyAuth token = (ApiKeyAuth) defaultClient.getAuthentication("token");
        token.setApiKey("YOUR API KEY");
        // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
        //token.setApiKeyPrefix("Token");

        CustomSpeechWebHooksApi apiInstance = new CustomSpeechWebHooksApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the web hook to ping.
        try {
            apiInstance.webHooksTest(id);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechWebHooksApi#webHooksTest");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Reason: " + e.getResponseBody());
            System.err.println("Response headers: " + e.getResponseHeaders());
            e.printStackTrace();
        }
    }
}
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **id** | **UUID**| The identifier of the web hook to ping. | |

### Return type


null (empty response body)

### Authorization

[api_key](../README.md#api_key), [token](../README.md#token)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **202** | A test request with the last entity is sent to the registered web hook. |  * Retry-After - The minimum number of seconds to wait before accessing the resource created in this operation. <br>  |
| **204** | No entity could be found for any event type, so no test request is sent to the registered web hook. |  -  |
| **0** | An error occurred. |  -  |

## webHooksTestWithHttpInfo

> ApiResponse<Void> webHooksTest webHooksTestWithHttpInfo(id)

Sends a request for each registered event type to the registered URL.

The payload will be generated from the last entity that would have invoked the web hook. If no entity is present for none of the registered event types,  the POST will respond with 204. If a test request can be made, it will respond with 200.  The request will contain a X-MicrosoftSpeechServices-Event header with the respective registered event type.  If the web hook was registered with a secret it will contain a X-MicrosoftSpeechServices-Signature header with an SHA256 hash of the payload with  the secret as HMAC key. The hash is base64 encoded.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechWebHooksApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("http://localhost");
        
        // Configure API key authorization: api_key
        ApiKeyAuth api_key = (ApiKeyAuth) defaultClient.getAuthentication("api_key");
        api_key.setApiKey("YOUR API KEY");
        // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
        //api_key.setApiKeyPrefix("Token");

        // Configure API key authorization: token
        ApiKeyAuth token = (ApiKeyAuth) defaultClient.getAuthentication("token");
        token.setApiKey("YOUR API KEY");
        // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
        //token.setApiKeyPrefix("Token");

        CustomSpeechWebHooksApi apiInstance = new CustomSpeechWebHooksApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the web hook to ping.
        try {
            ApiResponse<Void> response = apiInstance.webHooksTestWithHttpInfo(id);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechWebHooksApi#webHooksTest");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Response headers: " + e.getResponseHeaders());
            System.err.println("Reason: " + e.getResponseBody());
            e.printStackTrace();
        }
    }
}
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **id** | **UUID**| The identifier of the web hook to ping. | |

### Return type


ApiResponse<Void>

### Authorization

[api_key](../README.md#api_key), [token](../README.md#token)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **202** | A test request with the last entity is sent to the registered web hook. |  * Retry-After - The minimum number of seconds to wait before accessing the resource created in this operation. <br>  |
| **204** | No entity could be found for any event type, so no test request is sent to the registered web hook. |  -  |
| **0** | An error occurred. |  -  |


## webHooksUpdate

> WebHook webHooksUpdate(id, webHookUpdate)

Updates the web hook identified by the given ID.

If the property secret in the configuration is omitted or contains an empty string, future callbacks won&#39;t contain X-MicrosoftSpeechServices-Signature  headers. If the property contains a non-empty string, it will be used to create a SHA256 hash of the payload with the secret as HMAC key. This hash  will be set as X-MicrosoftSpeechServices-Signature header when calling back into the registered URL.                If the URL changes,  the web hook will stop receiving events until a  challenge/response is completed. To do this, a request with the event type challenge will be made with a query parameter called validationToken.  Respond to the challenge with a 200 OK containing the value of the validationToken query parameter as the response body. When the challenge/response  is successfully completed, the web hook will begin receiving events.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechWebHooksApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("http://localhost");
        
        // Configure API key authorization: api_key
        ApiKeyAuth api_key = (ApiKeyAuth) defaultClient.getAuthentication("api_key");
        api_key.setApiKey("YOUR API KEY");
        // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
        //api_key.setApiKeyPrefix("Token");

        // Configure API key authorization: token
        ApiKeyAuth token = (ApiKeyAuth) defaultClient.getAuthentication("token");
        token.setApiKey("YOUR API KEY");
        // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
        //token.setApiKeyPrefix("Token");

        CustomSpeechWebHooksApi apiInstance = new CustomSpeechWebHooksApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the web hook.
        WebHookUpdate webHookUpdate = new WebHookUpdate(); // WebHookUpdate | The updated values for the web hook.
        try {
            WebHook result = apiInstance.webHooksUpdate(id, webHookUpdate);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechWebHooksApi#webHooksUpdate");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Reason: " + e.getResponseBody());
            System.err.println("Response headers: " + e.getResponseHeaders());
            e.printStackTrace();
        }
    }
}
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **id** | **UUID**| The identifier of the web hook. | |
| **webHookUpdate** | [**WebHookUpdate**](WebHookUpdate.md)| The updated values for the web hook. | |

### Return type

[**WebHook**](WebHook.md)


### Authorization

[api_key](../README.md#api_key), [token](../README.md#token)

### HTTP request headers

- **Content-Type**: application/json, application/merge-patch+json
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | OK |  * Retry-After - The minimum number of seconds to wait before accessing the resource created in this operation. <br>  |
| **0** | An error occurred. |  -  |

## webHooksUpdateWithHttpInfo

> ApiResponse<WebHook> webHooksUpdate webHooksUpdateWithHttpInfo(id, webHookUpdate)

Updates the web hook identified by the given ID.

If the property secret in the configuration is omitted or contains an empty string, future callbacks won&#39;t contain X-MicrosoftSpeechServices-Signature  headers. If the property contains a non-empty string, it will be used to create a SHA256 hash of the payload with the secret as HMAC key. This hash  will be set as X-MicrosoftSpeechServices-Signature header when calling back into the registered URL.                If the URL changes,  the web hook will stop receiving events until a  challenge/response is completed. To do this, a request with the event type challenge will be made with a query parameter called validationToken.  Respond to the challenge with a 200 OK containing the value of the validationToken query parameter as the response body. When the challenge/response  is successfully completed, the web hook will begin receiving events.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechWebHooksApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("http://localhost");
        
        // Configure API key authorization: api_key
        ApiKeyAuth api_key = (ApiKeyAuth) defaultClient.getAuthentication("api_key");
        api_key.setApiKey("YOUR API KEY");
        // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
        //api_key.setApiKeyPrefix("Token");

        // Configure API key authorization: token
        ApiKeyAuth token = (ApiKeyAuth) defaultClient.getAuthentication("token");
        token.setApiKey("YOUR API KEY");
        // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
        //token.setApiKeyPrefix("Token");

        CustomSpeechWebHooksApi apiInstance = new CustomSpeechWebHooksApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the web hook.
        WebHookUpdate webHookUpdate = new WebHookUpdate(); // WebHookUpdate | The updated values for the web hook.
        try {
            ApiResponse<WebHook> response = apiInstance.webHooksUpdateWithHttpInfo(id, webHookUpdate);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechWebHooksApi#webHooksUpdate");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Response headers: " + e.getResponseHeaders());
            System.err.println("Reason: " + e.getResponseBody());
            e.printStackTrace();
        }
    }
}
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **id** | **UUID**| The identifier of the web hook. | |
| **webHookUpdate** | [**WebHookUpdate**](WebHookUpdate.md)| The updated values for the web hook. | |

### Return type

ApiResponse<[**WebHook**](WebHook.md)>


### Authorization

[api_key](../README.md#api_key), [token](../README.md#token)

### HTTP request headers

- **Content-Type**: application/json, application/merge-patch+json
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | OK |  * Retry-After - The minimum number of seconds to wait before accessing the resource created in this operation. <br>  |
| **0** | An error occurred. |  -  |

