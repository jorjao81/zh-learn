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
import org.openapitools.client.model.EntityError;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


import org.openapitools.client.ApiClient;
/**
 * WebHookProperties
 */
@JsonPropertyOrder({
  WebHookProperties.JSON_PROPERTY_ERROR,
  WebHookProperties.JSON_PROPERTY_API_VERSION,
  WebHookProperties.JSON_PROPERTY_SECRET
})
@javax.annotation.Generated(value = "org.openapitools.codegen.languages.JavaClientCodegen", date = "2025-03-03T10:07:46.057250+01:00[Europe/Berlin]", comments = "Generator version: 7.12.0")
public class WebHookProperties {
  public static final String JSON_PROPERTY_ERROR = "error";
  @javax.annotation.Nullable
  private EntityError error;

  public static final String JSON_PROPERTY_API_VERSION = "apiVersion";
  @javax.annotation.Nullable
  private String apiVersion;

  public static final String JSON_PROPERTY_SECRET = "secret";
  @javax.annotation.Nullable
  private String secret;

  public WebHookProperties() { 
  }

  @JsonCreator
  public WebHookProperties(
    @JsonProperty(JSON_PROPERTY_API_VERSION) String apiVersion
  ) {
  this();
    this.apiVersion = apiVersion;
  }

  public WebHookProperties error(@javax.annotation.Nullable EntityError error) {
    this.error = error;
    return this;
  }

  /**
   * Get error
   * @return error
   */
  @javax.annotation.Nullable
  @JsonProperty(JSON_PROPERTY_ERROR)
  @JsonInclude(value = JsonInclude.Include.USE_DEFAULTS)
  public EntityError getError() {
    return error;
  }


  @JsonProperty(JSON_PROPERTY_ERROR)
  @JsonInclude(value = JsonInclude.Include.USE_DEFAULTS)
  public void setError(@javax.annotation.Nullable EntityError error) {
    this.error = error;
  }


  /**
   * The API version the web hook was created in. This defines the shape of the payload in the callbacks.  If the payload type is not supported anymore, because the shape changed and the API version using it is removed (after deprecation),  the web hook will be disabled.
   * @return apiVersion
   */
  @javax.annotation.Nullable
  @JsonProperty(JSON_PROPERTY_API_VERSION)
  @JsonInclude(value = JsonInclude.Include.USE_DEFAULTS)
  public String getApiVersion() {
    return apiVersion;
  }




  public WebHookProperties secret(@javax.annotation.Nullable String secret) {
    this.secret = secret;
    return this;
  }

  /**
   * A secret that will be used to create a SHA256 hash of the payload with the secret as HMAC key.  This hash will be set as X-MicrosoftSpeechServices-Signature header when calling back into the registered URL.
   * @return secret
   */
  @javax.annotation.Nullable
  @JsonProperty(JSON_PROPERTY_SECRET)
  @JsonInclude(value = JsonInclude.Include.USE_DEFAULTS)
  public String getSecret() {
    return secret;
  }


  @JsonProperty(JSON_PROPERTY_SECRET)
  @JsonInclude(value = JsonInclude.Include.USE_DEFAULTS)
  public void setSecret(@javax.annotation.Nullable String secret) {
    this.secret = secret;
  }


  /**
   * Return true if this WebHookProperties object is equal to o.
   */
  @Override
  public boolean equals(Object o) {
    if (this == o) {
      return true;
    }
    if (o == null || getClass() != o.getClass()) {
      return false;
    }
    WebHookProperties webHookProperties = (WebHookProperties) o;
    return Objects.equals(this.error, webHookProperties.error) &&
        Objects.equals(this.apiVersion, webHookProperties.apiVersion) &&
        Objects.equals(this.secret, webHookProperties.secret);
  }

  @Override
  public int hashCode() {
    return Objects.hash(error, apiVersion, secret);
  }

  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append("class WebHookProperties {\n");
    sb.append("    error: ").append(toIndentedString(error)).append("\n");
    sb.append("    apiVersion: ").append(toIndentedString(apiVersion)).append("\n");
    sb.append("    secret: ").append(toIndentedString(secret)).append("\n");
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

    // add `error` to the URL query string
    if (getError() != null) {
      joiner.add(getError().toUrlQueryString(prefix + "error" + suffix));
    }

    // add `apiVersion` to the URL query string
    if (getApiVersion() != null) {
      joiner.add(String.format("%sapiVersion%s=%s", prefix, suffix, ApiClient.urlEncode(ApiClient.valueToString(getApiVersion()))));
    }

    // add `secret` to the URL query string
    if (getSecret() != null) {
      joiner.add(String.format("%ssecret%s=%s", prefix, suffix, ApiClient.urlEncode(ApiClient.valueToString(getSecret()))));
    }

    return joiner.toString();
  }

    public static class Builder {

    private WebHookProperties instance;

    public Builder() {
      this(new WebHookProperties());
    }

    protected Builder(WebHookProperties instance) {
      this.instance = instance;
    }

    public WebHookProperties.Builder error(EntityError error) {
      this.instance.error = error;
      return this;
    }
    public WebHookProperties.Builder apiVersion(String apiVersion) {
      this.instance.apiVersion = apiVersion;
      return this;
    }
    public WebHookProperties.Builder secret(String secret) {
      this.instance.secret = secret;
      return this;
    }


    /**
    * returns a built WebHookProperties instance.
    *
    * The builder is not reusable.
    */
    public WebHookProperties build() {
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
  public static WebHookProperties.Builder builder() {
    return new WebHookProperties.Builder();
  }

  /**
  * Create a builder with a shallow copy of this instance.
  */
  public WebHookProperties.Builder toBuilder() {
    return new WebHookProperties.Builder()
      .error(getError())
      .apiVersion(getApiVersion())
      .secret(getSecret());
  }

}

