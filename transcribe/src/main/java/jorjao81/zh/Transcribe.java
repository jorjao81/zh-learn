package jorjao81.zh;

import com.azure.storage.blob.BlobClient;
import com.azure.storage.blob.BlobContainerClient;
import com.azure.storage.blob.BlobServiceClient;
import com.azure.storage.blob.BlobServiceClientBuilder;
import picocli.CommandLine.Command;
import picocli.CommandLine.Option;
import picocli.CommandLine.Parameters;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.List;
import java.util.concurrent.Callable;

@Command(name = "search", mixinStandardHelpOptions = true, version = "",
        description = "Searches examples of a word")
class Search implements Callable<Integer> {
    @Parameters(index = "0", description = "The file to upload")
    private String s;

    @Override
    public Integer call() throws Exception { // your business logic goes here...
        
System.out.println("Search for " + s);
        return 0;
    }
}
