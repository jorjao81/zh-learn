# CustomSpeechEndpointsApi

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**endpointsCreate**](CustomSpeechEndpointsApi.md#endpointsCreate) | **POST** /endpoints | Creates a new endpoint. |
| [**endpointsCreateWithHttpInfo**](CustomSpeechEndpointsApi.md#endpointsCreateWithHttpInfo) | **POST** /endpoints | Creates a new endpoint. |
| [**endpointsDelete**](CustomSpeechEndpointsApi.md#endpointsDelete) | **DELETE** /endpoints/{id} | Deletes the endpoint identified by the given ID. |
| [**endpointsDeleteWithHttpInfo**](CustomSpeechEndpointsApi.md#endpointsDeleteWithHttpInfo) | **DELETE** /endpoints/{id} | Deletes the endpoint identified by the given ID. |
| [**endpointsDeleteBaseModelLog**](CustomSpeechEndpointsApi.md#endpointsDeleteBaseModelLog) | **DELETE** /endpoints/base/{locale}/files/logs/{logId} | Deletes one audio or transcription log that have been stored when using the default base model of a given language. |
| [**endpointsDeleteBaseModelLogWithHttpInfo**](CustomSpeechEndpointsApi.md#endpointsDeleteBaseModelLogWithHttpInfo) | **DELETE** /endpoints/base/{locale}/files/logs/{logId} | Deletes one audio or transcription log that have been stored when using the default base model of a given language. |
| [**endpointsDeleteBaseModelLogs**](CustomSpeechEndpointsApi.md#endpointsDeleteBaseModelLogs) | **DELETE** /endpoints/base/{locale}/files/logs | Deletes the specified audio and transcription logs that have been stored when using the default base model of a given language. It deletes all logs before (and including) a specific day. |
| [**endpointsDeleteBaseModelLogsWithHttpInfo**](CustomSpeechEndpointsApi.md#endpointsDeleteBaseModelLogsWithHttpInfo) | **DELETE** /endpoints/base/{locale}/files/logs | Deletes the specified audio and transcription logs that have been stored when using the default base model of a given language. It deletes all logs before (and including) a specific day. |
| [**endpointsDeleteLog**](CustomSpeechEndpointsApi.md#endpointsDeleteLog) | **DELETE** /endpoints/{id}/files/logs/{logId} | Deletes one audio or transcription log that have been stored for a given endpoint. |
| [**endpointsDeleteLogWithHttpInfo**](CustomSpeechEndpointsApi.md#endpointsDeleteLogWithHttpInfo) | **DELETE** /endpoints/{id}/files/logs/{logId} | Deletes one audio or transcription log that have been stored for a given endpoint. |
| [**endpointsDeleteLogs**](CustomSpeechEndpointsApi.md#endpointsDeleteLogs) | **DELETE** /endpoints/{id}/files/logs | Deletes the specified audio and transcription logs that have been stored for a given endpoint. It deletes all logs before (and including) a specific day. |
| [**endpointsDeleteLogsWithHttpInfo**](CustomSpeechEndpointsApi.md#endpointsDeleteLogsWithHttpInfo) | **DELETE** /endpoints/{id}/files/logs | Deletes the specified audio and transcription logs that have been stored for a given endpoint. It deletes all logs before (and including) a specific day. |
| [**endpointsGet**](CustomSpeechEndpointsApi.md#endpointsGet) | **GET** /endpoints/{id} | Gets the endpoint identified by the given ID. |
| [**endpointsGetWithHttpInfo**](CustomSpeechEndpointsApi.md#endpointsGetWithHttpInfo) | **GET** /endpoints/{id} | Gets the endpoint identified by the given ID. |
| [**endpointsGetBaseModelLog**](CustomSpeechEndpointsApi.md#endpointsGetBaseModelLog) | **GET** /endpoints/base/{locale}/files/logs/{logId} | Gets a specific audio or transcription log for the default base model in a given language. |
| [**endpointsGetBaseModelLogWithHttpInfo**](CustomSpeechEndpointsApi.md#endpointsGetBaseModelLogWithHttpInfo) | **GET** /endpoints/base/{locale}/files/logs/{logId} | Gets a specific audio or transcription log for the default base model in a given language. |
| [**endpointsGetLog**](CustomSpeechEndpointsApi.md#endpointsGetLog) | **GET** /endpoints/{id}/files/logs/{logId} | Gets a specific audio or transcription log for a given endpoint. |
| [**endpointsGetLogWithHttpInfo**](CustomSpeechEndpointsApi.md#endpointsGetLogWithHttpInfo) | **GET** /endpoints/{id}/files/logs/{logId} | Gets a specific audio or transcription log for a given endpoint. |
| [**endpointsList**](CustomSpeechEndpointsApi.md#endpointsList) | **GET** /endpoints | Gets the list of endpoints for the authenticated subscription. |
| [**endpointsListWithHttpInfo**](CustomSpeechEndpointsApi.md#endpointsListWithHttpInfo) | **GET** /endpoints | Gets the list of endpoints for the authenticated subscription. |
| [**endpointsListBaseModelLogs**](CustomSpeechEndpointsApi.md#endpointsListBaseModelLogs) | **GET** /endpoints/base/{locale}/files/logs | Gets the list of audio and transcription logs that have been stored when using the default base model of a given language. |
| [**endpointsListBaseModelLogsWithHttpInfo**](CustomSpeechEndpointsApi.md#endpointsListBaseModelLogsWithHttpInfo) | **GET** /endpoints/base/{locale}/files/logs | Gets the list of audio and transcription logs that have been stored when using the default base model of a given language. |
| [**endpointsListLogs**](CustomSpeechEndpointsApi.md#endpointsListLogs) | **GET** /endpoints/{id}/files/logs | Gets the list of audio and transcription logs that have been stored for a given endpoint. |
| [**endpointsListLogsWithHttpInfo**](CustomSpeechEndpointsApi.md#endpointsListLogsWithHttpInfo) | **GET** /endpoints/{id}/files/logs | Gets the list of audio and transcription logs that have been stored for a given endpoint. |
| [**endpointsListSupportedLocales**](CustomSpeechEndpointsApi.md#endpointsListSupportedLocales) | **GET** /endpoints/locales | Gets a list of supported locales for endpoint creations. |
| [**endpointsListSupportedLocalesWithHttpInfo**](CustomSpeechEndpointsApi.md#endpointsListSupportedLocalesWithHttpInfo) | **GET** /endpoints/locales | Gets a list of supported locales for endpoint creations. |
| [**endpointsUpdate**](CustomSpeechEndpointsApi.md#endpointsUpdate) | **PATCH** /endpoints/{id} | Updates the metadata of the endpoint identified by the given ID. |
| [**endpointsUpdateWithHttpInfo**](CustomSpeechEndpointsApi.md#endpointsUpdateWithHttpInfo) | **PATCH** /endpoints/{id} | Updates the metadata of the endpoint identified by the given ID. |



## endpointsCreate

> Endpoint endpointsCreate(endpoint)

Creates a new endpoint.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechEndpointsApi;

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

        CustomSpeechEndpointsApi apiInstance = new CustomSpeechEndpointsApi(defaultClient);
        Endpoint endpoint = new Endpoint(); // Endpoint | The details of the endpoint.
        try {
            Endpoint result = apiInstance.endpointsCreate(endpoint);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechEndpointsApi#endpointsCreate");
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
| **endpoint** | [**Endpoint**](Endpoint.md)| The details of the endpoint. | |

### Return type

[**Endpoint**](Endpoint.md)


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

## endpointsCreateWithHttpInfo

> ApiResponse<Endpoint> endpointsCreate endpointsCreateWithHttpInfo(endpoint)

Creates a new endpoint.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechEndpointsApi;

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

        CustomSpeechEndpointsApi apiInstance = new CustomSpeechEndpointsApi(defaultClient);
        Endpoint endpoint = new Endpoint(); // Endpoint | The details of the endpoint.
        try {
            ApiResponse<Endpoint> response = apiInstance.endpointsCreateWithHttpInfo(endpoint);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechEndpointsApi#endpointsCreate");
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
| **endpoint** | [**Endpoint**](Endpoint.md)| The details of the endpoint. | |

### Return type

ApiResponse<[**Endpoint**](Endpoint.md)>


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


## endpointsDelete

> void endpointsDelete(id)

Deletes the endpoint identified by the given ID.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechEndpointsApi;

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

        CustomSpeechEndpointsApi apiInstance = new CustomSpeechEndpointsApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the endpoint.
        try {
            apiInstance.endpointsDelete(id);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechEndpointsApi#endpointsDelete");
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
| **id** | **UUID**| The identifier of the endpoint. | |

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
| **204** | The model endpoint was successfully deleted. |  -  |
| **0** | An error occurred. |  -  |

## endpointsDeleteWithHttpInfo

> ApiResponse<Void> endpointsDelete endpointsDeleteWithHttpInfo(id)

Deletes the endpoint identified by the given ID.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechEndpointsApi;

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

        CustomSpeechEndpointsApi apiInstance = new CustomSpeechEndpointsApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the endpoint.
        try {
            ApiResponse<Void> response = apiInstance.endpointsDeleteWithHttpInfo(id);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechEndpointsApi#endpointsDelete");
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
| **id** | **UUID**| The identifier of the endpoint. | |

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
| **204** | The model endpoint was successfully deleted. |  -  |
| **0** | An error occurred. |  -  |


## endpointsDeleteBaseModelLog

> void endpointsDeleteBaseModelLog(locale, logId)

Deletes one audio or transcription log that have been stored when using the default base model of a given language.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechEndpointsApi;

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

        CustomSpeechEndpointsApi apiInstance = new CustomSpeechEndpointsApi(defaultClient);
        String locale = "locale_example"; // String | The language used to select the default base model.
        String logId = "logId_example"; // String | The identifier of the log.
        try {
            apiInstance.endpointsDeleteBaseModelLog(locale, logId);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechEndpointsApi#endpointsDeleteBaseModelLog");
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
| **locale** | **String**| The language used to select the default base model. | |
| **logId** | **String**| The identifier of the log. | |

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
| **204** | The log was successfully deleted. |  -  |
| **0** | An error occurred. |  -  |

## endpointsDeleteBaseModelLogWithHttpInfo

> ApiResponse<Void> endpointsDeleteBaseModelLog endpointsDeleteBaseModelLogWithHttpInfo(locale, logId)

Deletes one audio or transcription log that have been stored when using the default base model of a given language.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechEndpointsApi;

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

        CustomSpeechEndpointsApi apiInstance = new CustomSpeechEndpointsApi(defaultClient);
        String locale = "locale_example"; // String | The language used to select the default base model.
        String logId = "logId_example"; // String | The identifier of the log.
        try {
            ApiResponse<Void> response = apiInstance.endpointsDeleteBaseModelLogWithHttpInfo(locale, logId);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechEndpointsApi#endpointsDeleteBaseModelLog");
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
| **locale** | **String**| The language used to select the default base model. | |
| **logId** | **String**| The identifier of the log. | |

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
| **204** | The log was successfully deleted. |  -  |
| **0** | An error occurred. |  -  |


## endpointsDeleteBaseModelLogs

> void endpointsDeleteBaseModelLogs(locale, endDate)

Deletes the specified audio and transcription logs that have been stored when using the default base model of a given language. It deletes all logs before (and including) a specific day.

Deletion process is done asynchronously and can take up to one day depending on the amount of log files.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechEndpointsApi;

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

        CustomSpeechEndpointsApi apiInstance = new CustomSpeechEndpointsApi(defaultClient);
        String locale = "locale_example"; // String | The language used to select the default base model.
        String endDate = "endDate_example"; // String | The end date of the audio logs deletion (specific day, UTC).              Expected format: \"yyyy-mm-dd\". For instance, \"2023-03-15\" results in deleting all logs on March 15th, 2023 and before.              Deletes all existing logs when date is not specified.
        try {
            apiInstance.endpointsDeleteBaseModelLogs(locale, endDate);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechEndpointsApi#endpointsDeleteBaseModelLogs");
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
| **locale** | **String**| The language used to select the default base model. | |
| **endDate** | **String**| The end date of the audio logs deletion (specific day, UTC).              Expected format: \&quot;yyyy-mm-dd\&quot;. For instance, \&quot;2023-03-15\&quot; results in deleting all logs on March 15th, 2023 and before.              Deletes all existing logs when date is not specified. | [optional] |

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
| **202** | The logs will be deleted. |  -  |
| **0** | An error occurred. |  -  |

## endpointsDeleteBaseModelLogsWithHttpInfo

> ApiResponse<Void> endpointsDeleteBaseModelLogs endpointsDeleteBaseModelLogsWithHttpInfo(locale, endDate)

Deletes the specified audio and transcription logs that have been stored when using the default base model of a given language. It deletes all logs before (and including) a specific day.

Deletion process is done asynchronously and can take up to one day depending on the amount of log files.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechEndpointsApi;

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

        CustomSpeechEndpointsApi apiInstance = new CustomSpeechEndpointsApi(defaultClient);
        String locale = "locale_example"; // String | The language used to select the default base model.
        String endDate = "endDate_example"; // String | The end date of the audio logs deletion (specific day, UTC).              Expected format: \"yyyy-mm-dd\". For instance, \"2023-03-15\" results in deleting all logs on March 15th, 2023 and before.              Deletes all existing logs when date is not specified.
        try {
            ApiResponse<Void> response = apiInstance.endpointsDeleteBaseModelLogsWithHttpInfo(locale, endDate);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechEndpointsApi#endpointsDeleteBaseModelLogs");
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
| **locale** | **String**| The language used to select the default base model. | |
| **endDate** | **String**| The end date of the audio logs deletion (specific day, UTC).              Expected format: \&quot;yyyy-mm-dd\&quot;. For instance, \&quot;2023-03-15\&quot; results in deleting all logs on March 15th, 2023 and before.              Deletes all existing logs when date is not specified. | [optional] |

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
| **202** | The logs will be deleted. |  -  |
| **0** | An error occurred. |  -  |


## endpointsDeleteLog

> void endpointsDeleteLog(id, logId)

Deletes one audio or transcription log that have been stored for a given endpoint.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechEndpointsApi;

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

        CustomSpeechEndpointsApi apiInstance = new CustomSpeechEndpointsApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the endpoint.
        String logId = "logId_example"; // String | The identifier of the log.
        try {
            apiInstance.endpointsDeleteLog(id, logId);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechEndpointsApi#endpointsDeleteLog");
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
| **id** | **UUID**| The identifier of the endpoint. | |
| **logId** | **String**| The identifier of the log. | |

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
| **204** | The log was successfully deleted. |  -  |
| **0** | An error occurred. |  -  |

## endpointsDeleteLogWithHttpInfo

> ApiResponse<Void> endpointsDeleteLog endpointsDeleteLogWithHttpInfo(id, logId)

Deletes one audio or transcription log that have been stored for a given endpoint.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechEndpointsApi;

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

        CustomSpeechEndpointsApi apiInstance = new CustomSpeechEndpointsApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the endpoint.
        String logId = "logId_example"; // String | The identifier of the log.
        try {
            ApiResponse<Void> response = apiInstance.endpointsDeleteLogWithHttpInfo(id, logId);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechEndpointsApi#endpointsDeleteLog");
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
| **id** | **UUID**| The identifier of the endpoint. | |
| **logId** | **String**| The identifier of the log. | |

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
| **204** | The log was successfully deleted. |  -  |
| **0** | An error occurred. |  -  |


## endpointsDeleteLogs

> void endpointsDeleteLogs(id, endDate)

Deletes the specified audio and transcription logs that have been stored for a given endpoint. It deletes all logs before (and including) a specific day.

The deletion process is done asynchronously and can take up to one day depending on the amount of log files.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechEndpointsApi;

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

        CustomSpeechEndpointsApi apiInstance = new CustomSpeechEndpointsApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the endpoint.
        String endDate = "endDate_example"; // String | The end date of the audio logs deletion (specific day, UTC).              Expected format: \"yyyy-mm-dd\". For instance, \"2023-03-15\" results in deleting all logs on March 15th, 2023 and before.              Deletes all existing logs when date is not specified.
        try {
            apiInstance.endpointsDeleteLogs(id, endDate);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechEndpointsApi#endpointsDeleteLogs");
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
| **id** | **UUID**| The identifier of the endpoint. | |
| **endDate** | **String**| The end date of the audio logs deletion (specific day, UTC).              Expected format: \&quot;yyyy-mm-dd\&quot;. For instance, \&quot;2023-03-15\&quot; results in deleting all logs on March 15th, 2023 and before.              Deletes all existing logs when date is not specified. | [optional] |

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
| **202** | The logs will be deleted. |  -  |
| **0** | An error occurred. |  -  |

## endpointsDeleteLogsWithHttpInfo

> ApiResponse<Void> endpointsDeleteLogs endpointsDeleteLogsWithHttpInfo(id, endDate)

Deletes the specified audio and transcription logs that have been stored for a given endpoint. It deletes all logs before (and including) a specific day.

The deletion process is done asynchronously and can take up to one day depending on the amount of log files.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechEndpointsApi;

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

        CustomSpeechEndpointsApi apiInstance = new CustomSpeechEndpointsApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the endpoint.
        String endDate = "endDate_example"; // String | The end date of the audio logs deletion (specific day, UTC).              Expected format: \"yyyy-mm-dd\". For instance, \"2023-03-15\" results in deleting all logs on March 15th, 2023 and before.              Deletes all existing logs when date is not specified.
        try {
            ApiResponse<Void> response = apiInstance.endpointsDeleteLogsWithHttpInfo(id, endDate);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechEndpointsApi#endpointsDeleteLogs");
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
| **id** | **UUID**| The identifier of the endpoint. | |
| **endDate** | **String**| The end date of the audio logs deletion (specific day, UTC).              Expected format: \&quot;yyyy-mm-dd\&quot;. For instance, \&quot;2023-03-15\&quot; results in deleting all logs on March 15th, 2023 and before.              Deletes all existing logs when date is not specified. | [optional] |

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
| **202** | The logs will be deleted. |  -  |
| **0** | An error occurred. |  -  |


## endpointsGet

> Endpoint endpointsGet(id)

Gets the endpoint identified by the given ID.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechEndpointsApi;

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

        CustomSpeechEndpointsApi apiInstance = new CustomSpeechEndpointsApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the endpoint.
        try {
            Endpoint result = apiInstance.endpointsGet(id);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechEndpointsApi#endpointsGet");
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
| **id** | **UUID**| The identifier of the endpoint. | |

### Return type

[**Endpoint**](Endpoint.md)


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

## endpointsGetWithHttpInfo

> ApiResponse<Endpoint> endpointsGet endpointsGetWithHttpInfo(id)

Gets the endpoint identified by the given ID.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechEndpointsApi;

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

        CustomSpeechEndpointsApi apiInstance = new CustomSpeechEndpointsApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the endpoint.
        try {
            ApiResponse<Endpoint> response = apiInstance.endpointsGetWithHttpInfo(id);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechEndpointsApi#endpointsGet");
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
| **id** | **UUID**| The identifier of the endpoint. | |

### Return type

ApiResponse<[**Endpoint**](Endpoint.md)>


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


## endpointsGetBaseModelLog

> ModelFile endpointsGetBaseModelLog(locale, logId, sasValidityInSeconds)

Gets a specific audio or transcription log for the default base model in a given language.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechEndpointsApi;

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

        CustomSpeechEndpointsApi apiInstance = new CustomSpeechEndpointsApi(defaultClient);
        String locale = "locale_example"; // String | The language used to select the default base model.
        String logId = "logId_example"; // String | The identifier of the log.
        Integer sasValidityInSeconds = 56; // Integer | The duration in seconds that an SAS url should be valid. The default duration is 12 hours. When using BYOS (https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-encryption-of-data-at-rest#bring-your-own-storage-byos-for-customization-and-logging): A value of 0 means that a plain blob URI without SAS token will be generated.
        try {
            ModelFile result = apiInstance.endpointsGetBaseModelLog(locale, logId, sasValidityInSeconds);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechEndpointsApi#endpointsGetBaseModelLog");
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
| **locale** | **String**| The language used to select the default base model. | |
| **logId** | **String**| The identifier of the log. | |
| **sasValidityInSeconds** | **Integer**| The duration in seconds that an SAS url should be valid. The default duration is 12 hours. When using BYOS (https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-encryption-of-data-at-rest#bring-your-own-storage-byos-for-customization-and-logging): A value of 0 means that a plain blob URI without SAS token will be generated. | [optional] |

### Return type

[**ModelFile**](ModelFile.md)


### Authorization

[api_key](../README.md#api_key), [token](../README.md#token)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | OK |  -  |
| **0** | An error occurred. |  -  |

## endpointsGetBaseModelLogWithHttpInfo

> ApiResponse<ModelFile> endpointsGetBaseModelLog endpointsGetBaseModelLogWithHttpInfo(locale, logId, sasValidityInSeconds)

Gets a specific audio or transcription log for the default base model in a given language.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechEndpointsApi;

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

        CustomSpeechEndpointsApi apiInstance = new CustomSpeechEndpointsApi(defaultClient);
        String locale = "locale_example"; // String | The language used to select the default base model.
        String logId = "logId_example"; // String | The identifier of the log.
        Integer sasValidityInSeconds = 56; // Integer | The duration in seconds that an SAS url should be valid. The default duration is 12 hours. When using BYOS (https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-encryption-of-data-at-rest#bring-your-own-storage-byos-for-customization-and-logging): A value of 0 means that a plain blob URI without SAS token will be generated.
        try {
            ApiResponse<ModelFile> response = apiInstance.endpointsGetBaseModelLogWithHttpInfo(locale, logId, sasValidityInSeconds);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechEndpointsApi#endpointsGetBaseModelLog");
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
| **locale** | **String**| The language used to select the default base model. | |
| **logId** | **String**| The identifier of the log. | |
| **sasValidityInSeconds** | **Integer**| The duration in seconds that an SAS url should be valid. The default duration is 12 hours. When using BYOS (https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-encryption-of-data-at-rest#bring-your-own-storage-byos-for-customization-and-logging): A value of 0 means that a plain blob URI without SAS token will be generated. | [optional] |

### Return type

ApiResponse<[**ModelFile**](ModelFile.md)>


### Authorization

[api_key](../README.md#api_key), [token](../README.md#token)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | OK |  -  |
| **0** | An error occurred. |  -  |


## endpointsGetLog

> ModelFile endpointsGetLog(id, logId, sasValidityInSeconds)

Gets a specific audio or transcription log for a given endpoint.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechEndpointsApi;

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

        CustomSpeechEndpointsApi apiInstance = new CustomSpeechEndpointsApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the endpoint.
        String logId = "logId_example"; // String | The identifier of the log.
        Integer sasValidityInSeconds = 56; // Integer | The duration in seconds that an SAS url should be valid. The default duration is 12 hours. When using BYOS (https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-encryption-of-data-at-rest#bring-your-own-storage-byos-for-customization-and-logging): A value of 0 means that a plain blob URI without SAS token will be generated.
        try {
            ModelFile result = apiInstance.endpointsGetLog(id, logId, sasValidityInSeconds);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechEndpointsApi#endpointsGetLog");
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
| **id** | **UUID**| The identifier of the endpoint. | |
| **logId** | **String**| The identifier of the log. | |
| **sasValidityInSeconds** | **Integer**| The duration in seconds that an SAS url should be valid. The default duration is 12 hours. When using BYOS (https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-encryption-of-data-at-rest#bring-your-own-storage-byos-for-customization-and-logging): A value of 0 means that a plain blob URI without SAS token will be generated. | [optional] |

### Return type

[**ModelFile**](ModelFile.md)


### Authorization

[api_key](../README.md#api_key), [token](../README.md#token)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | OK |  -  |
| **0** | An error occurred. |  -  |

## endpointsGetLogWithHttpInfo

> ApiResponse<ModelFile> endpointsGetLog endpointsGetLogWithHttpInfo(id, logId, sasValidityInSeconds)

Gets a specific audio or transcription log for a given endpoint.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechEndpointsApi;

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

        CustomSpeechEndpointsApi apiInstance = new CustomSpeechEndpointsApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the endpoint.
        String logId = "logId_example"; // String | The identifier of the log.
        Integer sasValidityInSeconds = 56; // Integer | The duration in seconds that an SAS url should be valid. The default duration is 12 hours. When using BYOS (https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-encryption-of-data-at-rest#bring-your-own-storage-byos-for-customization-and-logging): A value of 0 means that a plain blob URI without SAS token will be generated.
        try {
            ApiResponse<ModelFile> response = apiInstance.endpointsGetLogWithHttpInfo(id, logId, sasValidityInSeconds);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechEndpointsApi#endpointsGetLog");
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
| **id** | **UUID**| The identifier of the endpoint. | |
| **logId** | **String**| The identifier of the log. | |
| **sasValidityInSeconds** | **Integer**| The duration in seconds that an SAS url should be valid. The default duration is 12 hours. When using BYOS (https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-encryption-of-data-at-rest#bring-your-own-storage-byos-for-customization-and-logging): A value of 0 means that a plain blob URI without SAS token will be generated. | [optional] |

### Return type

ApiResponse<[**ModelFile**](ModelFile.md)>


### Authorization

[api_key](../README.md#api_key), [token](../README.md#token)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | OK |  -  |
| **0** | An error occurred. |  -  |


## endpointsList

> PaginatedEndpoints endpointsList(skip, top, filter)

Gets the list of endpoints for the authenticated subscription.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechEndpointsApi;

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

        CustomSpeechEndpointsApi apiInstance = new CustomSpeechEndpointsApi(defaultClient);
        Integer skip = 56; // Integer | Number of datasets that will be skipped.
        Integer top = 56; // Integer | Number of datasets that will be included after skipping.
        String filter = "filter_example"; // String | A filtering expression for selecting a subset of the available endpoints.              - Supported properties: displayName, description, createdDateTime, lastActionDateTime, status, locale.              - Operators:                - eq, ne are supported for all properties.                - gt, ge, lt, le are supported for createdDateTime and lastActionDateTime.                - and, or, not are supported.              - Example:                filter=locale eq 'en-US'
        try {
            PaginatedEndpoints result = apiInstance.endpointsList(skip, top, filter);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechEndpointsApi#endpointsList");
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
| **filter** | **String**| A filtering expression for selecting a subset of the available endpoints.              - Supported properties: displayName, description, createdDateTime, lastActionDateTime, status, locale.              - Operators:                - eq, ne are supported for all properties.                - gt, ge, lt, le are supported for createdDateTime and lastActionDateTime.                - and, or, not are supported.              - Example:                filter&#x3D;locale eq &#39;en-US&#39; | [optional] |

### Return type

[**PaginatedEndpoints**](PaginatedEndpoints.md)


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

## endpointsListWithHttpInfo

> ApiResponse<PaginatedEndpoints> endpointsList endpointsListWithHttpInfo(skip, top, filter)

Gets the list of endpoints for the authenticated subscription.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechEndpointsApi;

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

        CustomSpeechEndpointsApi apiInstance = new CustomSpeechEndpointsApi(defaultClient);
        Integer skip = 56; // Integer | Number of datasets that will be skipped.
        Integer top = 56; // Integer | Number of datasets that will be included after skipping.
        String filter = "filter_example"; // String | A filtering expression for selecting a subset of the available endpoints.              - Supported properties: displayName, description, createdDateTime, lastActionDateTime, status, locale.              - Operators:                - eq, ne are supported for all properties.                - gt, ge, lt, le are supported for createdDateTime and lastActionDateTime.                - and, or, not are supported.              - Example:                filter=locale eq 'en-US'
        try {
            ApiResponse<PaginatedEndpoints> response = apiInstance.endpointsListWithHttpInfo(skip, top, filter);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechEndpointsApi#endpointsList");
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
| **filter** | **String**| A filtering expression for selecting a subset of the available endpoints.              - Supported properties: displayName, description, createdDateTime, lastActionDateTime, status, locale.              - Operators:                - eq, ne are supported for all properties.                - gt, ge, lt, le are supported for createdDateTime and lastActionDateTime.                - and, or, not are supported.              - Example:                filter&#x3D;locale eq &#39;en-US&#39; | [optional] |

### Return type

ApiResponse<[**PaginatedEndpoints**](PaginatedEndpoints.md)>


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


## endpointsListBaseModelLogs

> PaginatedFiles endpointsListBaseModelLogs(locale, sasValidityInSeconds, skipToken, top)

Gets the list of audio and transcription logs that have been stored when using the default base model of a given language.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechEndpointsApi;

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

        CustomSpeechEndpointsApi apiInstance = new CustomSpeechEndpointsApi(defaultClient);
        String locale = "locale_example"; // String | The language used to select the default base model.
        Integer sasValidityInSeconds = 56; // Integer | The duration in seconds that an SAS url should be valid. The default duration is 12 hours. When using BYOS (https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-encryption-of-data-at-rest#bring-your-own-storage-byos-for-customization-and-logging): A value of 0 means that a plain blob URI without SAS token will be generated.
        String skipToken = "skipToken_example"; // String | Token to skip logs that were already retrieved in previous requests. Pagination starts from beginning when not defined.
        Integer top = 56; // Integer | Number of datasets that will be included after skipping.
        try {
            PaginatedFiles result = apiInstance.endpointsListBaseModelLogs(locale, sasValidityInSeconds, skipToken, top);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechEndpointsApi#endpointsListBaseModelLogs");
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
| **locale** | **String**| The language used to select the default base model. | |
| **sasValidityInSeconds** | **Integer**| The duration in seconds that an SAS url should be valid. The default duration is 12 hours. When using BYOS (https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-encryption-of-data-at-rest#bring-your-own-storage-byos-for-customization-and-logging): A value of 0 means that a plain blob URI without SAS token will be generated. | [optional] |
| **skipToken** | **String**| Token to skip logs that were already retrieved in previous requests. Pagination starts from beginning when not defined. | [optional] |
| **top** | **Integer**| Number of datasets that will be included after skipping. | [optional] |

### Return type

[**PaginatedFiles**](PaginatedFiles.md)


### Authorization

[api_key](../README.md#api_key), [token](../README.md#token)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | OK |  -  |
| **0** | An error occurred. |  -  |

## endpointsListBaseModelLogsWithHttpInfo

> ApiResponse<PaginatedFiles> endpointsListBaseModelLogs endpointsListBaseModelLogsWithHttpInfo(locale, sasValidityInSeconds, skipToken, top)

Gets the list of audio and transcription logs that have been stored when using the default base model of a given language.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechEndpointsApi;

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

        CustomSpeechEndpointsApi apiInstance = new CustomSpeechEndpointsApi(defaultClient);
        String locale = "locale_example"; // String | The language used to select the default base model.
        Integer sasValidityInSeconds = 56; // Integer | The duration in seconds that an SAS url should be valid. The default duration is 12 hours. When using BYOS (https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-encryption-of-data-at-rest#bring-your-own-storage-byos-for-customization-and-logging): A value of 0 means that a plain blob URI without SAS token will be generated.
        String skipToken = "skipToken_example"; // String | Token to skip logs that were already retrieved in previous requests. Pagination starts from beginning when not defined.
        Integer top = 56; // Integer | Number of datasets that will be included after skipping.
        try {
            ApiResponse<PaginatedFiles> response = apiInstance.endpointsListBaseModelLogsWithHttpInfo(locale, sasValidityInSeconds, skipToken, top);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechEndpointsApi#endpointsListBaseModelLogs");
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
| **locale** | **String**| The language used to select the default base model. | |
| **sasValidityInSeconds** | **Integer**| The duration in seconds that an SAS url should be valid. The default duration is 12 hours. When using BYOS (https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-encryption-of-data-at-rest#bring-your-own-storage-byos-for-customization-and-logging): A value of 0 means that a plain blob URI without SAS token will be generated. | [optional] |
| **skipToken** | **String**| Token to skip logs that were already retrieved in previous requests. Pagination starts from beginning when not defined. | [optional] |
| **top** | **Integer**| Number of datasets that will be included after skipping. | [optional] |

### Return type

ApiResponse<[**PaginatedFiles**](PaginatedFiles.md)>


### Authorization

[api_key](../README.md#api_key), [token](../README.md#token)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | OK |  -  |
| **0** | An error occurred. |  -  |


## endpointsListLogs

> PaginatedFiles endpointsListLogs(id, sasValidityInSeconds, skipToken, top)

Gets the list of audio and transcription logs that have been stored for a given endpoint.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechEndpointsApi;

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

        CustomSpeechEndpointsApi apiInstance = new CustomSpeechEndpointsApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the endpoint.
        Integer sasValidityInSeconds = 56; // Integer | The duration in seconds that an SAS url should be valid. The default duration is 12 hours. When using BYOS (https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-encryption-of-data-at-rest#bring-your-own-storage-byos-for-customization-and-logging): A value of 0 means that a plain blob URI without SAS token will be generated.
        String skipToken = "skipToken_example"; // String | Token to skip logs that were already retrieved in previous requests. Pagination starts from beginning when not defined.
        Integer top = 56; // Integer | Number of datasets that will be included after skipping.
        try {
            PaginatedFiles result = apiInstance.endpointsListLogs(id, sasValidityInSeconds, skipToken, top);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechEndpointsApi#endpointsListLogs");
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
| **id** | **UUID**| The identifier of the endpoint. | |
| **sasValidityInSeconds** | **Integer**| The duration in seconds that an SAS url should be valid. The default duration is 12 hours. When using BYOS (https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-encryption-of-data-at-rest#bring-your-own-storage-byos-for-customization-and-logging): A value of 0 means that a plain blob URI without SAS token will be generated. | [optional] |
| **skipToken** | **String**| Token to skip logs that were already retrieved in previous requests. Pagination starts from beginning when not defined. | [optional] |
| **top** | **Integer**| Number of datasets that will be included after skipping. | [optional] |

### Return type

[**PaginatedFiles**](PaginatedFiles.md)


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

## endpointsListLogsWithHttpInfo

> ApiResponse<PaginatedFiles> endpointsListLogs endpointsListLogsWithHttpInfo(id, sasValidityInSeconds, skipToken, top)

Gets the list of audio and transcription logs that have been stored for a given endpoint.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechEndpointsApi;

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

        CustomSpeechEndpointsApi apiInstance = new CustomSpeechEndpointsApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the endpoint.
        Integer sasValidityInSeconds = 56; // Integer | The duration in seconds that an SAS url should be valid. The default duration is 12 hours. When using BYOS (https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-encryption-of-data-at-rest#bring-your-own-storage-byos-for-customization-and-logging): A value of 0 means that a plain blob URI without SAS token will be generated.
        String skipToken = "skipToken_example"; // String | Token to skip logs that were already retrieved in previous requests. Pagination starts from beginning when not defined.
        Integer top = 56; // Integer | Number of datasets that will be included after skipping.
        try {
            ApiResponse<PaginatedFiles> response = apiInstance.endpointsListLogsWithHttpInfo(id, sasValidityInSeconds, skipToken, top);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechEndpointsApi#endpointsListLogs");
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
| **id** | **UUID**| The identifier of the endpoint. | |
| **sasValidityInSeconds** | **Integer**| The duration in seconds that an SAS url should be valid. The default duration is 12 hours. When using BYOS (https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-encryption-of-data-at-rest#bring-your-own-storage-byos-for-customization-and-logging): A value of 0 means that a plain blob URI without SAS token will be generated. | [optional] |
| **skipToken** | **String**| Token to skip logs that were already retrieved in previous requests. Pagination starts from beginning when not defined. | [optional] |
| **top** | **Integer**| Number of datasets that will be included after skipping. | [optional] |

### Return type

ApiResponse<[**PaginatedFiles**](PaginatedFiles.md)>


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


## endpointsListSupportedLocales

> List<String> endpointsListSupportedLocales()

Gets a list of supported locales for endpoint creations.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechEndpointsApi;

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

        CustomSpeechEndpointsApi apiInstance = new CustomSpeechEndpointsApi(defaultClient);
        try {
            List<String> result = apiInstance.endpointsListSupportedLocales();
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechEndpointsApi#endpointsListSupportedLocales");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Reason: " + e.getResponseBody());
            System.err.println("Response headers: " + e.getResponseHeaders());
            e.printStackTrace();
        }
    }
}
```

### Parameters

This endpoint does not need any parameter.

### Return type

**List&lt;String&gt;**


### Authorization

[api_key](../README.md#api_key), [token](../README.md#token)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | OK |  -  |
| **0** | An error occurred. |  -  |

## endpointsListSupportedLocalesWithHttpInfo

> ApiResponse<List<String>> endpointsListSupportedLocales endpointsListSupportedLocalesWithHttpInfo()

Gets a list of supported locales for endpoint creations.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechEndpointsApi;

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

        CustomSpeechEndpointsApi apiInstance = new CustomSpeechEndpointsApi(defaultClient);
        try {
            ApiResponse<List<String>> response = apiInstance.endpointsListSupportedLocalesWithHttpInfo();
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechEndpointsApi#endpointsListSupportedLocales");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Response headers: " + e.getResponseHeaders());
            System.err.println("Reason: " + e.getResponseBody());
            e.printStackTrace();
        }
    }
}
```

### Parameters

This endpoint does not need any parameter.

### Return type

ApiResponse<**List&lt;String&gt;**>


### Authorization

[api_key](../README.md#api_key), [token](../README.md#token)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | OK |  -  |
| **0** | An error occurred. |  -  |


## endpointsUpdate

> Endpoint endpointsUpdate(id, endpointUpdate)

Updates the metadata of the endpoint identified by the given ID.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechEndpointsApi;

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

        CustomSpeechEndpointsApi apiInstance = new CustomSpeechEndpointsApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the endpoint.
        EndpointUpdate endpointUpdate = new EndpointUpdate(); // EndpointUpdate | The updated values for the endpoint.
        try {
            Endpoint result = apiInstance.endpointsUpdate(id, endpointUpdate);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechEndpointsApi#endpointsUpdate");
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
| **id** | **UUID**| The identifier of the endpoint. | |
| **endpointUpdate** | [**EndpointUpdate**](EndpointUpdate.md)| The updated values for the endpoint. | |

### Return type

[**Endpoint**](Endpoint.md)


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

## endpointsUpdateWithHttpInfo

> ApiResponse<Endpoint> endpointsUpdate endpointsUpdateWithHttpInfo(id, endpointUpdate)

Updates the metadata of the endpoint identified by the given ID.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechEndpointsApi;

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

        CustomSpeechEndpointsApi apiInstance = new CustomSpeechEndpointsApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the endpoint.
        EndpointUpdate endpointUpdate = new EndpointUpdate(); // EndpointUpdate | The updated values for the endpoint.
        try {
            ApiResponse<Endpoint> response = apiInstance.endpointsUpdateWithHttpInfo(id, endpointUpdate);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechEndpointsApi#endpointsUpdate");
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
| **id** | **UUID**| The identifier of the endpoint. | |
| **endpointUpdate** | [**EndpointUpdate**](EndpointUpdate.md)| The updated values for the endpoint. | |

### Return type

ApiResponse<[**Endpoint**](Endpoint.md)>


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

