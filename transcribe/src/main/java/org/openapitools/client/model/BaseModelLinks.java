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
import java.util.Arrays;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


import org.openapitools.client.ApiClient;
/**
 * BaseModelLinks
 */
@JsonPropertyOrder({
  BaseModelLinks.JSON_PROPERTY_MANIFEST
})
@javax.annotation.Generated(value = "org.openapitools.codegen.languages.JavaClientCodegen", date = "2025-03-03T10:07:46.057250+01:00[Europe/Berlin]", comments = "Generator version: 7.12.0")
public class BaseModelLinks {
  public static final String JSON_PROPERTY_MANIFEST = "manifest";
  @javax.annotation.Nullable
  private URI manifest;

  public BaseModelLinks() { 
  }

  @JsonCreator
  public BaseModelLinks(
    @JsonProperty(JSON_PROPERTY_MANIFEST) URI manifest
  ) {
  this();
    this.manifest = manifest;
  }

  /**
   * The location to get a manifest for this model to be used in the on-prem container. See operation \&quot;Models_GetCustomModelManifest\&quot; for more details.
   * @return manifest
   */
  @javax.annotation.Nullable
  @JsonProperty(JSON_PROPERTY_MANIFEST)
  @JsonInclude(value = JsonInclude.Include.USE_DEFAULTS)
  public URI getManifest() {
    return manifest;
  }




  /**
   * Return true if this BaseModelLinks object is equal to o.
   */
  @Override
  public boolean equals(Object o) {
    if (this == o) {
      return true;
    }
    if (o == null || getClass() != o.getClass()) {
      return false;
    }
    BaseModelLinks baseModelLinks = (BaseModelLinks) o;
    return Objects.equals(this.manifest, baseModelLinks.manifest);
  }

  @Override
  public int hashCode() {
    return Objects.hash(manifest);
  }

  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append("class BaseModelLinks {\n");
    sb.append("    manifest: ").append(toIndentedString(manifest)).append("\n");
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

    // add `manifest` to the URL query string
    if (getManifest() != null) {
      joiner.add(String.format("%smanifest%s=%s", prefix, suffix, ApiClient.urlEncode(ApiClient.valueToString(getManifest()))));
    }

    return joiner.toString();
  }

    public static class Builder {

    private BaseModelLinks instance;

    public Builder() {
      this(new BaseModelLinks());
    }

    protected Builder(BaseModelLinks instance) {
      this.instance = instance;
    }

    public BaseModelLinks.Builder manifest(URI manifest) {
      this.instance.manifest = manifest;
      return this;
    }


    /**
    * returns a built BaseModelLinks instance.
    *
    * The builder is not reusable.
    */
    public BaseModelLinks build() {
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
  public static BaseModelLinks.Builder builder() {
    return new BaseModelLinks.Builder();
  }

  /**
  * Create a builder with a shallow copy of this instance.
  */
  public BaseModelLinks.Builder toBuilder() {
    return new BaseModelLinks.Builder()
      .manifest(getManifest());
  }

}

