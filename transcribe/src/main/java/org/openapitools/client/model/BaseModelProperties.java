/*
 * Speech Services API version 3.2
 * Speech Services API version 3.2.
 *
 * The version of the OpenAPI document: 3.2
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */


package org.openapitools.client.model;

import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.StringJoiner;
import java.util.Objects;
import java.util.Map;
import java.util.HashMap;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonTypeName;
import com.fasterxml.jackson.annotation.JsonValue;
import java.util.Arrays;
import org.openapitools.client.model.BaseModelDeprecationDates;
import org.openapitools.client.model.BaseModelFeatures;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


import org.openapitools.client.ApiClient;
/**
 * BaseModelProperties
 */
@JsonPropertyOrder({
  BaseModelProperties.JSON_PROPERTY_DEPRECATION_DATES,
  BaseModelProperties.JSON_PROPERTY_FEATURES,
  BaseModelProperties.JSON_PROPERTY_CHARGE_FOR_ADAPTATION
})
@javax.annotation.Generated(value = "org.openapitools.codegen.languages.JavaClientCodegen", date = "2025-03-03T10:07:46.057250+01:00[Europe/Berlin]", comments = "Generator version: 7.12.0")
public class BaseModelProperties {
  public static final String JSON_PROPERTY_DEPRECATION_DATES = "deprecationDates";
  @javax.annotation.Nullable
  private BaseModelDeprecationDates deprecationDates;

  public static final String JSON_PROPERTY_FEATURES = "features";
  @javax.annotation.Nullable
  private BaseModelFeatures features;

  public static final String JSON_PROPERTY_CHARGE_FOR_ADAPTATION = "chargeForAdaptation";
  @javax.annotation.Nullable
  private Boolean chargeForAdaptation;

  public BaseModelProperties() { 
  }

  @JsonCreator
  public BaseModelProperties(
    @JsonProperty(JSON_PROPERTY_CHARGE_FOR_ADAPTATION) Boolean chargeForAdaptation
  ) {
  this();
    this.chargeForAdaptation = chargeForAdaptation;
  }

  public BaseModelProperties deprecationDates(@javax.annotation.Nullable BaseModelDeprecationDates deprecationDates) {
    this.deprecationDates = deprecationDates;
    return this;
  }

  /**
   * Get deprecationDates
   * @return deprecationDates
   */
  @javax.annotation.Nullable
  @JsonProperty(JSON_PROPERTY_DEPRECATION_DATES)
  @JsonInclude(value = JsonInclude.Include.USE_DEFAULTS)
  public BaseModelDeprecationDates getDeprecationDates() {
    return deprecationDates;
  }


  @JsonProperty(JSON_PROPERTY_DEPRECATION_DATES)
  @JsonInclude(value = JsonInclude.Include.USE_DEFAULTS)
  public void setDeprecationDates(@javax.annotation.Nullable BaseModelDeprecationDates deprecationDates) {
    this.deprecationDates = deprecationDates;
  }


  public BaseModelProperties features(@javax.annotation.Nullable BaseModelFeatures features) {
    this.features = features;
    return this;
  }

  /**
   * Get features
   * @return features
   */
  @javax.annotation.Nullable
  @JsonProperty(JSON_PROPERTY_FEATURES)
  @JsonInclude(value = JsonInclude.Include.USE_DEFAULTS)
  public BaseModelFeatures getFeatures() {
    return features;
  }


  @JsonProperty(JSON_PROPERTY_FEATURES)
  @JsonInclude(value = JsonInclude.Include.USE_DEFAULTS)
  public void setFeatures(@javax.annotation.Nullable BaseModelFeatures features) {
    this.features = features;
  }


  /**
   * A value indicating whether model adaptation is charged.
   * @return chargeForAdaptation
   */
  @javax.annotation.Nullable
  @JsonProperty(JSON_PROPERTY_CHARGE_FOR_ADAPTATION)
  @JsonInclude(value = JsonInclude.Include.USE_DEFAULTS)
  public Boolean getChargeForAdaptation() {
    return chargeForAdaptation;
  }




