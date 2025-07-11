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
import java.net.URI;
import java.time.OffsetDateTime;
import java.util.Arrays;
import org.openapitools.client.model.BaseModelLinks;
import org.openapitools.client.model.BaseModelProperties;
import org.openapitools.client.model.Status;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


import org.openapitools.client.ApiClient;
/**
 * BaseModel
 */
@JsonPropertyOrder({
  BaseModel.JSON_PROPERTY_LINKS,
  BaseModel.JSON_PROPERTY_PROPERTIES,
  BaseModel.JSON_PROPERTY_SELF,
  BaseModel.JSON_PROPERTY_LOCALE,
  BaseModel.JSON_PROPERTY_DISPLAY_NAME,
  BaseModel.JSON_PROPERTY_DESCRIPTION,
  BaseModel.JSON_PROPERTY_LAST_ACTION_DATE_TIME,
  BaseModel.JSON_PROPERTY_STATUS,
  BaseModel.JSON_PROPERTY_CREATED_DATE_TIME
})
@javax.annotation.Generated(value = "org.openapitools.codegen.languages.JavaClientCodegen", date = "2025-03-03T10:07:46.057250+01:00[Europe/Berlin]", comments = "Generator version: 7.12.0")
public class BaseModel {
  public static final String JSON_PROPERTY_LINKS = "links";
  @javax.annotation.Nullable
  private BaseModelLinks links;

  public static final String JSON_PROPERTY_PROPERTIES = "properties";
  @javax.annotation.Nullable
  private BaseModelProperties properties;

  public static final String JSON_PROPERTY_SELF = "self";
  @javax.annotation.Nullable
  private URI self;

  public static final String JSON_PROPERTY_LOCALE = "locale";
  @javax.annotation.Nonnull
  private String locale;

  public static final String JSON_PROPERTY_DISPLAY_NAME = "displayName";
  @javax.annotation.Nonnull
  private String displayName;

  public static final String JSON_PROPERTY_DESCRIPTION = "description";
  @javax.annotation.Nullable
  private String description;

  public static final String JSON_PROPERTY_LAST_ACTION_DATE_TIME = "lastActionDateTime";
  @javax.annotation.Nullable
  private OffsetDateTime lastActionDateTime;

  public static final String JSON_PROPERTY_STATUS = "status";
  @javax.annotation.Nullable
  private Status status;

  public static final String JSON_PROPERTY_CREATED_DATE_TIME = "createdDateTime";
  @javax.annotation.Nullable
  private OffsetDateTime createdDateTime;

  public BaseModel() { 
  }

  @JsonCreator
  public BaseModel(
    @JsonProperty(JSON_PROPERTY_SELF) URI self, 
    @JsonProperty(JSON_PROPERTY_LAST_ACTION_DATE_TIME) OffsetDateTime lastActionDateTime, 
    @JsonProperty(JSON_PROPERTY_CREATED_DATE_TIME) OffsetDateTime createdDateTime
  ) {
  this();
    this.self = self;
    this.lastActionDateTime = lastActionDateTime;
    this.createdDateTime = createdDateTime;
  }

  public BaseModel links(@javax.annotation.Nullable BaseModelLinks links) {
    this.links = links;
    return this;
  }

  /**
   * Get links
   * @return links
   */
  @javax.annotation.Nullable
  @JsonProperty(JSON_PROPERTY_LINKS)
  @JsonInclude(value = JsonInclude.Include.USE_DEFAULTS)
  public BaseModelLinks getLinks() {
    return links;
  }


  @JsonProperty(JSON_PROPERTY_LINKS)
  @JsonInclude(value = JsonInclude.Include.USE_DEFAULTS)
  public void setLinks(@javax.annotation.Nullable BaseModelLinks links) {
    this.links = links;
  }


  public BaseModel properties(@javax.annotation.Nullable BaseModelProperties properties) {
    this.properties = properties;
    return this;
  }

  /**
   * Get properties
   * @return properties
   */
  @javax.annotation.Nullable
  @JsonProperty(JSON_PROPERTY_PROPERTIES)
  @JsonInclude(value = JsonInclude.Include.USE_DEFAULTS)
  public BaseModelProperties getProperties() {
    return properties;
  }


  @JsonProperty(JSON_PROPERTY_PROPERTIES)
  @JsonInclude(value = JsonInclude.Include.USE_DEFAULTS)
  public void setProperties(@javax.annotation.Nullable BaseModelProperties properties) {
    this.properties = properties;
  }


  /**
   * The location of this entity.
   * @return self
   */
  @javax.annotation.Nullable
  @JsonProperty(JSON_PROPERTY_SELF)
  @JsonInclude(value = JsonInclude.Include.USE_DEFAULTS)
  public URI getSelf() {
    return self;
  }




