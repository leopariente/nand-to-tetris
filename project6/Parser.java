import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;

public class Parser {
    private File file;
    private BufferedReader reader;
    private String currentInstruction;

    public Parser(File file) {
        this.file = file;
        try {
            this.reader = new BufferedReader(new FileReader(file));
            this.advance();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public boolean hasMoreLines() {
        try {
            return this.currentInstruction != null;
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }

    public void advance() {
        try {
            String line = reader.readLine();
            if (line != null) {
                line = line.trim();
                while (line.isEmpty() || line.startsWith("//")) {
                    line = reader.readLine();
                    line = line.trim();
                }
            }
            this.currentInstruction = line;
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public CommandType commandType() {
        if (currentInstruction.startsWith("/")) {
            return null;
        } else if (currentInstruction.startsWith("@")) {
            return CommandType.A_COMMAND;
        } else if (currentInstruction.startsWith("(") && currentInstruction.endsWith(")")) {
            return CommandType.L_COMMAND;
        } else {
            return CommandType.C_COMMAND;
        }
    }

    public String symbol() {
        if (currentInstruction.startsWith("@")) {
            return currentInstruction.substring(1);
        } else if (currentInstruction.startsWith("(") && currentInstruction.endsWith(")")) {
            return currentInstruction.substring(1, currentInstruction.length() - 1);
        }
        return "";
    }

    public boolean isSymbolNumeric(String symbol) {
        try {
            Integer.parseInt(symbol);
            return true;
        } catch (NumberFormatException e) {
            return false;
        }
    }

    public String dest() {
        if (!currentInstruction.contains("=")) {
            return "";
        }
        String destPart = currentInstruction.split("=")[0];
        return destPart.trim();
    }

    public String comp() {
        String compPart;
        if (currentInstruction.contains("=")) {
            compPart = currentInstruction.substring(currentInstruction.indexOf("=") + 1);
        } else {
            compPart = currentInstruction;
        }
        if (compPart.contains(";")) {
            compPart = compPart.substring(0, compPart.indexOf(";"));
        }
        return compPart.trim();
    }

    public String jump() {
        if (!currentInstruction.contains(";")) {
            return "";
        }
        String[] parts = currentInstruction.split(";");
        String jumpPart = parts[parts.length - 1];
        return jumpPart.trim();
    }
}
