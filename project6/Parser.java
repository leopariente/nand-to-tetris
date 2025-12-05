import java.io.FileInputStream;

public class Parser {
    private FileInputStream fileString;

    public Parser(FileInputStream fileString) {
        this.fileString = fileString;
        
    }
    public boolean hasMoreLines() {
        // Implementation here
        return false;
    }
    public void advance() {
        // Implementation here
    }
    public CommandType commandType() {
        // Implementation here
        return null;
    }
    public String symbol() {
        // Implementation here
        return null;
    }
    public String dest() {
        // Implementation here
        return null;
    }
    public String comp() {
        // Implementation here
        return null;
    }
    public String jump() {
        // Implementation here
        return null;
    }
}
