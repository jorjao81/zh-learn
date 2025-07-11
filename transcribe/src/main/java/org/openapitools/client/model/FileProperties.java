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
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


import org.openapitools.client.ApiClient;
/**
 * FileProperties
 */
@JsonPropertyOrder({
  FileProperties.JSON_PROPERTY_SIZE,
  FileProperties.JSON_PROPERTY_DURATION
})
@javax.annotation.Generated(value = "org.openapitools.codegen.languages.JavaClientCodegen", date = "2025-03-03T10:07:46.057250+01:00[Europe/Berlin]", comments = "Generator version: 7.12.0")
public class FileProperties {
  public static final String JSON_PROPERTY_SIZE = "size";
  @javax.annotation.Nullable
  private Long size;

  public static final String JSON_PROPERTY_DURATION = "duration";
  @javax.annotation.Nullable
  private String duration;

  public FileProperties() { 
  }

  @JsonCreator
  public FileProperties(
    @JsonProperty(JSON_PROPERTY_SIZE) Long size, 
    @JsonProperty(JSON_PROPERTY_DURATION) String duration
  ) {
  this();
    this.size = size;
    this.duration = duration;
  }

  /**
   * The size of the data in bytes.
   * @return size
   */
  @javax.annotation.Nullable
  @JsonProperty(JSON_PROPERTY_SIZE)
  @JsonInclude(value = JsonInclude.Include.USE_DEFAULTS)
  public Long getSize() {
    return size;
  }




  /**
   * The duration in case this file is an audio file. The duration is encoded as ISO 8601  duration (\&quot;PnYnMnDTnHnMnS\&quot;, see https://en.wikipedia.org/wiki/ISO_8601#Durations).
   * @return duration
   */
  @javax.annotation.Nullable
  @JsonProperty(JSON_PROPERTY_DURATION)
  @JsonInclude(value = JsonInclude.Include.USE_DEFAULTS)
  public String getDuration() {
    return duration;
  }




  /**
   * Return true if this FileProperties object is equal to o.
   */
  @Override
  public boolean equals(Object o) {
    if (this == o) {
      return true;
    }
    if (o == null || getClass() != o.getClass()) {
      return false;
    }
    FileProperties fileProperties = (FileProperties) o;
    return Objects.equals(this.size, fileProperties.size) &&
        Objects.equals(this.duration, fileProperties.duration);
  }

  @Override
  public int hashCode() {
    return Objects.hash(size, duration);
  }

  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append("class FileProperties {\n");
    sb.append("    size: ").append(toIndentedString(size)).append("\n");
    sb.append("    duration: ").append(toIndentedString(duration)).append("\n");
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

    // add `size` to the URL query string
    if (getSize() != null) {
      joiner.add(String.format("%ssize%s=%s", prefix, suffix, ApiClient.urlEncode(ApiClient.valueToString(getSize()))));
    }

    // add `duration` to the URL query string
    if (getDuration() != null) {
      joiner.add(String.format("%sduration%s=%s", prefix, suffix, ApiClient.urlEncode(ApiClient.valueToString(getDuration()))));
    }

    return joiner.toString();
  }

    public static class Builder {

    private FileProperties instance;

    public Builder() {
      this(new FileProperties());
    }

    protected Builder(FileProperties instance) {
      this.instance = instance;
    }

    public FileProperties.Builder size(Long size) {
      this.instance.size = size;
      return this;
    }
    public FileProperties.Builder duration(String duration) {
      this.instance.duration = duration;
      return this;
    }


    /**
    * returns a built FileProperties instance.
    *
    * The builder is not reusable.
    */
    public FileProperties build() {
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
  public static FileProperties.Builder builder() {
    return new FileProperties.Builder();
  }

  /**
  * Create a builder with a shallow copy of this instance.
  */
  public FileProperties.Builder toBuilder() {
    return new FileProperties.Builder()
      .size(getSize())
      .duration(getDuration());
  }

}

