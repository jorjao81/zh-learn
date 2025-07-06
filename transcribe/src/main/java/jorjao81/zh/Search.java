package jorjao81.zh;

import com.azure.storage.blob.BlobClient;
import com.azure.storage.blob.BlobContainerClient;
import com.azure.storage.blob.BlobServiceClient;
import com.azure.storage.blob.BlobServiceClientBuilder;
import picocli.CommandLine;
import picocli.CommandLine.Command;
import picocli.CommandLine.Option;
import picocli.CommandLine.Parameters;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.math.BigInteger;
import java.nio.file.Files;
import java.security.MessageDigest;
import java.util.List;
import java.util.concurrent.Callable;

@Command(name = "upload", mixinStandardHelpOptions = true, version = "",
        description = "Uploads audio to AZ storage")
class Upload implements Callable<Integer> {
    @Parameters(index = "0..*", description = "The file to upload")
    private List<File> files;

    @Option(names = {"-f", "--folder"}, description = "The folder to upload to.")
    private String folder = "";

    @Override
    public Integer call() throws Exception { // your business logic goes here...
        
        // Replace with your actual connection string
        String storageAccountKey = System.getenv("AZ_STORAGE_ACCOUNT_KEY_ZH");
        if (storageAccountKey == null) {
            System.err.println("Error: AZ_STORAGE_ACCOUNT_KEY_ZH environment variable not set.");
            return 1;
        }
        // Replace with your actual storage account name
        // read from environment variable export AZ_STORAGE_ACCOUNT_NAME_ZH
        String storageAccountName = System.getenv("AZ_STORAGE_ACCOUNT_NAME_ZH");
        if (storageAccountName == null) {
            System.err.println("Error: AZ_STORAGE_ACCOUNT_NAME_ZH environment variable not set.");
            return 1;
        }
        String connectionString = "DefaultEndpointsProtocol=https;AccountName=" + storageAccountName + ";AccountKey=" + storageAccountKey + ";EndpointSuffix=core.windows.net";
        String containerName = "audio";

        for(File file : files) {
            String blobName = folder + "/" + file.getName();
            uploadBlob(connectionString, containerName, file, blobName);
        }

        return 0;
    }
    public static void uploadBlob(String connectionString, String containerName, File file, String blobName) throws IOException {
        // Create a BlobServiceClient object which will be used to create a container client
        BlobServiceClient blobServiceClient = new BlobServiceClientBuilder()
                .connectionString(connectionString)
                .buildClient();
        // Get a reference to the container
        BlobContainerClient containerClient = blobServiceClient.getBlobContainerClient(containerName);
        // Get a reference to a blob
        BlobClient blobClient = containerClient.getBlobClient(blobName);
        // Create a new file instance from the path
        // Create input stream from file
        InputStream dataStream = new FileInputStream(file);
        // Upload the file to the blob
        System.out.println("Uploading to Blob storage as blob:\n\t" + blobClient.getBlobUrl());
        blobClient.upload(dataStream, file.length(), true); // true means overwrite
        dataStream.close();
        System.out.println("File uploaded successfully!");
    }
}
