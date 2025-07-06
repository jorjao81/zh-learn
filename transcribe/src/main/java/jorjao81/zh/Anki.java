package jorjao81.zh;

import picocli.CommandLine.Command;
import picocli.CommandLine.Parameters;

import java.util.concurrent.Callable;

@Command(name = "anki", mixinStandardHelpOptions = true, version = "",
        description = "Searches examples of a word")
class Generate implements Callable<Integer> {
    @Parameters(index = "0", description = "The file to upload")
    private String s;

    @Override
    public Integer call() throws Exception { // your business logic goes here...
        
System.out.println("Search for " + s);
        return 0;
    }
}
