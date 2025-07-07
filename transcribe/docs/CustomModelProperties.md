

# CustomModelProperties


## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**customModelWeightPercent** | **Integer** | The weight of custom model between 1 (1% custom model and 99% base model) and 100 (100% custom model and 0% base model).  When this property is not set, the service chooses a suitable value (get the model to retrieve the selected weight).  Start without using this property. If needed, choose a larger (or smaller) weight to increase (or decrease) the impact of the custom model. |  [optional] |
|**deprecationDates** | [**CustomModelDeprecationDates**](CustomModelDeprecationDates.md) |  |  [optional] |
|**features** | [**CustomModelFeatures**](CustomModelFeatures.md) |  |  [optional] |
|**email** | **String** | The email address to send email notifications to in case the operation completes.  The value will be removed after successfully sending the email. |  [optional] |
|**error** | [**EntityError**](EntityError.md) |  |  [optional] |



