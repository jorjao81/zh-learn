

# LanguageIdentificationProperties


## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**mode** | **LanguageIdentificationMode** |  |  [optional] |
|**candidateLocales** | **List&lt;String&gt;** | The candidate locales for language identification (example [\&quot;en-US\&quot;, \&quot;de-DE\&quot;, \&quot;es-ES\&quot;]). A minimum of 2 and a maximum of 10 candidate locales, including the main locale for the transcription, is supported for continuous mode. For single language identification, the maximum number of candidate locales is unbounded. |  |
|**speechModelMapping** | [**Map&lt;String, EntityReference&gt;**](EntityReference.md) | An optional mapping of locales to speech model entities. If no model is given for a locale, the default base model is used.  Keys must be locales contained in the candidate locales, values are entities for models of the respective locales. |  [optional] |