  public BaseModel locale(@javax.annotation.Nonnull String locale) {
    this.locale = locale;
    return this;
  }

  /**
   * The locale of the contained data.
   * @return locale
   */
  @javax.annotation.Nonnull
  @JsonProperty(JSON_PROPERTY_LOCALE)
  @JsonInclude(value = JsonInclude.Include.ALWAYS)
  public String getLocale() {
    return locale;
  }


  @JsonProperty(JSON_PROPERTY_LOCALE)
  @JsonInclude(value = JsonInclude.Include.ALWAYS)
  public void setLocale(@javax.annotation.Nonnull String locale) {
    this.locale = locale;
  }


  public BaseModel displayName(@javax.annotation.Nonnull String displayName) {
    this.displayName = displayName;
    return this;
  }

  /**
   * The display name of the object.
   * @return displayName
   */
  @javax.annotation.Nonnull
  @JsonProperty(JSON_PROPERTY_DISPLAY_NAME)
  @JsonInclude(value = JsonInclude.Include.ALWAYS)
  public String getDisplayName() {
    return displayName;
  }


  @JsonProperty(JSON_PROPERTY_DISPLAY_NAME)
  @JsonInclude(value = JsonInclude.Include.ALWAYS)
  public void setDisplayName(@javax.annotation.Nonnull String displayName) {
    this.displayName = displayName;
  }


  public BaseModel description(@javax.annotation.Nullable String description) {
    this.description = description;
    return this;
  }

  /**
   * The description of the object.
   * @return description
   */
  @javax.annotation.Nullable
  @JsonProperty(JSON_PROPERTY_DESCRIPTION)
  @JsonInclude(value = JsonInclude.Include.USE_DEFAULTS)
  public String getDescription() {
    return description;
  }


  @JsonProperty(JSON_PROPERTY_DESCRIPTION)
  @JsonInclude(value = JsonInclude.Include.USE_DEFAULTS)
  public void setDescription(@javax.annotation.Nullable String description) {
    this.description = description;
  }


  /**
   * The time-stamp when the current status was entered.  The time stamp is encoded as ISO 8601 date and time format  (\&quot;YYYY-MM-DDThh:mm:ssZ\&quot;, see https://en.wikipedia.org/wiki/ISO_8601#Combined_date_and_time_representations).
   * @return lastActionDateTime
   */
  @javax.annotation.Nullable
  @JsonProperty(JSON_PROPERTY_LAST_ACTION_DATE_TIME)
  @JsonInclude(value = JsonInclude.Include.USE_DEFAULTS)
  public OffsetDateTime getLastActionDateTime() {
    return lastActionDateTime;
  }




  public BaseModel status(@javax.annotation.Nullable Status status) {
    this.status = status;
    return this;
  }

  /**
   * Get status
   * @return status
   */
  @javax.annotation.Nullable
  @JsonProperty(JSON_PROPERTY_STATUS)
  @JsonInclude(value = JsonInclude.Include.USE_DEFAULTS)
  public Status getStatus() {
    return status;
  }


  @JsonProperty(JSON_PROPERTY_STATUS)
  @JsonInclude(value = JsonInclude.Include.USE_DEFAULTS)
  public void setStatus(@javax.annotation.Nullable Status status) {
    this.status = status;
  }


  /**
   * The time-stamp when the object was created.  The time stamp is encoded as ISO 8601 date and time format  (\&quot;YYYY-MM-DDThh:mm:ssZ\&quot;, see https://en.wikipedia.org/wiki/ISO_8601#Combined_date_and_time_representations).
   * @return createdDateTime
   */
  @javax.annotation.Nullable
  @JsonProperty(JSON_PROPERTY_CREATED_DATE_TIME)
  @JsonInclude(value = JsonInclude.Include.USE_DEFAULTS)
  public OffsetDateTime getCreatedDateTime() {
    return createdDateTime;
  }




  /**
   * Return true if this BaseModel object is equal to o.
   */
  @Override
  public boolean equals(Object o) {
    if (this == o) {
      return true;
    }
    if (o == null || getClass() != o.getClass()) {
      return false;
    }
    BaseModel baseModel = (BaseModel) o;
    return Objects.equals(this.links, baseModel.links) &&
        Objects.equals(this.properties, baseModel.properties) &&
        Objects.equals(this.self, baseModel.self) &&
        Objects.equals(this.locale, baseModel.locale) &&
        Objects.equals(this.displayName, baseModel.displayName) &&
        Objects.equals(this.description, baseModel.description) &&
        Objects.equals(this.lastActionDateTime, baseModel.lastActionDateTime) &&
        Objects.equals(this.status, baseModel.status) &&
        Objects.equals(this.createdDateTime, baseModel.createdDateTime);
  }