  /**
   * Return true if this BaseModelProperties object is equal to o.
   */
  @Override
  public boolean equals(Object o) {
    if (this == o) {
      return true;
    }
    if (o == null || getClass() != o.getClass()) {
      return false;
    }
    BaseModelProperties baseModelProperties = (BaseModelProperties) o;
    return Objects.equals(this.deprecationDates, baseModelProperties.deprecationDates) &&
        Objects.equals(this.features, baseModelProperties.features) &&
        Objects.equals(this.chargeForAdaptation, baseModelProperties.chargeForAdaptation);
  }

  @Override
  public int hashCode() {
    return Objects.hash(deprecationDates, features, chargeForAdaptation);
  }

  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append("class BaseModelProperties {\n");
    sb.append("    deprecationDates: ").append(toIndentedString(deprecationDates)).append("\n");
    sb.append("    features: ").append(toIndentedString(features)).append("\n");
    sb.append("    chargeForAdaptation: ").append(toIndentedString(chargeForAdaptation)).append("\n");
    sb.append("}");
    return sb.toString();
  }

  /**
   * Convert the given object to string with each line indented by 4 spaces
   * (except the first line).
   */
  private String toIndentedString(Object o) {
    if (o == null) {
      return "null";
    }
    return o.toString().replace("\n", "\n    ");
  }

  /**
   * Convert the instance into URL query string.
   *
   * @return URL query string
   */
  public String toUrlQueryString() {
    return toUrlQueryString(null);
  }

  /**
   * Convert the instance into URL query string.
   *
   * @param prefix prefix of the query string
   * @return URL query string
   */
  public String toUrlQueryString(String prefix) {
    String suffix = "";
    String containerSuffix = "";
    String containerPrefix = "";
    if (prefix == null) {
      // style=form, explode=true, e.g. /pet?name=cat&type=manx
      prefix = "";
    } else {
      // deepObject style e.g. /pet?id[name]=cat&id[type]=manx
      prefix = prefix + "[";
      suffix = "]";
      containerSuffix = "]";
      containerPrefix = "[";
    }

    StringJoiner joiner = new StringJoiner("&");

    // add `deprecationDates` to the URL query string
    if (getDeprecationDates() != null) {
      joiner.add(getDeprecationDates().toUrlQueryString(prefix + "deprecationDates" + suffix));
    }

    // add `features` to the URL query string
    if (getFeatures() != null) {
      joiner.add(getFeatures().toUrlQueryString(prefix + "features" + suffix));
    }

    // add `chargeForAdaptation` to the URL query string
    if (getChargeForAdaptation() != null) {
      joiner.add(String.format("%schargeForAdaptation%s=%s", prefix, suffix, ApiClient.urlEncode(ApiClient.valueToString(getChargeForAdaptation()))));
    }

    return joiner.toString();
  }

    public static class Builder {

    private BaseModelProperties instance;

    public Builder() {
      this(new BaseModelProperties());
    }

    protected Builder(BaseModelProperties instance) {
      this.instance = instance;
    }

    public BaseModelProperties.Builder deprecationDates(BaseModelDeprecationDates deprecationDates) {
      this.instance.deprecationDates = deprecationDates;
      return this;
    }
    public BaseModelProperties.Builder features(BaseModelFeatures features) {
      this.instance.features = features;
      return this;
    }
    public BaseModelProperties.Builder chargeForAdaptation(Boolean chargeForAdaptation) {
      this.instance.chargeForAdaptation = chargeForAdaptation;
      return this;
    }


    /**
    * returns a built BaseModelProperties instance.
    *
    * The builder is not reusable.
    */
    public BaseModelProperties build() {
      try {
        return this.instance;
      } finally {
        // ensure that this.instance is not reused
        this.instance = null;
      }
    }

    @Override
    public String toString() {
      return getClass() + "=(" + instance + ")";
    }
  }

  /**
  * Create a builder with no initialized field.
  */
  public static BaseModelProperties.Builder builder() {
    return new BaseModelProperties.Builder();
  }

  /**
  * Create a builder with a shallow copy of this instance.
  */
  public BaseModelProperties.Builder toBuilder() {
    return new BaseModelProperties.Builder()
      .deprecationDates(getDeprecationDates())
      .features(getFeatures())
      .chargeForAdaptation(getChargeForAdaptation());
  }

}

