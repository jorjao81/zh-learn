# CustomSpeechDatasetsForModelAdaptationApi

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**datasetsCommitBlocks**](CustomSpeechDatasetsForModelAdaptationApi.md#datasetsCommitBlocks) | **POST** /datasets/{id}/blocks:commit | Commit block list to complete the upload of the dataset. |
| [**datasetsCommitBlocksWithHttpInfo**](CustomSpeechDatasetsForModelAdaptationApi.md#datasetsCommitBlocksWithHttpInfo) | **POST** /datasets/{id}/blocks:commit | Commit block list to complete the upload of the dataset. |
| [**datasetsCreate**](CustomSpeechDatasetsForModelAdaptationApi.md#datasetsCreate) | **POST** /datasets | Uploads and creates a new dataset by getting the data from a specified URL or starts waiting for data blocks to be uploaded. |
| [**datasetsCreateWithHttpInfo**](CustomSpeechDatasetsForModelAdaptationApi.md#datasetsCreateWithHttpInfo) | **POST** /datasets | Uploads and creates a new dataset by getting the data from a specified URL or starts waiting for data blocks to be uploaded. |
| [**datasetsDelete**](CustomSpeechDatasetsForModelAdaptationApi.md#datasetsDelete) | **DELETE** /datasets/{id} | Deletes the specified dataset. |
| [**datasetsDeleteWithHttpInfo**](CustomSpeechDatasetsForModelAdaptationApi.md#datasetsDeleteWithHttpInfo) | **DELETE** /datasets/{id} | Deletes the specified dataset. |
| [**datasetsGet**](CustomSpeechDatasetsForModelAdaptationApi.md#datasetsGet) | **GET** /datasets/{id} | Gets the dataset identified by the given ID. |
| [**datasetsGetWithHttpInfo**](CustomSpeechDatasetsForModelAdaptationApi.md#datasetsGetWithHttpInfo) | **GET** /datasets/{id} | Gets the dataset identified by the given ID. |
| [**datasetsGetBlocks**](CustomSpeechDatasetsForModelAdaptationApi.md#datasetsGetBlocks) | **GET** /datasets/{id}/blocks | Gets the list of uploaded blocks for this dataset. |
| [**datasetsGetBlocksWithHttpInfo**](CustomSpeechDatasetsForModelAdaptationApi.md#datasetsGetBlocksWithHttpInfo) | **GET** /datasets/{id}/blocks | Gets the list of uploaded blocks for this dataset. |
| [**datasetsGetFile**](CustomSpeechDatasetsForModelAdaptationApi.md#datasetsGetFile) | **GET** /datasets/{id}/files/{fileId} | Gets one specific file (identified with fileId) from a dataset (identified with id). |
| [**datasetsGetFileWithHttpInfo**](CustomSpeechDatasetsForModelAdaptationApi.md#datasetsGetFileWithHttpInfo) | **GET** /datasets/{id}/files/{fileId} | Gets one specific file (identified with fileId) from a dataset (identified with id). |
| [**datasetsList**](CustomSpeechDatasetsForModelAdaptationApi.md#datasetsList) | **GET** /datasets | Gets a list of datasets for the authenticated subscription. |
| [**datasetsListWithHttpInfo**](CustomSpeechDatasetsForModelAdaptationApi.md#datasetsListWithHttpInfo) | **GET** /datasets | Gets a list of datasets for the authenticated subscription. |
| [**datasetsListFiles**](CustomSpeechDatasetsForModelAdaptationApi.md#datasetsListFiles) | **GET** /datasets/{id}/files | Gets the files of the dataset identified by the given ID. |
| [**datasetsListFilesWithHttpInfo**](CustomSpeechDatasetsForModelAdaptationApi.md#datasetsListFilesWithHttpInfo) | **GET** /datasets/{id}/files | Gets the files of the dataset identified by the given ID. |
| [**datasetsListSupportedLocales**](CustomSpeechDatasetsForModelAdaptationApi.md#datasetsListSupportedLocales) | **GET** /datasets/locales | Gets a list of supported locales for datasets. |
| [**datasetsListSupportedLocalesWithHttpInfo**](CustomSpeechDatasetsForModelAdaptationApi.md#datasetsListSupportedLocalesWithHttpInfo) | **GET** /datasets/locales | Gets a list of supported locales for datasets. |
| [**datasetsUpdate**](CustomSpeechDatasetsForModelAdaptationApi.md#datasetsUpdate) | **PATCH** /datasets/{id} | Updates the mutable details of the dataset identified by its ID. |
| [**datasetsUpdateWithHttpInfo**](CustomSpeechDatasetsForModelAdaptationApi.md#datasetsUpdateWithHttpInfo) | **PATCH** /datasets/{id} | Updates the mutable details of the dataset identified by its ID. |
| [**datasetsUpload**](CustomSpeechDatasetsForModelAdaptationApi.md#datasetsUpload) | **POST** /datasets/upload | Uploads data and creates a new dataset. |
| [**datasetsUploadWithHttpInfo**](CustomSpeechDatasetsForModelAdaptationApi.md#datasetsUploadWithHttpInfo) | **POST** /datasets/upload | Uploads data and creates a new dataset. |
| [**datasetsUploadBlock**](CustomSpeechDatasetsForModelAdaptationApi.md#datasetsUploadBlock) | **PUT** /datasets/{id}/blocks | Upload a block of data for the dataset. The maximum size of the block is 8MiB. |
| [**datasetsUploadBlockWithHttpInfo**](CustomSpeechDatasetsForModelAdaptationApi.md#datasetsUploadBlockWithHttpInfo) | **PUT** /datasets/{id}/blocks | Upload a block of data for the dataset. The maximum size of the block is 8MiB. |



## datasetsCommitBlocks

> void datasetsCommitBlocks(id, blockList)

Commit block list to complete the upload of the dataset.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechDatasetsForModelAdaptationApi;

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

        CustomSpeechDatasetsForModelAdaptationApi apiInstance = new CustomSpeechDatasetsForModelAdaptationApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the dataset.
        List<CommitBlocksEntry> blockList = Arrays.asList(); // List<CommitBlocksEntry> | The list of blocks that compile the dataset.
        try {
            apiInstance.datasetsCommitBlocks(id, blockList);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechDatasetsForModelAdaptationApi#datasetsCommitBlocks");
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
| **id** | **UUID**| The identifier of the dataset. | |
| **blockList** | [**List&lt;CommitBlocksEntry&gt;**](CommitBlocksEntry.md)| The list of blocks that compile the dataset. | |

### Return type


null (empty response body)

### Authorization

[api_key](../README.md#api_key), [token](../README.md#token)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | The block list is accepted and the data import process can continue. |  -  |
| **0** | An error occurred. |  -  |

## datasetsCommitBlocksWithHttpInfo

> ApiResponse<Void> datasetsCommitBlocks datasetsCommitBlocksWithHttpInfo(id, blockList)

Commit block list to complete the upload of the dataset.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechDatasetsForModelAdaptationApi;

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

        CustomSpeechDatasetsForModelAdaptationApi apiInstance = new CustomSpeechDatasetsForModelAdaptationApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the dataset.
        List<CommitBlocksEntry> blockList = Arrays.asList(); // List<CommitBlocksEntry> | The list of blocks that compile the dataset.
        try {
            ApiResponse<Void> response = apiInstance.datasetsCommitBlocksWithHttpInfo(id, blockList);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechDatasetsForModelAdaptationApi#datasetsCommitBlocks");
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
| **id** | **UUID**| The identifier of the dataset. | |
| **blockList** | [**List&lt;CommitBlocksEntry&gt;**](CommitBlocksEntry.md)| The list of blocks that compile the dataset. | |

### Return type


ApiResponse<Void>

### Authorization

[api_key](../README.md#api_key), [token](../README.md#token)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | The block list is accepted and the data import process can continue. |  -  |
| **0** | An error occurred. |  -  |


## datasetsCreate

> Dataset datasetsCreate(dataset)

Uploads and creates a new dataset by getting the data from a specified URL or starts waiting for data blocks to be uploaded.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechDatasetsForModelAdaptationApi;

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

        CustomSpeechDatasetsForModelAdaptationApi apiInstance = new CustomSpeechDatasetsForModelAdaptationApi(defaultClient);
        Dataset dataset = new Dataset(); // Dataset | Definition for the new dataset.
        try {
            Dataset result = apiInstance.datasetsCreate(dataset);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechDatasetsForModelAdaptationApi#datasetsCreate");
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
| **dataset** | [**Dataset**](Dataset.md)| Definition for the new dataset. | |

### Return type

[**Dataset**](Dataset.md)


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

## datasetsCreateWithHttpInfo

> ApiResponse<Dataset> datasetsCreate datasetsCreateWithHttpInfo(dataset)

Uploads and creates a new dataset by getting the data from a specified URL or starts waiting for data blocks to be uploaded.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechDatasetsForModelAdaptationApi;

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

        CustomSpeechDatasetsForModelAdaptationApi apiInstance = new CustomSpeechDatasetsForModelAdaptationApi(defaultClient);
        Dataset dataset = new Dataset(); // Dataset | Definition for the new dataset.
        try {
            ApiResponse<Dataset> response = apiInstance.datasetsCreateWithHttpInfo(dataset);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechDatasetsForModelAdaptationApi#datasetsCreate");
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
| **dataset** | [**Dataset**](Dataset.md)| Definition for the new dataset. | |

### Return type

ApiResponse<[**Dataset**](Dataset.md)>


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


## datasetsDelete

> void datasetsDelete(id)

Deletes the specified dataset.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechDatasetsForModelAdaptationApi;

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

        CustomSpeechDatasetsForModelAdaptationApi apiInstance = new CustomSpeechDatasetsForModelAdaptationApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the dataset.
        try {
            apiInstance.datasetsDelete(id);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechDatasetsForModelAdaptationApi#datasetsDelete");
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
| **id** | **UUID**| The identifier of the dataset. | |

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
| **204** | The dataset was successfully deleted or did not exist. |  -  |
| **0** | An error occurred. |  -  |

## datasetsDeleteWithHttpInfo

> ApiResponse<Void> datasetsDelete datasetsDeleteWithHttpInfo(id)

Deletes the specified dataset.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechDatasetsForModelAdaptationApi;

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

        CustomSpeechDatasetsForModelAdaptationApi apiInstance = new CustomSpeechDatasetsForModelAdaptationApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the dataset.
        try {
            ApiResponse<Void> response = apiInstance.datasetsDeleteWithHttpInfo(id);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechDatasetsForModelAdaptationApi#datasetsDelete");
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
| **id** | **UUID**| The identifier of the dataset. | |

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
| **204** | The dataset was successfully deleted or did not exist. |  -  |
| **0** | An error occurred. |  -  |


## datasetsGet

> Dataset datasetsGet(id)

Gets the dataset identified by the given ID.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechDatasetsForModelAdaptationApi;

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

        CustomSpeechDatasetsForModelAdaptationApi apiInstance = new CustomSpeechDatasetsForModelAdaptationApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the dataset.
        try {
            Dataset result = apiInstance.datasetsGet(id);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechDatasetsForModelAdaptationApi#datasetsGet");
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
| **id** | **UUID**| The identifier of the dataset. | |

### Return type

[**Dataset**](Dataset.md)


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

## datasetsGetWithHttpInfo

> ApiResponse<Dataset> datasetsGet datasetsGetWithHttpInfo(id)

Gets the dataset identified by the given ID.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechDatasetsForModelAdaptationApi;

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

        CustomSpeechDatasetsForModelAdaptationApi apiInstance = new CustomSpeechDatasetsForModelAdaptationApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the dataset.
        try {
            ApiResponse<Dataset> response = apiInstance.datasetsGetWithHttpInfo(id);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechDatasetsForModelAdaptationApi#datasetsGet");
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
| **id** | **UUID**| The identifier of the dataset. | |

### Return type

ApiResponse<[**Dataset**](Dataset.md)>


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


## datasetsGetBlocks

> UploadedBlocks datasetsGetBlocks(id)

Gets the list of uploaded blocks for this dataset.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechDatasetsForModelAdaptationApi;

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

        CustomSpeechDatasetsForModelAdaptationApi apiInstance = new CustomSpeechDatasetsForModelAdaptationApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the dataset.
        try {
            UploadedBlocks result = apiInstance.datasetsGetBlocks(id);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechDatasetsForModelAdaptationApi#datasetsGetBlocks");
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
| **id** | **UUID**| The identifier of the dataset. | |

### Return type

[**UploadedBlocks**](UploadedBlocks.md)


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

## datasetsGetBlocksWithHttpInfo

> ApiResponse<UploadedBlocks> datasetsGetBlocks datasetsGetBlocksWithHttpInfo(id)

Gets the list of uploaded blocks for this dataset.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechDatasetsForModelAdaptationApi;

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

        CustomSpeechDatasetsForModelAdaptationApi apiInstance = new CustomSpeechDatasetsForModelAdaptationApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the dataset.
        try {
            ApiResponse<UploadedBlocks> response = apiInstance.datasetsGetBlocksWithHttpInfo(id);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechDatasetsForModelAdaptationApi#datasetsGetBlocks");
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
| **id** | **UUID**| The identifier of the dataset. | |

### Return type

ApiResponse<[**UploadedBlocks**](UploadedBlocks.md)>


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


## datasetsGetFile

> ModelFile datasetsGetFile(id, fileId, sasValidityInSeconds)

Gets one specific file (identified with fileId) from a dataset (identified with id).

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechDatasetsForModelAdaptationApi;

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

        CustomSpeechDatasetsForModelAdaptationApi apiInstance = new CustomSpeechDatasetsForModelAdaptationApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the dataset.
        UUID fileId = UUID.randomUUID(); // UUID | The identifier of the file.
        Integer sasValidityInSeconds = 56; // Integer | The duration in seconds that an SAS url should be valid. The default duration is 12 hours. When using BYOS (https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-encryption-of-data-at-rest#bring-your-own-storage-byos-for-customization-and-logging): A value of 0 means that a plain blob URI without SAS token will be generated.
        try {
            ModelFile result = apiInstance.datasetsGetFile(id, fileId, sasValidityInSeconds);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechDatasetsForModelAdaptationApi#datasetsGetFile");
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
| **id** | **UUID**| The identifier of the dataset. | |
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

## datasetsGetFileWithHttpInfo

> ApiResponse<ModelFile> datasetsGetFile datasetsGetFileWithHttpInfo(id, fileId, sasValidityInSeconds)

Gets one specific file (identified with fileId) from a dataset (identified with id).

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechDatasetsForModelAdaptationApi;

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

        CustomSpeechDatasetsForModelAdaptationApi apiInstance = new CustomSpeechDatasetsForModelAdaptationApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the dataset.
        UUID fileId = UUID.randomUUID(); // UUID | The identifier of the file.
        Integer sasValidityInSeconds = 56; // Integer | The duration in seconds that an SAS url should be valid. The default duration is 12 hours. When using BYOS (https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-encryption-of-data-at-rest#bring-your-own-storage-byos-for-customization-and-logging): A value of 0 means that a plain blob URI without SAS token will be generated.
        try {
            ApiResponse<ModelFile> response = apiInstance.datasetsGetFileWithHttpInfo(id, fileId, sasValidityInSeconds);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechDatasetsForModelAdaptationApi#datasetsGetFile");
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
| **id** | **UUID**| The identifier of the dataset. | |
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


## datasetsList

> PaginatedDatasets datasetsList(skip, top, filter)

Gets a list of datasets for the authenticated subscription.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechDatasetsForModelAdaptationApi;

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

        CustomSpeechDatasetsForModelAdaptationApi apiInstance = new CustomSpeechDatasetsForModelAdaptationApi(defaultClient);
        Integer skip = 56; // Integer | Number of datasets that will be skipped.
        Integer top = 56; // Integer | Number of datasets that will be included after skipping.
        String filter = "filter_example"; // String | A filtering expression for selecting a subset of the available datasets.              - Supported properties: displayName, description, createdDateTime, lastActionDateTime, status, locale, kind.              - Operators:                - eq, ne are supported for all properties.                - gt, ge, lt, le are supported for createdDateTime and lastActionDateTime.                - and, or, not are supported.              -Example:               filter=createdDateTime gt 2022-02-01T11:00:00Z and displayName eq 'My dataset'
        try {
            PaginatedDatasets result = apiInstance.datasetsList(skip, top, filter);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechDatasetsForModelAdaptationApi#datasetsList");
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
| **filter** | **String**| A filtering expression for selecting a subset of the available datasets.              - Supported properties: displayName, description, createdDateTime, lastActionDateTime, status, locale, kind.              - Operators:                - eq, ne are supported for all properties.                - gt, ge, lt, le are supported for createdDateTime and lastActionDateTime.                - and, or, not are supported.              -Example:               filter&#x3D;createdDateTime gt 2022-02-01T11:00:00Z and displayName eq &#39;My dataset&#39; | [optional] |

### Return type

[**PaginatedDatasets**](PaginatedDatasets.md)


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

## datasetsListWithHttpInfo

> ApiResponse<PaginatedDatasets> datasetsList datasetsListWithHttpInfo(skip, top, filter)

Gets a list of datasets for the authenticated subscription.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechDatasetsForModelAdaptationApi;

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

        CustomSpeechDatasetsForModelAdaptationApi apiInstance = new CustomSpeechDatasetsForModelAdaptationApi(defaultClient);
        Integer skip = 56; // Integer | Number of datasets that will be skipped.
        Integer top = 56; // Integer | Number of datasets that will be included after skipping.
        String filter = "filter_example"; // String | A filtering expression for selecting a subset of the available datasets.              - Supported properties: displayName, description, createdDateTime, lastActionDateTime, status, locale, kind.              - Operators:                - eq, ne are supported for all properties.                - gt, ge, lt, le are supported for createdDateTime and lastActionDateTime.                - and, or, not are supported.              -Example:               filter=createdDateTime gt 2022-02-01T11:00:00Z and displayName eq 'My dataset'
        try {
            ApiResponse<PaginatedDatasets> response = apiInstance.datasetsListWithHttpInfo(skip, top, filter);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechDatasetsForModelAdaptationApi#datasetsList");
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
| **filter** | **String**| A filtering expression for selecting a subset of the available datasets.              - Supported properties: displayName, description, createdDateTime, lastActionDateTime, status, locale, kind.              - Operators:                - eq, ne are supported for all properties.                - gt, ge, lt, le are supported for createdDateTime and lastActionDateTime.                - and, or, not are supported.              -Example:               filter&#x3D;createdDateTime gt 2022-02-01T11:00:00Z and displayName eq &#39;My dataset&#39; | [optional] |

### Return type

ApiResponse<[**PaginatedDatasets**](PaginatedDatasets.md)>


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


## datasetsListFiles

> PaginatedFiles datasetsListFiles(id, sasValidityInSeconds, skip, top, filter)

Gets the files of the dataset identified by the given ID.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechDatasetsForModelAdaptationApi;

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

        CustomSpeechDatasetsForModelAdaptationApi apiInstance = new CustomSpeechDatasetsForModelAdaptationApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the dataset.
        Integer sasValidityInSeconds = 56; // Integer | The duration in seconds that an SAS url should be valid. The default duration is 12 hours. When using BYOS (https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-encryption-of-data-at-rest#bring-your-own-storage-byos-for-customization-and-logging): A value of 0 means that a plain blob URI without SAS token will be generated.
        Integer skip = 56; // Integer | Number of datasets that will be skipped.
        Integer top = 56; // Integer | Number of datasets that will be included after skipping.
        String filter = "filter_example"; // String | A filtering expression for selecting a subset of the available files.              - Supported properties: name, createdDateTime, kind.              - Operators:                - eq, ne are supported for all properties.                - gt, ge, lt, le are supported for createdDateTime.                - and, or, not are supported.              - Example:                filter=name eq 'myaudio.wav' and kind eq 'Audio'
        try {
            PaginatedFiles result = apiInstance.datasetsListFiles(id, sasValidityInSeconds, skip, top, filter);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechDatasetsForModelAdaptationApi#datasetsListFiles");
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
| **id** | **UUID**| The identifier of the dataset. | |
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

## datasetsListFilesWithHttpInfo

> ApiResponse<PaginatedFiles> datasetsListFiles datasetsListFilesWithHttpInfo(id, sasValidityInSeconds, skip, top, filter)

Gets the files of the dataset identified by the given ID.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechDatasetsForModelAdaptationApi;

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

        CustomSpeechDatasetsForModelAdaptationApi apiInstance = new CustomSpeechDatasetsForModelAdaptationApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the dataset.
        Integer sasValidityInSeconds = 56; // Integer | The duration in seconds that an SAS url should be valid. The default duration is 12 hours. When using BYOS (https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-encryption-of-data-at-rest#bring-your-own-storage-byos-for-customization-and-logging): A value of 0 means that a plain blob URI without SAS token will be generated.
        Integer skip = 56; // Integer | Number of datasets that will be skipped.
        Integer top = 56; // Integer | Number of datasets that will be included after skipping.
        String filter = "filter_example"; // String | A filtering expression for selecting a subset of the available files.              - Supported properties: name, createdDateTime, kind.              - Operators:                - eq, ne are supported for all properties.                - gt, ge, lt, le are supported for createdDateTime.                - and, or, not are supported.              - Example:                filter=name eq 'myaudio.wav' and kind eq 'Audio'
        try {
            ApiResponse<PaginatedFiles> response = apiInstance.datasetsListFilesWithHttpInfo(id, sasValidityInSeconds, skip, top, filter);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechDatasetsForModelAdaptationApi#datasetsListFiles");
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
| **id** | **UUID**| The identifier of the dataset. | |
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


## datasetsListSupportedLocales

> Map<String, List<DatasetKind>> datasetsListSupportedLocales()

Gets a list of supported locales for datasets.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechDatasetsForModelAdaptationApi;

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

        CustomSpeechDatasetsForModelAdaptationApi apiInstance = new CustomSpeechDatasetsForModelAdaptationApi(defaultClient);
        try {
            Map<String, List<DatasetKind>> result = apiInstance.datasetsListSupportedLocales();
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechDatasetsForModelAdaptationApi#datasetsListSupportedLocales");
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

[**Map&lt;String, List&lt;DatasetKind&gt;&gt;**](List.md)


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

## datasetsListSupportedLocalesWithHttpInfo

> ApiResponse<Map<String, List<DatasetKind>>> datasetsListSupportedLocales datasetsListSupportedLocalesWithHttpInfo()

Gets a list of supported locales for datasets.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechDatasetsForModelAdaptationApi;

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

        CustomSpeechDatasetsForModelAdaptationApi apiInstance = new CustomSpeechDatasetsForModelAdaptationApi(defaultClient);
        try {
            ApiResponse<Map<String, List<DatasetKind>>> response = apiInstance.datasetsListSupportedLocalesWithHttpInfo();
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechDatasetsForModelAdaptationApi#datasetsListSupportedLocales");
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

ApiResponse<[**Map&lt;String, List&lt;DatasetKind&gt;&gt;**](List.md)>


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


## datasetsUpdate

> Dataset datasetsUpdate(id, datasetUpdate)

Updates the mutable details of the dataset identified by its ID.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechDatasetsForModelAdaptationApi;

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

        CustomSpeechDatasetsForModelAdaptationApi apiInstance = new CustomSpeechDatasetsForModelAdaptationApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the dataset.
        DatasetUpdate datasetUpdate = new DatasetUpdate(); // DatasetUpdate | The updated values for the dataset.
        try {
            Dataset result = apiInstance.datasetsUpdate(id, datasetUpdate);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechDatasetsForModelAdaptationApi#datasetsUpdate");
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
| **id** | **UUID**| The identifier of the dataset. | |
| **datasetUpdate** | [**DatasetUpdate**](DatasetUpdate.md)| The updated values for the dataset. | |

### Return type

[**Dataset**](Dataset.md)


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

## datasetsUpdateWithHttpInfo

> ApiResponse<Dataset> datasetsUpdate datasetsUpdateWithHttpInfo(id, datasetUpdate)

Updates the mutable details of the dataset identified by its ID.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechDatasetsForModelAdaptationApi;

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

        CustomSpeechDatasetsForModelAdaptationApi apiInstance = new CustomSpeechDatasetsForModelAdaptationApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the dataset.
        DatasetUpdate datasetUpdate = new DatasetUpdate(); // DatasetUpdate | The updated values for the dataset.
        try {
            ApiResponse<Dataset> response = apiInstance.datasetsUpdateWithHttpInfo(id, datasetUpdate);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechDatasetsForModelAdaptationApi#datasetsUpdate");
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
| **id** | **UUID**| The identifier of the dataset. | |
| **datasetUpdate** | [**DatasetUpdate**](DatasetUpdate.md)| The updated values for the dataset. | |

### Return type

ApiResponse<[**Dataset**](Dataset.md)>


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


## datasetsUpload

> Dataset datasetsUpload(displayName, locale, kind, project, description, customProperties, data, email)

Uploads data and creates a new dataset.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechDatasetsForModelAdaptationApi;

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

        CustomSpeechDatasetsForModelAdaptationApi apiInstance = new CustomSpeechDatasetsForModelAdaptationApi(defaultClient);
        String displayName = "displayName_example"; // String | The name of this dataset.
        String locale = "locale_example"; // String | The locale of this dataset.
        String kind = "kind_example"; // String | The kind of the dataset. Possible values are \\\"Language\\\", \\\"Acoustic\\\", \\\"Pronunciation\\\", \\\"AudioFiles\\\", \\\"LanguageMarkdown\\\", \\\"OutputFormatting\\\".
        String project = "project_example"; // String | The optional string representation of the url of a project. If set, the dataset will be associated with that project.
        String description = "description_example"; // String | Optional description of this dataset.
        String customProperties = "customProperties_example"; // String | The optional custom properties of this entity. The maximum allowed key length is 64 characters, the maximum allowed value length is 256 characters and the count of allowed entries is 10.
        File data = new File("/path/to/file"); // File | For acoustic datasets, a zip file containing the audio data and a text file containing the transcriptions for the audio data. For language datasets, a text file containing the language or pronunciation data. Required in both cases.
        String email = "email_example"; // String | An optional string containing the email address to send email notifications to in case the operation completes. The value will be removed after successfully sending the email.
        try {
            Dataset result = apiInstance.datasetsUpload(displayName, locale, kind, project, description, customProperties, data, email);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechDatasetsForModelAdaptationApi#datasetsUpload");
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
| **displayName** | **String**| The name of this dataset. | |
| **locale** | **String**| The locale of this dataset. | |
| **kind** | **String**| The kind of the dataset. Possible values are \\\&quot;Language\\\&quot;, \\\&quot;Acoustic\\\&quot;, \\\&quot;Pronunciation\\\&quot;, \\\&quot;AudioFiles\\\&quot;, \\\&quot;LanguageMarkdown\\\&quot;, \\\&quot;OutputFormatting\\\&quot;. | |
| **project** | **String**| The optional string representation of the url of a project. If set, the dataset will be associated with that project. | [optional] |
| **description** | **String**| Optional description of this dataset. | [optional] |
| **customProperties** | **String**| The optional custom properties of this entity. The maximum allowed key length is 64 characters, the maximum allowed value length is 256 characters and the count of allowed entries is 10. | [optional] |
| **data** | **File**| For acoustic datasets, a zip file containing the audio data and a text file containing the transcriptions for the audio data. For language datasets, a text file containing the language or pronunciation data. Required in both cases. | [optional] |
| **email** | **String**| An optional string containing the email address to send email notifications to in case the operation completes. The value will be removed after successfully sending the email. | [optional] |

### Return type

[**Dataset**](Dataset.md)


### Authorization

[api_key](../README.md#api_key), [token](../README.md#token)

### HTTP request headers

- **Content-Type**: multipart/form-data
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **201** | The response contains information about the entity as payload and its location as header. |  * Location - The location of the created resource. <br>  |
| **0** | An error occurred. |  -  |

## datasetsUploadWithHttpInfo

> ApiResponse<Dataset> datasetsUpload datasetsUploadWithHttpInfo(displayName, locale, kind, project, description, customProperties, data, email)

Uploads data and creates a new dataset.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechDatasetsForModelAdaptationApi;

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

        CustomSpeechDatasetsForModelAdaptationApi apiInstance = new CustomSpeechDatasetsForModelAdaptationApi(defaultClient);
        String displayName = "displayName_example"; // String | The name of this dataset.
        String locale = "locale_example"; // String | The locale of this dataset.
        String kind = "kind_example"; // String | The kind of the dataset. Possible values are \\\"Language\\\", \\\"Acoustic\\\", \\\"Pronunciation\\\", \\\"AudioFiles\\\", \\\"LanguageMarkdown\\\", \\\"OutputFormatting\\\".
        String project = "project_example"; // String | The optional string representation of the url of a project. If set, the dataset will be associated with that project.
        String description = "description_example"; // String | Optional description of this dataset.
        String customProperties = "customProperties_example"; // String | The optional custom properties of this entity. The maximum allowed key length is 64 characters, the maximum allowed value length is 256 characters and the count of allowed entries is 10.
        File data = new File("/path/to/file"); // File | For acoustic datasets, a zip file containing the audio data and a text file containing the transcriptions for the audio data. For language datasets, a text file containing the language or pronunciation data. Required in both cases.
        String email = "email_example"; // String | An optional string containing the email address to send email notifications to in case the operation completes. The value will be removed after successfully sending the email.
        try {
            ApiResponse<Dataset> response = apiInstance.datasetsUploadWithHttpInfo(displayName, locale, kind, project, description, customProperties, data, email);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechDatasetsForModelAdaptationApi#datasetsUpload");
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
| **displayName** | **String**| The name of this dataset. | |
| **locale** | **String**| The locale of this dataset. | |
| **kind** | **String**| The kind of the dataset. Possible values are \\\&quot;Language\\\&quot;, \\\&quot;Acoustic\\\&quot;, \\\&quot;Pronunciation\\\&quot;, \\\&quot;AudioFiles\\\&quot;, \\\&quot;LanguageMarkdown\\\&quot;, \\\&quot;OutputFormatting\\\&quot;. | |
| **project** | **String**| The optional string representation of the url of a project. If set, the dataset will be associated with that project. | [optional] |
| **description** | **String**| Optional description of this dataset. | [optional] |
| **customProperties** | **String**| The optional custom properties of this entity. The maximum allowed key length is 64 characters, the maximum allowed value length is 256 characters and the count of allowed entries is 10. | [optional] |
| **data** | **File**| For acoustic datasets, a zip file containing the audio data and a text file containing the transcriptions for the audio data. For language datasets, a text file containing the language or pronunciation data. Required in both cases. | [optional] |
| **email** | **String**| An optional string containing the email address to send email notifications to in case the operation completes. The value will be removed after successfully sending the email. | [optional] |

### Return type

ApiResponse<[**Dataset**](Dataset.md)>


### Authorization

[api_key](../README.md#api_key), [token](../README.md#token)

### HTTP request headers

- **Content-Type**: multipart/form-data
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **201** | The response contains information about the entity as payload and its location as header. |  * Location - The location of the created resource. <br>  |
| **0** | An error occurred. |  -  |


## datasetsUploadBlock

> void datasetsUploadBlock(id, blockid, body)

Upload a block of data for the dataset. The maximum size of the block is 8MiB.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechDatasetsForModelAdaptationApi;

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

        CustomSpeechDatasetsForModelAdaptationApi apiInstance = new CustomSpeechDatasetsForModelAdaptationApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the dataset.
        String blockid = "blockid_example"; // String | A valid Base64 string value that identifies the block. Prior to encoding, the string must be less than or equal to 64 bytes in size. For a given blob, the length of the value specified for the blockid parameter must be the same size for each block. Note that the Base64 string must be URL-encoded.
        File body = new File("/path/to/file"); // File | 
        try {
            apiInstance.datasetsUploadBlock(id, blockid, body);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechDatasetsForModelAdaptationApi#datasetsUploadBlock");
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
| **id** | **UUID**| The identifier of the dataset. | |
| **blockid** | **String**| A valid Base64 string value that identifies the block. Prior to encoding, the string must be less than or equal to 64 bytes in size. For a given blob, the length of the value specified for the blockid parameter must be the same size for each block. Note that the Base64 string must be URL-encoded. | |
| **body** | **File**|  | |

### Return type


null (empty response body)

### Authorization

[api_key](../README.md#api_key), [token](../README.md#token)

### HTTP request headers

- **Content-Type**: application/octet-stream
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **201** | The data block was uploaded successfully. |  -  |
| **0** | An error occurred. |  -  |

## datasetsUploadBlockWithHttpInfo

> ApiResponse<Void> datasetsUploadBlock datasetsUploadBlockWithHttpInfo(id, blockid, body)

Upload a block of data for the dataset. The maximum size of the block is 8MiB.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechDatasetsForModelAdaptationApi;

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

        CustomSpeechDatasetsForModelAdaptationApi apiInstance = new CustomSpeechDatasetsForModelAdaptationApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the dataset.
        String blockid = "blockid_example"; // String | A valid Base64 string value that identifies the block. Prior to encoding, the string must be less than or equal to 64 bytes in size. For a given blob, the length of the value specified for the blockid parameter must be the same size for each block. Note that the Base64 string must be URL-encoded.
        File body = new File("/path/to/file"); // File | 
        try {
            ApiResponse<Void> response = apiInstance.datasetsUploadBlockWithHttpInfo(id, blockid, body);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechDatasetsForModelAdaptationApi#datasetsUploadBlock");
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
| **id** | **UUID**| The identifier of the dataset. | |
| **blockid** | **String**| A valid Base64 string value that identifies the block. Prior to encoding, the string must be less than or equal to 64 bytes in size. For a given blob, the length of the value specified for the blockid parameter must be the same size for each block. Note that the Base64 string must be URL-encoded. | |
| **body** | **File**|  | |

### Return type


ApiResponse<Void>

### Authorization

[api_key](../README.md#api_key), [token](../README.md#token)

### HTTP request headers

- **Content-Type**: application/octet-stream
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **201** | The data block was uploaded successfully. |  -  |
| **0** | An error occurred. |  -  |