  @Override
  public int hashCode() {
    return Objects.hash(links, properties, self, locale, displayName, description, lastActionDateTime, status, createdDateTime);
  }

  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append("class BaseModel {\n");
    sb.append("    links: ").append(toIndentedString(links)).append("\n");
    sb.append("    properties: ").append(toIndentedString(properties)).append("\n");
    sb.append("    self: ").append(toIndentedString(self)).append("\n");
    sb.append("    locale: ").append(toIndentedString(locale)).append("\n");
    sb.append("    displayName: ").append(toIndentedString(displayName)).append("\n");
    sb.append("    description: ").append(toIndentedString(description)).append("\n");
    sb.append("    lastActionDateTime: ").append(toIndentedString(lastActionDateTime)).append("\n");
    sb.append("    status: ").append(toIndentedString(status)).append("\n");
    sb.append("    createdDateTime: ").append(toIndentedString(createdDateTime)).append("\n");
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

    // add `self` to the URL query string
    if (getSelf() != null) {
      joiner.add(String.format("%sself%s=%s", prefix, suffix, ApiClient.urlEncode(ApiClient.valueToString(getSelf()))));
    }

    // add `locale` to the URL query string
    if (getLocale() != null) {
      joiner.add(String.format("%slocale%s=%s", prefix, suffix, ApiClient.urlEncode(ApiClient.valueToString(getLocale()))));
    }

    // add `displayName` to the URL query string
    if (getDisplayName() != null) {
      joiner.add(String.format("%sdisplayName%s=%s", prefix, suffix, ApiClient.urlEncode(ApiClient.valueToString(getDisplayName()))));
    }

    // add `description` to the URL query string
    if (getDescription() != null) {
      joiner.add(String.format("%sdescription%s=%s", prefix, suffix, ApiClient.urlEncode(ApiClient.valueToString(getDescription()))));
    }

    // add `lastActionDateTime` to the URL query string
    if (getLastActionDateTime() != null) {
      joiner.add(String.format("%slastActionDateTime%s=%s", prefix, suffix, ApiClient.urlEncode(ApiClient.valueToString(getLastActionDateTime()))));
    }

    // add `status` to the URL query string
    if (getStatus() != null) {
      joiner.add(String.format("%sstatus%s=%s", prefix, suffix, ApiClient.urlEncode(ApiClient.valueToString(getStatus()))));
    }

    // add `createdDateTime` to the URL query string
    if (getCreatedDateTime() != null) {
      joiner.add(String.format("%screatedDateTime%s=%s", prefix, suffix, ApiClient.urlEncode(ApiClient.valueToString(getCreatedDateTime()))));
    }

    return joiner.toString();
  }

    public static class Builder {

    private BaseModel instance;

    public Builder() {
      this(new BaseModel());
    }

    protected Builder(BaseModel instance) {
      this.instance = instance;
    }

    public BaseModel.Builder links(BaseModelLinks links) {
      this.instance.links = links;
      return this;
    }
    public BaseModel.Builder properties(BaseModelProperties properties) {
      this.instance.properties = properties;
      return this;
    }
    public BaseModel.Builder self(URI self) {
      this.instance.self = self;
      return this;
    }
    public BaseModel.Builder locale(String locale) {
      this.instance.locale = locale;
      return this;
    }
    public BaseModel.Builder displayName(String displayName) {
      this.instance.displayName = displayName;
      return this;
    }
    public BaseModel.Builder description(String description) {
      this.instance.description = description;
      return this;
    }
    public BaseModel.Builder lastActionDateTime(OffsetDateTime lastActionDateTime) {
      this.instance.lastActionDateTime = lastActionDateTime;
      return this;
    }
    public BaseModel.Builder status(Status status) {
      this.instance.status = status;
      return this;
    }
    public BaseModel.Builder createdDateTime(OffsetDateTime createdDateTime) {
      this.instance.createdDateTime = createdDateTime;
      return this;
    }


    /**
    * returns a built BaseModel instance.
    *
    * The builder is not reusable.
    */
    public BaseModel build() {
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
  public static BaseModel.Builder builder() {
    return new BaseModel.Builder();
  }

  /**
  * Create a builder with a shallow copy of this instance.
  */
  public BaseModel.Builder toBuilder() {
    return new BaseModel.Builder()
      .self(getSelf())
      .locale(getLocale())
      .displayName(getDisplayName())
      .description(getDescription())
      .lastActionDateTime(getLastActionDateTime())
      .status(getStatus())
      .createdDateTime(getCreatedDateTime());
  }

}

