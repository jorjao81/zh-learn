# CustomSpeechModelEvaluationsApi

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**evaluationsCreate**](CustomSpeechModelEvaluationsApi.md#evaluationsCreate) | **POST** /evaluations | Creates a new evaluation. |
| [**evaluationsCreateWithHttpInfo**](CustomSpeechModelEvaluationsApi.md#evaluationsCreateWithHttpInfo) | **POST** /evaluations | Creates a new evaluation. |
| [**evaluationsDelete**](CustomSpeechModelEvaluationsApi.md#evaluationsDelete) | **DELETE** /evaluations/{id} | Deletes the evaluation identified by the given ID. |
| [**evaluationsDeleteWithHttpInfo**](CustomSpeechModelEvaluationsApi.md#evaluationsDeleteWithHttpInfo) | **DELETE** /evaluations/{id} | Deletes the evaluation identified by the given ID. |
| [**evaluationsGet**](CustomSpeechModelEvaluationsApi.md#evaluationsGet) | **GET** /evaluations/{id} | Gets the evaluation identified by the given ID. |
| [**evaluationsGetWithHttpInfo**](CustomSpeechModelEvaluationsApi.md#evaluationsGetWithHttpInfo) | **GET** /evaluations/{id} | Gets the evaluation identified by the given ID. |
| [**evaluationsGetFile**](CustomSpeechModelEvaluationsApi.md#evaluationsGetFile) | **GET** /evaluations/{id}/files/{fileId} | Gets one specific file (identified with fileId) from an evaluation (identified with id). |
| [**evaluationsGetFileWithHttpInfo**](CustomSpeechModelEvaluationsApi.md#evaluationsGetFileWithHttpInfo) | **GET** /evaluations/{id}/files/{fileId} | Gets one specific file (identified with fileId) from an evaluation (identified with id). |
| [**evaluationsList**](CustomSpeechModelEvaluationsApi.md#evaluationsList) | **GET** /evaluations | Gets the list of evaluations for the authenticated subscription. |
| [**evaluationsListWithHttpInfo**](CustomSpeechModelEvaluationsApi.md#evaluationsListWithHttpInfo) | **GET** /evaluations | Gets the list of evaluations for the authenticated subscription. |
| [**evaluationsListFiles**](CustomSpeechModelEvaluationsApi.md#evaluationsListFiles) | **GET** /evaluations/{id}/files | Gets the files of the evaluation identified by the given ID. |
| [**evaluationsListFilesWithHttpInfo**](CustomSpeechModelEvaluationsApi.md#evaluationsListFilesWithHttpInfo) | **GET** /evaluations/{id}/files | Gets the files of the evaluation identified by the given ID. |
| [**evaluationsListSupportedLocales**](CustomSpeechModelEvaluationsApi.md#evaluationsListSupportedLocales) | **GET** /evaluations/locales | Gets a list of supported locales for evaluations. |
| [**evaluationsListSupportedLocalesWithHttpInfo**](CustomSpeechModelEvaluationsApi.md#evaluationsListSupportedLocalesWithHttpInfo) | **GET** /evaluations/locales | Gets a list of supported locales for evaluations. |
| [**evaluationsUpdate**](CustomSpeechModelEvaluationsApi.md#evaluationsUpdate) | **PATCH** /evaluations/{id} | Updates the mutable details of the evaluation identified by its id. |
| [**evaluationsUpdateWithHttpInfo**](CustomSpeechModelEvaluationsApi.md#evaluationsUpdateWithHttpInfo) | **PATCH** /evaluations/{id} | Updates the mutable details of the evaluation identified by its id. |



## evaluationsCreate

> Evaluation evaluationsCreate(evaluation)

Creates a new evaluation.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechModelEvaluationsApi;

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

        CustomSpeechModelEvaluationsApi apiInstance = new CustomSpeechModelEvaluationsApi(defaultClient);
        Evaluation evaluation = new Evaluation(); // Evaluation | The details of the new evaluation.
        try {
            Evaluation result = apiInstance.evaluationsCreate(evaluation);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechModelEvaluationsApi#evaluationsCreate");
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
| **evaluation** | [**Evaluation**](Evaluation.md)| The details of the new evaluation. | |

### Return type

[**Evaluation**](Evaluation.md)


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

## evaluationsCreateWithHttpInfo

> ApiResponse<Evaluation> evaluationsCreate evaluationsCreateWithHttpInfo(evaluation)

Creates a new evaluation.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechModelEvaluationsApi;

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

        CustomSpeechModelEvaluationsApi apiInstance = new CustomSpeechModelEvaluationsApi(defaultClient);
        Evaluation evaluation = new Evaluation(); // Evaluation | The details of the new evaluation.
        try {
            ApiResponse<Evaluation> response = apiInstance.evaluationsCreateWithHttpInfo(evaluation);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechModelEvaluationsApi#evaluationsCreate");
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
| **evaluation** | [**Evaluation**](Evaluation.md)| The details of the new evaluation. | |

### Return type

ApiResponse<[**Evaluation**](Evaluation.md)>


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


## evaluationsDelete

> void evaluationsDelete(id)

Deletes the evaluation identified by the given ID.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechModelEvaluationsApi;

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

        CustomSpeechModelEvaluationsApi apiInstance = new CustomSpeechModelEvaluationsApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the evaluation.
        try {
            apiInstance.evaluationsDelete(id);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechModelEvaluationsApi#evaluationsDelete");
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
| **id** | **UUID**| The identifier of the evaluation. | |

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
| **204** | The evaluation was successfully deleted or did not exist. |  -  |
| **0** | An error occurred. |  -  |

## evaluationsDeleteWithHttpInfo

> ApiResponse<Void> evaluationsDelete evaluationsDeleteWithHttpInfo(id)

Deletes the evaluation identified by the given ID.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechModelEvaluationsApi;

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

        CustomSpeechModelEvaluationsApi apiInstance = new CustomSpeechModelEvaluationsApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the evaluation.
        try {
            ApiResponse<Void> response = apiInstance.evaluationsDeleteWithHttpInfo(id);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechModelEvaluationsApi#evaluationsDelete");
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
| **id** | **UUID**| The identifier of the evaluation. | |

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
| **204** | The evaluation was successfully deleted or did not exist. |  -  |
| **0** | An error occurred. |  -  |


## evaluationsGet

> Evaluation evaluationsGet(id)

Gets the evaluation identified by the given ID.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechModelEvaluationsApi;

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

        CustomSpeechModelEvaluationsApi apiInstance = new CustomSpeechModelEvaluationsApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the evaluation.
        try {
            Evaluation result = apiInstance.evaluationsGet(id);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechModelEvaluationsApi#evaluationsGet");
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
| **id** | **UUID**| The identifier of the evaluation. | |

### Return type

[**Evaluation**](Evaluation.md)


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

## evaluationsGetWithHttpInfo

> ApiResponse<Evaluation> evaluationsGet evaluationsGetWithHttpInfo(id)

Gets the evaluation identified by the given ID.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechModelEvaluationsApi;

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

        CustomSpeechModelEvaluationsApi apiInstance = new CustomSpeechModelEvaluationsApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the evaluation.
        try {
            ApiResponse<Evaluation> response = apiInstance.evaluationsGetWithHttpInfo(id);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechModelEvaluationsApi#evaluationsGet");
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
| **id** | **UUID**| The identifier of the evaluation. | |

### Return type

ApiResponse<[**Evaluation**](Evaluation.md)>


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


## evaluationsGetFile

> ModelFile evaluationsGetFile(id, fileId, sasValidityInSeconds)

Gets one specific file (identified with fileId) from an evaluation (identified with id).

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechModelEvaluationsApi;

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

        CustomSpeechModelEvaluationsApi apiInstance = new CustomSpeechModelEvaluationsApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the evaluation.
        UUID fileId = UUID.randomUUID(); // UUID | The identifier of the file.
        Integer sasValidityInSeconds = 56; // Integer | The duration in seconds that an SAS url should be valid. The default duration is 12 hours. When using BYOS (https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-encryption-of-data-at-rest#bring-your-own-storage-byos-for-customization-and-logging): A value of 0 means that a plain blob URI without SAS token will be generated.
        try {
            ModelFile result = apiInstance.evaluationsGetFile(id, fileId, sasValidityInSeconds);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechModelEvaluationsApi#evaluationsGetFile");
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
| **id** | **UUID**| The identifier of the evaluation. | |
| **fileId** | **UUID**| The identifier of the file. | |
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

## evaluationsGetFileWithHttpInfo

> ApiResponse<ModelFile> evaluationsGetFile evaluationsGetFileWithHttpInfo(id, fileId, sasValidityInSeconds)

Gets one specific file (identified with fileId) from an evaluation (identified with id).

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechModelEvaluationsApi;

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

        CustomSpeechModelEvaluationsApi apiInstance = new CustomSpeechModelEvaluationsApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the evaluation.
        UUID fileId = UUID.randomUUID(); // UUID | The identifier of the file.
        Integer sasValidityInSeconds = 56; // Integer | The duration in seconds that an SAS url should be valid. The default duration is 12 hours. When using BYOS (https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-encryption-of-data-at-rest#bring-your-own-storage-byos-for-customization-and-logging): A value of 0 means that a plain blob URI without SAS token will be generated.
        try {
            ApiResponse<ModelFile> response = apiInstance.evaluationsGetFileWithHttpInfo(id, fileId, sasValidityInSeconds);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechModelEvaluationsApi#evaluationsGetFile");
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
| **id** | **UUID**| The identifier of the evaluation. | |
| **fileId** | **UUID**| The identifier of the file. | |
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


## evaluationsList

> PaginatedEvaluations evaluationsList(skip, top, filter)

Gets the list of evaluations for the authenticated subscription.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechModelEvaluationsApi;

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

        CustomSpeechModelEvaluationsApi apiInstance = new CustomSpeechModelEvaluationsApi(defaultClient);
        Integer skip = 56; // Integer | Number of datasets that will be skipped.
        Integer top = 56; // Integer | Number of datasets that will be included after skipping.
        String filter = "filter_example"; // String | A filtering expression for selecting a subset of the available evaluations.              - Supported properties: displayName, description, createdDateTime, lastActionDateTime, status and locale.              - Operators:                - eq, ne are supported for all properties.                - gt, ge, lt, le are supported for createdDateTime and lastActionDateTime.                - and, or, not are supported.              - Example:                filter=displayName eq 'My evaluation'
        try {
            PaginatedEvaluations result = apiInstance.evaluationsList(skip, top, filter);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechModelEvaluationsApi#evaluationsList");
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
| **filter** | **String**| A filtering expression for selecting a subset of the available evaluations.              - Supported properties: displayName, description, createdDateTime, lastActionDateTime, status and locale.              - Operators:                - eq, ne are supported for all properties.                - gt, ge, lt, le are supported for createdDateTime and lastActionDateTime.                - and, or, not are supported.              - Example:                filter&#x3D;displayName eq &#39;My evaluation&#39; | [optional] |

### Return type

[**PaginatedEvaluations**](PaginatedEvaluations.md)


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

## evaluationsListWithHttpInfo

> ApiResponse<PaginatedEvaluations> evaluationsList evaluationsListWithHttpInfo(skip, top, filter)

Gets the list of evaluations for the authenticated subscription.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechModelEvaluationsApi;

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

        CustomSpeechModelEvaluationsApi apiInstance = new CustomSpeechModelEvaluationsApi(defaultClient);
        Integer skip = 56; // Integer | Number of datasets that will be skipped.
        Integer top = 56; // Integer | Number of datasets that will be included after skipping.
        String filter = "filter_example"; // String | A filtering expression for selecting a subset of the available evaluations.              - Supported properties: displayName, description, createdDateTime, lastActionDateTime, status and locale.              - Operators:                - eq, ne are supported for all properties.                - gt, ge, lt, le are supported for createdDateTime and lastActionDateTime.                - and, or, not are supported.              - Example:                filter=displayName eq 'My evaluation'
        try {
            ApiResponse<PaginatedEvaluations> response = apiInstance.evaluationsListWithHttpInfo(skip, top, filter);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechModelEvaluationsApi#evaluationsList");
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
| **filter** | **String**| A filtering expression for selecting a subset of the available evaluations.              - Supported properties: displayName, description, createdDateTime, lastActionDateTime, status and locale.              - Operators:                - eq, ne are supported for all properties.                - gt, ge, lt, le are supported for createdDateTime and lastActionDateTime.                - and, or, not are supported.              - Example:                filter&#x3D;displayName eq &#39;My evaluation&#39; | [optional] |

### Return type

ApiResponse<[**PaginatedEvaluations**](PaginatedEvaluations.md)>


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


## evaluationsListFiles

> PaginatedFiles evaluationsListFiles(id, sasValidityInSeconds, skip, top, filter)

Gets the files of the evaluation identified by the given ID.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechModelEvaluationsApi;

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

        CustomSpeechModelEvaluationsApi apiInstance = new CustomSpeechModelEvaluationsApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the evaluation.
        Integer sasValidityInSeconds = 56; // Integer | The duration in seconds that an SAS url should be valid. The default duration is 12 hours. When using BYOS (https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-encryption-of-data-at-rest#bring-your-own-storage-byos-for-customization-and-logging): A value of 0 means that a plain blob URI without SAS token will be generated.
        Integer skip = 56; // Integer | Number of datasets that will be skipped.
        Integer top = 56; // Integer | Number of datasets that will be included after skipping.
        String filter = "filter_example"; // String | A filtering expression for selecting a subset of the available files.              - Supported properties: name, createdDateTime, kind.              - Operators:                - eq, ne are supported for all properties.                - gt, ge, lt, le are supported for createdDateTime.                - and, or, not are supported.              - Example:                filter=name eq 'myaudio.wav' and kind eq 'Audio'
        try {
            PaginatedFiles result = apiInstance.evaluationsListFiles(id, sasValidityInSeconds, skip, top, filter);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechModelEvaluationsApi#evaluationsListFiles");
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
| **id** | **UUID**| The identifier of the evaluation. | |
| **sasValidityInSeconds** | **Integer**| The duration in seconds that an SAS url should be valid. The default duration is 12 hours. When using BYOS (https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-encryption-of-data-at-rest#bring-your-own-storage-byos-for-customization-and-logging): A value of 0 means that a plain blob URI without SAS token will be generated. | [optional] |
| **skip** | **Integer**| Number of datasets that will be skipped. | [optional] |
| **top** | **Integer**| Number of datasets that will be included after skipping. | [optional] |
| **filter** | **String**| A filtering expression for selecting a subset of the available files.              - Supported properties: name, createdDateTime, kind.              - Operators:                - eq, ne are supported for all properties.                - gt, ge, lt, le are supported for createdDateTime.                - and, or, not are supported.              - Example:                filter&#x3D;name eq &#39;myaudio.wav&#39; and kind eq &#39;Audio&#39; | [optional] |

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

## evaluationsListFilesWithHttpInfo

> ApiResponse<PaginatedFiles> evaluationsListFiles evaluationsListFilesWithHttpInfo(id, sasValidityInSeconds, skip, top, filter)

Gets the files of the evaluation identified by the given ID.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechModelEvaluationsApi;

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

        CustomSpeechModelEvaluationsApi apiInstance = new CustomSpeechModelEvaluationsApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the evaluation.
        Integer sasValidityInSeconds = 56; // Integer | The duration in seconds that an SAS url should be valid. The default duration is 12 hours. When using BYOS (https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-encryption-of-data-at-rest#bring-your-own-storage-byos-for-customization-and-logging): A value of 0 means that a plain blob URI without SAS token will be generated.
        Integer skip = 56; // Integer | Number of datasets that will be skipped.
        Integer top = 56; // Integer | Number of datasets that will be included after skipping.
        String filter = "filter_example"; // String | A filtering expression for selecting a subset of the available files.              - Supported properties: name, createdDateTime, kind.              - Operators:                - eq, ne are supported for all properties.                - gt, ge, lt, le are supported for createdDateTime.                - and, or, not are supported.              - Example:                filter=name eq 'myaudio.wav' and kind eq 'Audio'
        try {
            ApiResponse<PaginatedFiles> response = apiInstance.evaluationsListFilesWithHttpInfo(id, sasValidityInSeconds, skip, top, filter);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechModelEvaluationsApi#evaluationsListFiles");
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
| **id** | **UUID**| The identifier of the evaluation. | |
| **sasValidityInSeconds** | **Integer**| The duration in seconds that an SAS url should be valid. The default duration is 12 hours. When using BYOS (https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-encryption-of-data-at-rest#bring-your-own-storage-byos-for-customization-and-logging): A value of 0 means that a plain blob URI without SAS token will be generated. | [optional] |
| **skip** | **Integer**| Number of datasets that will be skipped. | [optional] |
| **top** | **Integer**| Number of datasets that will be included after skipping. | [optional] |
| **filter** | **String**| A filtering expression for selecting a subset of the available files.              - Supported properties: name, createdDateTime, kind.              - Operators:                - eq, ne are supported for all properties.                - gt, ge, lt, le are supported for createdDateTime.                - and, or, not are supported.              - Example:                filter&#x3D;name eq &#39;myaudio.wav&#39; and kind eq &#39;Audio&#39; | [optional] |

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


## evaluationsListSupportedLocales

> List<String> evaluationsListSupportedLocales()

Gets a list of supported locales for evaluations.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechModelEvaluationsApi;

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

        CustomSpeechModelEvaluationsApi apiInstance = new CustomSpeechModelEvaluationsApi(defaultClient);
        try {
            List<String> result = apiInstance.evaluationsListSupportedLocales();
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechModelEvaluationsApi#evaluationsListSupportedLocales");
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

## evaluationsListSupportedLocalesWithHttpInfo

> ApiResponse<List<String>> evaluationsListSupportedLocales evaluationsListSupportedLocalesWithHttpInfo()

Gets a list of supported locales for evaluations.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechModelEvaluationsApi;

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

        CustomSpeechModelEvaluationsApi apiInstance = new CustomSpeechModelEvaluationsApi(defaultClient);
        try {
            ApiResponse<List<String>> response = apiInstance.evaluationsListSupportedLocalesWithHttpInfo();
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechModelEvaluationsApi#evaluationsListSupportedLocales");
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


## evaluationsUpdate

> Evaluation evaluationsUpdate(id, evaluationUpdate)

Updates the mutable details of the evaluation identified by its id.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechModelEvaluationsApi;

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

        CustomSpeechModelEvaluationsApi apiInstance = new CustomSpeechModelEvaluationsApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the evaluation.
        EvaluationUpdate evaluationUpdate = new EvaluationUpdate(); // EvaluationUpdate | The object containing the updated fields of the evaluation.
        try {
            Evaluation result = apiInstance.evaluationsUpdate(id, evaluationUpdate);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechModelEvaluationsApi#evaluationsUpdate");
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
| **id** | **UUID**| The identifier of the evaluation. | |
| **evaluationUpdate** | [**EvaluationUpdate**](EvaluationUpdate.md)| The object containing the updated fields of the evaluation. | |

### Return type

[**Evaluation**](Evaluation.md)


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

## evaluationsUpdateWithHttpInfo

> ApiResponse<Evaluation> evaluationsUpdate evaluationsUpdateWithHttpInfo(id, evaluationUpdate)

Updates the mutable details of the evaluation identified by its id.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechModelEvaluationsApi;

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

        CustomSpeechModelEvaluationsApi apiInstance = new CustomSpeechModelEvaluationsApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the evaluation.
        EvaluationUpdate evaluationUpdate = new EvaluationUpdate(); // EvaluationUpdate | The object containing the updated fields of the evaluation.
        try {
            ApiResponse<Evaluation> response = apiInstance.evaluationsUpdateWithHttpInfo(id, evaluationUpdate);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechModelEvaluationsApi#evaluationsUpdate");
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
| **id** | **UUID**| The identifier of the evaluation. | |
| **evaluationUpdate** | [**EvaluationUpdate**](EvaluationUpdate.md)| The object containing the updated fields of the evaluation. | |

### Return type

ApiResponse<[**Evaluation**](Evaluation.md)>


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

