# CustomSpeechModelsApi

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**modelsAuthorizeCopy**](CustomSpeechModelsApi.md#modelsAuthorizeCopy) | **POST** /models:authorizecopy | Allows another speech resource (source) to copy a model to this speech resource (target). |
| [**modelsAuthorizeCopyWithHttpInfo**](CustomSpeechModelsApi.md#modelsAuthorizeCopyWithHttpInfo) | **POST** /models:authorizecopy | Allows another speech resource (source) to copy a model to this speech resource (target). |
| [**modelsCopy**](CustomSpeechModelsApi.md#modelsCopy) | **POST** /models/{id}:copy | Copies a model from one subscription to another. |
| [**modelsCopyWithHttpInfo**](CustomSpeechModelsApi.md#modelsCopyWithHttpInfo) | **POST** /models/{id}:copy | Copies a model from one subscription to another. |
| [**modelsCreate**](CustomSpeechModelsApi.md#modelsCreate) | **POST** /models | Creates a new model. |
| [**modelsCreateWithHttpInfo**](CustomSpeechModelsApi.md#modelsCreateWithHttpInfo) | **POST** /models | Creates a new model. |
| [**modelsDelete**](CustomSpeechModelsApi.md#modelsDelete) | **DELETE** /models/{id} | Deletes the model identified by the given ID. |
| [**modelsDeleteWithHttpInfo**](CustomSpeechModelsApi.md#modelsDeleteWithHttpInfo) | **DELETE** /models/{id} | Deletes the model identified by the given ID. |
| [**modelsGetBaseModel**](CustomSpeechModelsApi.md#modelsGetBaseModel) | **GET** /models/base/{id} | Gets the base model identified by the given ID. |
| [**modelsGetBaseModelWithHttpInfo**](CustomSpeechModelsApi.md#modelsGetBaseModelWithHttpInfo) | **GET** /models/base/{id} | Gets the base model identified by the given ID. |
| [**modelsGetBaseModelManifest**](CustomSpeechModelsApi.md#modelsGetBaseModelManifest) | **GET** /models/base/{id}/manifest | Returns an manifest for this base model which can be used in an on-premise container. |
| [**modelsGetBaseModelManifestWithHttpInfo**](CustomSpeechModelsApi.md#modelsGetBaseModelManifestWithHttpInfo) | **GET** /models/base/{id}/manifest | Returns an manifest for this base model which can be used in an on-premise container. |
| [**modelsGetCustomModel**](CustomSpeechModelsApi.md#modelsGetCustomModel) | **GET** /models/{id} | Gets the model identified by the given ID. |
| [**modelsGetCustomModelWithHttpInfo**](CustomSpeechModelsApi.md#modelsGetCustomModelWithHttpInfo) | **GET** /models/{id} | Gets the model identified by the given ID. |
| [**modelsGetCustomModelManifest**](CustomSpeechModelsApi.md#modelsGetCustomModelManifest) | **GET** /models/{id}/manifest | Returns an manifest for this model which can be used in an on-premise container. |
| [**modelsGetCustomModelManifestWithHttpInfo**](CustomSpeechModelsApi.md#modelsGetCustomModelManifestWithHttpInfo) | **GET** /models/{id}/manifest | Returns an manifest for this model which can be used in an on-premise container. |
| [**modelsGetFile**](CustomSpeechModelsApi.md#modelsGetFile) | **GET** /models/{id}/files/{fileId} | Gets one specific file (identified with fileId) from a model (identified with id). |
| [**modelsGetFileWithHttpInfo**](CustomSpeechModelsApi.md#modelsGetFileWithHttpInfo) | **GET** /models/{id}/files/{fileId} | Gets one specific file (identified with fileId) from a model (identified with id). |
| [**modelsListBaseModels**](CustomSpeechModelsApi.md#modelsListBaseModels) | **GET** /models/base | Gets the list of base models for the authenticated subscription. |
| [**modelsListBaseModelsWithHttpInfo**](CustomSpeechModelsApi.md#modelsListBaseModelsWithHttpInfo) | **GET** /models/base | Gets the list of base models for the authenticated subscription. |
| [**modelsListCustomModels**](CustomSpeechModelsApi.md#modelsListCustomModels) | **GET** /models | Gets the list of custom models for the authenticated subscription. |
| [**modelsListCustomModelsWithHttpInfo**](CustomSpeechModelsApi.md#modelsListCustomModelsWithHttpInfo) | **GET** /models | Gets the list of custom models for the authenticated subscription. |
| [**modelsListFiles**](CustomSpeechModelsApi.md#modelsListFiles) | **GET** /models/{id}/files | Gets the files of the model identified by the given ID. |
| [**modelsListFilesWithHttpInfo**](CustomSpeechModelsApi.md#modelsListFilesWithHttpInfo) | **GET** /models/{id}/files | Gets the files of the model identified by the given ID. |
| [**modelsListSupportedLocales**](CustomSpeechModelsApi.md#modelsListSupportedLocales) | **GET** /models/locales | Gets a list of supported locales for model adaptation. |
| [**modelsListSupportedLocalesWithHttpInfo**](CustomSpeechModelsApi.md#modelsListSupportedLocalesWithHttpInfo) | **GET** /models/locales | Gets a list of supported locales for model adaptation. |
| [**modelsUpdate**](CustomSpeechModelsApi.md#modelsUpdate) | **PATCH** /models/{id} | Updates the metadata of the model identified by the given ID. |
| [**modelsUpdateWithHttpInfo**](CustomSpeechModelsApi.md#modelsUpdateWithHttpInfo) | **PATCH** /models/{id} | Updates the metadata of the model identified by the given ID. |



## modelsAuthorizeCopy

> ModelCopyAuthorization modelsAuthorizeCopy(modelCopyAuthorizationDefinition)

Allows another speech resource (source) to copy a model to this speech resource (target).

This method can be used to allow copying a model from another speech resource.  Only custom models can be copied from another speech resource.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechModelsApi;

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

        CustomSpeechModelsApi apiInstance = new CustomSpeechModelsApi(defaultClient);
        ModelCopyAuthorizationDefinition modelCopyAuthorizationDefinition = new ModelCopyAuthorizationDefinition(); // ModelCopyAuthorizationDefinition | The body contains the Azure Resource ID of the source speech resource.
        try {
            ModelCopyAuthorization result = apiInstance.modelsAuthorizeCopy(modelCopyAuthorizationDefinition);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechModelsApi#modelsAuthorizeCopy");
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
| **modelCopyAuthorizationDefinition** | [**ModelCopyAuthorizationDefinition**](ModelCopyAuthorizationDefinition.md)| The body contains the Azure Resource ID of the source speech resource. | |

### Return type

[**ModelCopyAuthorization**](ModelCopyAuthorization.md)


### Authorization

[api_key](../README.md#api_key), [token](../README.md#token)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | The response contains information about the entity as payload and its location as header. |  -  |
| **0** | An error occurred. |  -  |

## modelsAuthorizeCopyWithHttpInfo

> ApiResponse<ModelCopyAuthorization> modelsAuthorizeCopy modelsAuthorizeCopyWithHttpInfo(modelCopyAuthorizationDefinition)

Allows another speech resource (source) to copy a model to this speech resource (target).

This method can be used to allow copying a model from another speech resource.  Only custom models can be copied from another speech resource.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechModelsApi;

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

        CustomSpeechModelsApi apiInstance = new CustomSpeechModelsApi(defaultClient);
        ModelCopyAuthorizationDefinition modelCopyAuthorizationDefinition = new ModelCopyAuthorizationDefinition(); // ModelCopyAuthorizationDefinition | The body contains the Azure Resource ID of the source speech resource.
        try {
            ApiResponse<ModelCopyAuthorization> response = apiInstance.modelsAuthorizeCopyWithHttpInfo(modelCopyAuthorizationDefinition);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechModelsApi#modelsAuthorizeCopy");
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
| **modelCopyAuthorizationDefinition** | [**ModelCopyAuthorizationDefinition**](ModelCopyAuthorizationDefinition.md)| The body contains the Azure Resource ID of the source speech resource. | |

### Return type

ApiResponse<[**ModelCopyAuthorization**](ModelCopyAuthorization.md)>


### Authorization

[api_key](../README.md#api_key), [token](../README.md#token)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | The response contains information about the entity as payload and its location as header. |  -  |
| **0** | An error occurred. |  -  |


## modelsCopy

> Operation modelsCopy(id, modelCopyAuthorization)

Copies a model from one subscription to another.

This method can be used to copy a model from this speech resource to a target one.  The authorization is obtained on the target speech resource.  Only custom models can be copied to another speech resource.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechModelsApi;

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

        CustomSpeechModelsApi apiInstance = new CustomSpeechModelsApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the model that will be copied.
        ModelCopyAuthorization modelCopyAuthorization = new ModelCopyAuthorization(); // ModelCopyAuthorization | The body contains the authorization to copy to the target speech resource.
        try {
            Operation result = apiInstance.modelsCopy(id, modelCopyAuthorization);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechModelsApi#modelsCopy");
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
| **id** | **UUID**| The identifier of the model that will be copied. | |
| **modelCopyAuthorization** | [**ModelCopyAuthorization**](ModelCopyAuthorization.md)| The body contains the authorization to copy to the target speech resource. | |

### Return type

[**Operation**](Operation.md)


### Authorization

[api_key](../README.md#api_key), [token](../README.md#token)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **202** | The response contains information about the entity as payload and its location as header. |  * Retry-After - The minimum number of seconds to wait before accessing the resource created in this operation. <br>  * Operation-Location - The location of the operation to track progress. <br>  |
| **0** | An error occurred. |  -  |

## modelsCopyWithHttpInfo

> ApiResponse<Operation> modelsCopy modelsCopyWithHttpInfo(id, modelCopyAuthorization)

Copies a model from one subscription to another.

This method can be used to copy a model from this speech resource to a target one.  The authorization is obtained on the target speech resource.  Only custom models can be copied to another speech resource.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechModelsApi;

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

        CustomSpeechModelsApi apiInstance = new CustomSpeechModelsApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the model that will be copied.
        ModelCopyAuthorization modelCopyAuthorization = new ModelCopyAuthorization(); // ModelCopyAuthorization | The body contains the authorization to copy to the target speech resource.
        try {
            ApiResponse<Operation> response = apiInstance.modelsCopyWithHttpInfo(id, modelCopyAuthorization);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechModelsApi#modelsCopy");
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
| **id** | **UUID**| The identifier of the model that will be copied. | |
| **modelCopyAuthorization** | [**ModelCopyAuthorization**](ModelCopyAuthorization.md)| The body contains the authorization to copy to the target speech resource. | |

### Return type

ApiResponse<[**Operation**](Operation.md)>


### Authorization

[api_key](../README.md#api_key), [token](../README.md#token)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **202** | The response contains information about the entity as payload and its location as header. |  * Retry-After - The minimum number of seconds to wait before accessing the resource created in this operation. <br>  * Operation-Location - The location of the operation to track progress. <br>  |
| **0** | An error occurred. |  -  |


## modelsCreate

> CustomModel modelsCreate(model)

Creates a new model.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechModelsApi;

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

        CustomSpeechModelsApi apiInstance = new CustomSpeechModelsApi(defaultClient);
        CustomModel model = new CustomModel(); // CustomModel | The details of the new model.
        try {
            CustomModel result = apiInstance.modelsCreate(model);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechModelsApi#modelsCreate");
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
| **model** | [**CustomModel**](CustomModel.md)| The details of the new model. | |

### Return type

[**CustomModel**](CustomModel.md)


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

## modelsCreateWithHttpInfo

> ApiResponse<CustomModel> modelsCreate modelsCreateWithHttpInfo(model)

Creates a new model.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechModelsApi;

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

        CustomSpeechModelsApi apiInstance = new CustomSpeechModelsApi(defaultClient);
        CustomModel model = new CustomModel(); // CustomModel | The details of the new model.
        try {
            ApiResponse<CustomModel> response = apiInstance.modelsCreateWithHttpInfo(model);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechModelsApi#modelsCreate");
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
| **model** | [**CustomModel**](CustomModel.md)| The details of the new model. | |

### Return type

ApiResponse<[**CustomModel**](CustomModel.md)>


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


## modelsDelete

> void modelsDelete(id)

Deletes the model identified by the given ID.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechModelsApi;

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

        CustomSpeechModelsApi apiInstance = new CustomSpeechModelsApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the model.
        try {
            apiInstance.modelsDelete(id);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechModelsApi#modelsDelete");
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
| **id** | **UUID**| The identifier of the model. | |

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
| **204** | The model was successfully deleted or did not exist. |  -  |
| **0** | An error occurred. |  -  |

## modelsDeleteWithHttpInfo

> ApiResponse<Void> modelsDelete modelsDeleteWithHttpInfo(id)

Deletes the model identified by the given ID.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechModelsApi;

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

        CustomSpeechModelsApi apiInstance = new CustomSpeechModelsApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the model.
        try {
            ApiResponse<Void> response = apiInstance.modelsDeleteWithHttpInfo(id);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechModelsApi#modelsDelete");
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
| **id** | **UUID**| The identifier of the model. | |

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
| **204** | The model was successfully deleted or did not exist. |  -  |
| **0** | An error occurred. |  -  |


## modelsGetBaseModel

> BaseModel modelsGetBaseModel(id)

Gets the base model identified by the given ID.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechModelsApi;

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

        CustomSpeechModelsApi apiInstance = new CustomSpeechModelsApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the base model.
        try {
            BaseModel result = apiInstance.modelsGetBaseModel(id);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechModelsApi#modelsGetBaseModel");
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
| **id** | **UUID**| The identifier of the base model. | |

### Return type

[**BaseModel**](BaseModel.md)


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

## modelsGetBaseModelWithHttpInfo

> ApiResponse<BaseModel> modelsGetBaseModel modelsGetBaseModelWithHttpInfo(id)

Gets the base model identified by the given ID.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechModelsApi;

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

        CustomSpeechModelsApi apiInstance = new CustomSpeechModelsApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the base model.
        try {
            ApiResponse<BaseModel> response = apiInstance.modelsGetBaseModelWithHttpInfo(id);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechModelsApi#modelsGetBaseModel");
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
| **id** | **UUID**| The identifier of the base model. | |

### Return type

ApiResponse<[**BaseModel**](BaseModel.md)>


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


## modelsGetBaseModelManifest

> ModelManifest modelsGetBaseModelManifest(id, sasValidityInSeconds)

Returns an manifest for this base model which can be used in an on-premise container.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechModelsApi;

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

        CustomSpeechModelsApi apiInstance = new CustomSpeechModelsApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The ID of the model to generate a manifest for.
        Integer sasValidityInSeconds = 56; // Integer | The duration in seconds that an SAS url should be valid. The default duration is 12 hours. When using BYOS (https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-encryption-of-data-at-rest#bring-your-own-storage-byos-for-customization-and-logging): A value of 0 means that a plain blob URI without SAS token will be generated.
        try {
            ModelManifest result = apiInstance.modelsGetBaseModelManifest(id, sasValidityInSeconds);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechModelsApi#modelsGetBaseModelManifest");
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
| **id** | **UUID**| The ID of the model to generate a manifest for. | |
| **sasValidityInSeconds** | **Integer**| The duration in seconds that an SAS url should be valid. The default duration is 12 hours. When using BYOS (https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-encryption-of-data-at-rest#bring-your-own-storage-byos-for-customization-and-logging): A value of 0 means that a plain blob URI without SAS token will be generated. | [optional] |

### Return type

[**ModelManifest**](ModelManifest.md)


### Authorization

[api_key](../README.md#api_key), [token](../README.md#token)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successfully generated a model manifest. |  -  |
| **0** | An error occurred. |  -  |

## modelsGetBaseModelManifestWithHttpInfo

> ApiResponse<ModelManifest> modelsGetBaseModelManifest modelsGetBaseModelManifestWithHttpInfo(id, sasValidityInSeconds)

Returns an manifest for this base model which can be used in an on-premise container.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechModelsApi;

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

        CustomSpeechModelsApi apiInstance = new CustomSpeechModelsApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The ID of the model to generate a manifest for.
        Integer sasValidityInSeconds = 56; // Integer | The duration in seconds that an SAS url should be valid. The default duration is 12 hours. When using BYOS (https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-encryption-of-data-at-rest#bring-your-own-storage-byos-for-customization-and-logging): A value of 0 means that a plain blob URI without SAS token will be generated.
        try {
            ApiResponse<ModelManifest> response = apiInstance.modelsGetBaseModelManifestWithHttpInfo(id, sasValidityInSeconds);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechModelsApi#modelsGetBaseModelManifest");
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
| **id** | **UUID**| The ID of the model to generate a manifest for. | |
| **sasValidityInSeconds** | **Integer**| The duration in seconds that an SAS url should be valid. The default duration is 12 hours. When using BYOS (https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-encryption-of-data-at-rest#bring-your-own-storage-byos-for-customization-and-logging): A value of 0 means that a plain blob URI without SAS token will be generated. | [optional] |

### Return type

ApiResponse<[**ModelManifest**](ModelManifest.md)>


### Authorization

[api_key](../README.md#api_key), [token](../README.md#token)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successfully generated a model manifest. |  -  |
| **0** | An error occurred. |  -  |


## modelsGetCustomModel

> CustomModel modelsGetCustomModel(id)

Gets the model identified by the given ID.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechModelsApi;

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

        CustomSpeechModelsApi apiInstance = new CustomSpeechModelsApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the model.
        try {
            CustomModel result = apiInstance.modelsGetCustomModel(id);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechModelsApi#modelsGetCustomModel");
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
| **id** | **UUID**| The identifier of the model. | |

### Return type

[**CustomModel**](CustomModel.md)


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

## modelsGetCustomModelWithHttpInfo

> ApiResponse<CustomModel> modelsGetCustomModel modelsGetCustomModelWithHttpInfo(id)

Gets the model identified by the given ID.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechModelsApi;

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

        CustomSpeechModelsApi apiInstance = new CustomSpeechModelsApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the model.
        try {
            ApiResponse<CustomModel> response = apiInstance.modelsGetCustomModelWithHttpInfo(id);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechModelsApi#modelsGetCustomModel");
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
| **id** | **UUID**| The identifier of the model. | |

### Return type

ApiResponse<[**CustomModel**](CustomModel.md)>


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


## modelsGetCustomModelManifest

> ModelManifest modelsGetCustomModelManifest(id, sasValidityInSeconds)

Returns an manifest for this model which can be used in an on-premise container.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechModelsApi;

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

        CustomSpeechModelsApi apiInstance = new CustomSpeechModelsApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The ID of the model to generate a manifest for.
        Integer sasValidityInSeconds = 56; // Integer | The duration in seconds that an SAS url should be valid. The default duration is 12 hours. When using BYOS (https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-encryption-of-data-at-rest#bring-your-own-storage-byos-for-customization-and-logging): A value of 0 means that a plain blob URI without SAS token will be generated.
        try {
            ModelManifest result = apiInstance.modelsGetCustomModelManifest(id, sasValidityInSeconds);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechModelsApi#modelsGetCustomModelManifest");
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
| **id** | **UUID**| The ID of the model to generate a manifest for. | |
| **sasValidityInSeconds** | **Integer**| The duration in seconds that an SAS url should be valid. The default duration is 12 hours. When using BYOS (https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-encryption-of-data-at-rest#bring-your-own-storage-byos-for-customization-and-logging): A value of 0 means that a plain blob URI without SAS token will be generated. | [optional] |

### Return type

[**ModelManifest**](ModelManifest.md)


### Authorization

[api_key](../README.md#api_key), [token](../README.md#token)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successfully generated a model manifest. |  -  |
| **0** | An error occurred. |  -  |

## modelsGetCustomModelManifestWithHttpInfo

> ApiResponse<ModelManifest> modelsGetCustomModelManifest modelsGetCustomModelManifestWithHttpInfo(id, sasValidityInSeconds)

Returns an manifest for this model which can be used in an on-premise container.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechModelsApi;

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

        CustomSpeechModelsApi apiInstance = new CustomSpeechModelsApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The ID of the model to generate a manifest for.
        Integer sasValidityInSeconds = 56; // Integer | The duration in seconds that an SAS url should be valid. The default duration is 12 hours. When using BYOS (https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-encryption-of-data-at-rest#bring-your-own-storage-byos-for-customization-and-logging): A value of 0 means that a plain blob URI without SAS token will be generated.
        try {
            ApiResponse<ModelManifest> response = apiInstance.modelsGetCustomModelManifestWithHttpInfo(id, sasValidityInSeconds);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechModelsApi#modelsGetCustomModelManifest");
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
| **id** | **UUID**| The ID of the model to generate a manifest for. | |
| **sasValidityInSeconds** | **Integer**| The duration in seconds that an SAS url should be valid. The default duration is 12 hours. When using BYOS (https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-encryption-of-data-at-rest#bring-your-own-storage-byos-for-customization-and-logging): A value of 0 means that a plain blob URI without SAS token will be generated. | [optional] |

### Return type

ApiResponse<[**ModelManifest**](ModelManifest.md)>


### Authorization

[api_key](../README.md#api_key), [token](../README.md#token)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successfully generated a model manifest. |  -  |
| **0** | An error occurred. |  -  |


## modelsGetFile

> ModelFile modelsGetFile(id, fileId, sasValidityInSeconds)

Gets one specific file (identified with fileId) from a model (identified with id).

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechModelsApi;

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

        CustomSpeechModelsApi apiInstance = new CustomSpeechModelsApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the model.
        UUID fileId = UUID.randomUUID(); // UUID | The identifier of the file.
        Integer sasValidityInSeconds = 56; // Integer | The duration in seconds that an SAS url should be valid. The default duration is 12 hours. When using BYOS (https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-encryption-of-data-at-rest#bring-your-own-storage-byos-for-customization-and-logging): A value of 0 means that a plain blob URI without SAS token will be generated.
        try {
            ModelFile result = apiInstance.modelsGetFile(id, fileId, sasValidityInSeconds);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechModelsApi#modelsGetFile");
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
| **id** | **UUID**| The identifier of the model. | |
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

## modelsGetFileWithHttpInfo

> ApiResponse<ModelFile> modelsGetFile modelsGetFileWithHttpInfo(id, fileId, sasValidityInSeconds)

Gets one specific file (identified with fileId) from a model (identified with id).

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechModelsApi;

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

        CustomSpeechModelsApi apiInstance = new CustomSpeechModelsApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the model.
        UUID fileId = UUID.randomUUID(); // UUID | The identifier of the file.
        Integer sasValidityInSeconds = 56; // Integer | The duration in seconds that an SAS url should be valid. The default duration is 12 hours. When using BYOS (https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-encryption-of-data-at-rest#bring-your-own-storage-byos-for-customization-and-logging): A value of 0 means that a plain blob URI without SAS token will be generated.
        try {
            ApiResponse<ModelFile> response = apiInstance.modelsGetFileWithHttpInfo(id, fileId, sasValidityInSeconds);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechModelsApi#modelsGetFile");
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
| **id** | **UUID**| The identifier of the model. | |
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


## modelsListBaseModels

> PaginatedBaseModels modelsListBaseModels(skip, top, filter)

Gets the list of base models for the authenticated subscription.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechModelsApi;

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

        CustomSpeechModelsApi apiInstance = new CustomSpeechModelsApi(defaultClient);
        Integer skip = 56; // Integer | Number of datasets that will be skipped.
        Integer top = 56; // Integer | Number of datasets that will be included after skipping.
        String filter = "filter_example"; // String | A filtering expression for selecting a subset of the available base models.              - Supported properties: displayName, description, createdDateTime, lastActionDateTime, status, locale.              - Operators:                - eq, ne are supported for all properties.                - gt, ge, lt, le are supported for createdDateTime and lastActionDateTime.                - and, or, not are supported.              - Example:                filter=status eq 'NotStarted' or status eq 'Running'
        try {
            PaginatedBaseModels result = apiInstance.modelsListBaseModels(skip, top, filter);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechModelsApi#modelsListBaseModels");
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
| **filter** | **String**| A filtering expression for selecting a subset of the available base models.              - Supported properties: displayName, description, createdDateTime, lastActionDateTime, status, locale.              - Operators:                - eq, ne are supported for all properties.                - gt, ge, lt, le are supported for createdDateTime and lastActionDateTime.                - and, or, not are supported.              - Example:                filter&#x3D;status eq &#39;NotStarted&#39; or status eq &#39;Running&#39; | [optional] |

### Return type

[**PaginatedBaseModels**](PaginatedBaseModels.md)


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

## modelsListBaseModelsWithHttpInfo

> ApiResponse<PaginatedBaseModels> modelsListBaseModels modelsListBaseModelsWithHttpInfo(skip, top, filter)

Gets the list of base models for the authenticated subscription.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechModelsApi;

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

        CustomSpeechModelsApi apiInstance = new CustomSpeechModelsApi(defaultClient);
        Integer skip = 56; // Integer | Number of datasets that will be skipped.
        Integer top = 56; // Integer | Number of datasets that will be included after skipping.
        String filter = "filter_example"; // String | A filtering expression for selecting a subset of the available base models.              - Supported properties: displayName, description, createdDateTime, lastActionDateTime, status, locale.              - Operators:                - eq, ne are supported for all properties.                - gt, ge, lt, le are supported for createdDateTime and lastActionDateTime.                - and, or, not are supported.              - Example:                filter=status eq 'NotStarted' or status eq 'Running'
        try {
            ApiResponse<PaginatedBaseModels> response = apiInstance.modelsListBaseModelsWithHttpInfo(skip, top, filter);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechModelsApi#modelsListBaseModels");
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
| **filter** | **String**| A filtering expression for selecting a subset of the available base models.              - Supported properties: displayName, description, createdDateTime, lastActionDateTime, status, locale.              - Operators:                - eq, ne are supported for all properties.                - gt, ge, lt, le are supported for createdDateTime and lastActionDateTime.                - and, or, not are supported.              - Example:                filter&#x3D;status eq &#39;NotStarted&#39; or status eq &#39;Running&#39; | [optional] |

### Return type

ApiResponse<[**PaginatedBaseModels**](PaginatedBaseModels.md)>


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


## modelsListCustomModels

> PaginatedCustomModels modelsListCustomModels(skip, top, filter)

Gets the list of custom models for the authenticated subscription.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechModelsApi;

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

        CustomSpeechModelsApi apiInstance = new CustomSpeechModelsApi(defaultClient);
        Integer skip = 56; // Integer | Number of datasets that will be skipped.
        Integer top = 56; // Integer | Number of datasets that will be included after skipping.
        String filter = "filter_example"; // String | A filtering expression for selecting a subset of the available models.              - Supported properties: displayName, description, createdDateTime, lastActionDateTime, status, locale.              - Operators:                - eq, ne are supported for all properties.                - gt, ge, lt, le are supported for createdDateTime and lastActionDateTime.                - and, or, not are supported.              - Example:                filter=status eq 'NotStarted' or status eq 'Running'
        try {
            PaginatedCustomModels result = apiInstance.modelsListCustomModels(skip, top, filter);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechModelsApi#modelsListCustomModels");
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
| **filter** | **String**| A filtering expression for selecting a subset of the available models.              - Supported properties: displayName, description, createdDateTime, lastActionDateTime, status, locale.              - Operators:                - eq, ne are supported for all properties.                - gt, ge, lt, le are supported for createdDateTime and lastActionDateTime.                - and, or, not are supported.              - Example:                filter&#x3D;status eq &#39;NotStarted&#39; or status eq &#39;Running&#39; | [optional] |

### Return type

[**PaginatedCustomModels**](PaginatedCustomModels.md)


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

## modelsListCustomModelsWithHttpInfo

> ApiResponse<PaginatedCustomModels> modelsListCustomModels modelsListCustomModelsWithHttpInfo(skip, top, filter)

Gets the list of custom models for the authenticated subscription.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechModelsApi;

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

        CustomSpeechModelsApi apiInstance = new CustomSpeechModelsApi(defaultClient);
        Integer skip = 56; // Integer | Number of datasets that will be skipped.
        Integer top = 56; // Integer | Number of datasets that will be included after skipping.
        String filter = "filter_example"; // String | A filtering expression for selecting a subset of the available models.              - Supported properties: displayName, description, createdDateTime, lastActionDateTime, status, locale.              - Operators:                - eq, ne are supported for all properties.                - gt, ge, lt, le are supported for createdDateTime and lastActionDateTime.                - and, or, not are supported.              - Example:                filter=status eq 'NotStarted' or status eq 'Running'
        try {
            ApiResponse<PaginatedCustomModels> response = apiInstance.modelsListCustomModelsWithHttpInfo(skip, top, filter);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechModelsApi#modelsListCustomModels");
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
| **filter** | **String**| A filtering expression for selecting a subset of the available models.              - Supported properties: displayName, description, createdDateTime, lastActionDateTime, status, locale.              - Operators:                - eq, ne are supported for all properties.                - gt, ge, lt, le are supported for createdDateTime and lastActionDateTime.                - and, or, not are supported.              - Example:                filter&#x3D;status eq &#39;NotStarted&#39; or status eq &#39;Running&#39; | [optional] |

### Return type

ApiResponse<[**PaginatedCustomModels**](PaginatedCustomModels.md)>


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


## modelsListFiles

> PaginatedFiles modelsListFiles(id, sasValidityInSeconds, skip, top, filter)

Gets the files of the model identified by the given ID.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechModelsApi;

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

        CustomSpeechModelsApi apiInstance = new CustomSpeechModelsApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the model.
        Integer sasValidityInSeconds = 56; // Integer | The duration in seconds that an SAS url should be valid. The default duration is 12 hours. When using BYOS (https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-encryption-of-data-at-rest#bring-your-own-storage-byos-for-customization-and-logging): A value of 0 means that a plain blob URI without SAS token will be generated.
        Integer skip = 56; // Integer | Number of datasets that will be skipped.
        Integer top = 56; // Integer | Number of datasets that will be included after skipping.
        String filter = "filter_example"; // String | A filtering expression for selecting a subset of the available files.              - Supported properties: name, createdDateTime, kind.              - Operators:                - eq, ne are supported for all properties.                - gt, ge, lt, le are supported for createdDateTime.                - and, or, not are supported.              - Example:                filter=name eq 'myaudio.wav' and kind eq 'Audio'
        try {
            PaginatedFiles result = apiInstance.modelsListFiles(id, sasValidityInSeconds, skip, top, filter);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechModelsApi#modelsListFiles");
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
| **id** | **UUID**| The identifier of the model. | |
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

## modelsListFilesWithHttpInfo

> ApiResponse<PaginatedFiles> modelsListFiles modelsListFilesWithHttpInfo(id, sasValidityInSeconds, skip, top, filter)

Gets the files of the model identified by the given ID.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechModelsApi;

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

        CustomSpeechModelsApi apiInstance = new CustomSpeechModelsApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the model.
        Integer sasValidityInSeconds = 56; // Integer | The duration in seconds that an SAS url should be valid. The default duration is 12 hours. When using BYOS (https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-encryption-of-data-at-rest#bring-your-own-storage-byos-for-customization-and-logging): A value of 0 means that a plain blob URI without SAS token will be generated.
        Integer skip = 56; // Integer | Number of datasets that will be skipped.
        Integer top = 56; // Integer | Number of datasets that will be included after skipping.
        String filter = "filter_example"; // String | A filtering expression for selecting a subset of the available files.              - Supported properties: name, createdDateTime, kind.              - Operators:                - eq, ne are supported for all properties.                - gt, ge, lt, le are supported for createdDateTime.                - and, or, not are supported.              - Example:                filter=name eq 'myaudio.wav' and kind eq 'Audio'
        try {
            ApiResponse<PaginatedFiles> response = apiInstance.modelsListFilesWithHttpInfo(id, sasValidityInSeconds, skip, top, filter);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechModelsApi#modelsListFiles");
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
| **id** | **UUID**| The identifier of the model. | |
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


## modelsListSupportedLocales

> List<String> modelsListSupportedLocales()

Gets a list of supported locales for model adaptation.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechModelsApi;

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

        CustomSpeechModelsApi apiInstance = new CustomSpeechModelsApi(defaultClient);
        try {
            List<String> result = apiInstance.modelsListSupportedLocales();
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechModelsApi#modelsListSupportedLocales");
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

## modelsListSupportedLocalesWithHttpInfo

> ApiResponse<List<String>> modelsListSupportedLocales modelsListSupportedLocalesWithHttpInfo()

Gets a list of supported locales for model adaptation.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechModelsApi;

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

        CustomSpeechModelsApi apiInstance = new CustomSpeechModelsApi(defaultClient);
        try {
            ApiResponse<List<String>> response = apiInstance.modelsListSupportedLocalesWithHttpInfo();
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechModelsApi#modelsListSupportedLocales");
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


## modelsUpdate

> CustomModel modelsUpdate(id, modelUpdate)

Updates the metadata of the model identified by the given ID.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechModelsApi;

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

        CustomSpeechModelsApi apiInstance = new CustomSpeechModelsApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the model.
        ModelUpdate modelUpdate = new ModelUpdate(); // ModelUpdate | The updated values for the model.
        try {
            CustomModel result = apiInstance.modelsUpdate(id, modelUpdate);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechModelsApi#modelsUpdate");
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
| **id** | **UUID**| The identifier of the model. | |
| **modelUpdate** | [**ModelUpdate**](ModelUpdate.md)| The updated values for the model. | |

### Return type

[**CustomModel**](CustomModel.md)


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

## modelsUpdateWithHttpInfo

> ApiResponse<CustomModel> modelsUpdate modelsUpdateWithHttpInfo(id, modelUpdate)

Updates the metadata of the model identified by the given ID.

### Example

```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.CustomSpeechModelsApi;

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

        CustomSpeechModelsApi apiInstance = new CustomSpeechModelsApi(defaultClient);
        UUID id = UUID.randomUUID(); // UUID | The identifier of the model.
        ModelUpdate modelUpdate = new ModelUpdate(); // ModelUpdate | The updated values for the model.
        try {
            ApiResponse<CustomModel> response = apiInstance.modelsUpdateWithHttpInfo(id, modelUpdate);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling CustomSpeechModelsApi#modelsUpdate");
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
| **id** | **UUID**| The identifier of the model. | |
| **modelUpdate** | [**ModelUpdate**](ModelUpdate.md)| The updated values for the model. | |

### Return type

ApiResponse<[**CustomModel**](CustomModel.md)>


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

