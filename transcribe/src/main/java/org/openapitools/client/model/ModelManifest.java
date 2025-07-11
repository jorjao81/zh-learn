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
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.openapitools.client.model.EntityReference;
import org.openapitools.client.model.ModelFile;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


import org.openapitools.client.ApiClient;
/**
 * ModelManifest
 */
@JsonPropertyOrder({
  ModelManifest.JSON_PROPERTY_MODEL,
  ModelManifest.JSON_PROPERTY_MODEL_FILES,
  ModelManifest.JSON_PROPERTY_PROPERTIES
})
@javax.annotation.Generated(value = "org.openapitools.codegen.languages.JavaClientCodegen", date = "2025-03-03T10:07:46.057250+01:00[Europe/Berlin]", comments = "Generator version: 7.12.0")
public class ModelManifest {
  public static final String JSON_PROPERTY_MODEL = "model";
  @javax.annotation.Nonnull
  private EntityReference model;

  public static final String JSON_PROPERTY_MODEL_FILES = "modelFiles";
  @javax.annotation.Nonnull
  private List<ModelFile> modelFiles = new ArrayList<>();

  public static final String JSON_PROPERTY_PROPERTIES = "properties";
  @javax.annotation.Nonnull
  private Map<String, Object> properties = new HashMap<>();

  public ModelManifest() { 
  }

  public ModelManifest model(@javax.annotation.Nonnull EntityReference model) {
    this.model = model;
    return this;
  }

  /**
   * Get model
   * @return model
   */
  @javax.annotation.Nonnull
  @JsonProperty(JSON_PROPERTY_MODEL)
  @JsonInclude(value = JsonInclude.Include.ALWAYS)
  public EntityReference getModel() {
    return model;
  }


  @JsonProperty(JSON_PROPERTY_MODEL)
  @JsonInclude(value = JsonInclude.Include.ALWAYS)
  public void setModel(@javax.annotation.Nonnull EntityReference model) {
    this.model = model;
  }


  public ModelManifest modelFiles(@javax.annotation.Nonnull List<ModelFile> modelFiles) {
    this.modelFiles = modelFiles;
    return this;
  }

  public ModelManifest addModelFilesItem(ModelFile modelFilesItem) {
    if (this.modelFiles == null) {
      this.modelFiles = new ArrayList<>();
    }
    this.modelFiles.add(modelFilesItem);
    return this;
  }

  /**
   * The model files of this model.
   * @return modelFiles
   */
  @javax.annotation.Nonnull
  @JsonProperty(JSON_PROPERTY_MODEL_FILES)
  @JsonInclude(value = JsonInclude.Include.ALWAYS)
  public List<ModelFile> getModelFiles() {
    return modelFiles;
  }


  @JsonProperty(JSON_PROPERTY_MODEL_FILES)
  @JsonInclude(value = JsonInclude.Include.ALWAYS)
  public void setModelFiles(@javax.annotation.Nonnull List<ModelFile> modelFiles) {
    this.modelFiles = modelFiles;
  }


  public ModelManifest properties(@javax.annotation.Nonnull Map<String, Object> properties) {
    this.properties = properties;
    return this;
  }

  public ModelManifest putPropertiesItem(String key, Object propertiesItem) {
    if (this.properties == null) {
      this.properties = new HashMap<>();
    }
    this.properties.put(key, propertiesItem);
    return this;
  }

  /**
   * The configuration for running this model in a container.
   * @return properties
   */
  @javax.annotation.Nonnull
  @JsonProperty(JSON_PROPERTY_PROPERTIES)
  @JsonInclude(value = JsonInclude.Include.ALWAYS)
  public Map<String, Object> getProperties() {
    return properties;
  }


  @JsonProperty(JSON_PROPERTY_PROPERTIES)
  @JsonInclude(value = JsonInclude.Include.ALWAYS)
  public void setProperties(@javax.annotation.Nonnull Map<String, Object> properties) {
    this.properties = properties;
  }


  /**
   * Return true if this ModelManifest object is equal to o.
   */
  @Override
  public boolean equals(Object o) {
    if (this == o) {
      return true;
    }
    if (o == null || getClass() != o.getClass()) {
      return false;
    }
    ModelManifest modelManifest = (ModelManifest) o;
    return Objects.equals(this.model, modelManifest.model) &&
        Objects.equals(this.modelFiles, modelManifest.modelFiles) &&
        Objects.equals(this.properties, modelManifest.properties);
  }

  @Override
  public int hashCode() {
    return Objects.hash(model, modelFiles, properties);
  }

  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append("class ModelManifest {\n");
    sb.append("    model: ").append(toIndentedString(model)).append("\n");
    sb.append("    modelFiles: ").append(toIndentedString(modelFiles)).append("\n");
    sb.append("    properties: ").append(toIndentedString(properties)).append("\n");
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

    // add `model` to the URL query string
    if (getModel() != null) {
      joiner.add(getModel().toUrlQueryString(prefix + "model" + suffix));
    }

    // add `modelFiles` to the URL query string
    if (getModelFiles() != null) {
      for (int i = 0; i < getModelFiles().size(); i++) {
        if (getModelFiles().get(i) != null) {
          joiner.add(getModelFiles().get(i).toUrlQueryString(String.format("%smodelFiles%s%s", prefix, suffix,
          "".equals(suffix) ? "" : String.format("%s%d%s", containerPrefix, i, containerSuffix))));
        }
      }
    }

    // add `properties` to the URL query string
    if (getProperties() != null) {
      for (String _key : getProperties().keySet()) {
        joiner.add(String.format("%sproperties%s%s=%s", prefix, suffix,
            "".equals(suffix) ? "" : String.format("%s%d%s", containerPrefix, _key, containerSuffix),
            getProperties().get(_key), ApiClient.urlEncode(ApiClient.valueToString(getProperties().get(_key)))));
      }
    }

    return joiner.toString();
  }

    public static class Builder {

    private ModelManifest instance;

    public Builder() {
      this(new ModelManifest());
    }

    protected Builder(ModelManifest instance) {
      this.instance = instance;
    }

    public ModelManifest.Builder model(EntityReference model) {
      this.instance.model = model;
      return this;
    }
    public ModelManifest.Builder modelFiles(List<ModelFile> modelFiles) {
      this.instance.modelFiles = modelFiles;
      return this;
    }
    public ModelManifest.Builder properties(Map<String, Object> properties) {
      this.instance.properties = properties;
      return this;
    }


    /**
    * returns a built ModelManifest instance.
    *
    * The builder is not reusable.
    */
    public ModelManifest build() {
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
  public static ModelManifest.Builder builder() {
    return new ModelManifest.Builder();
  }

  /**
  * Create a builder with a shallow copy of this instance.
  */
  public ModelManifest.Builder toBuilder() {
    return new ModelManifest.Builder()
      .model(getModel())
      .modelFiles(getModelFiles())
      .properties(getProperties());
  }

}

