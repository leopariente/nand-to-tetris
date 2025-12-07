import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;

public class HackAssembler {
    private File inputFile;
    private Parser parser;
    private Code code;
    private SymbolTable symbolTable;
    private int freeAddress = 16;
    private int pc = 0;

    public HackAssembler(File inputFile) {
        this.code = new Code();
        this.symbolTable = new SymbolTable();
        this.parser = new Parser(inputFile);
        this.inputFile = inputFile;
    }

    public void assemble() {
        while (this.parser.hasMoreLines()) {
            if (parser.getInstruction() == "" || parser.getInstruction().startsWith("/")) {
                this.parser.advance();
                continue;
            }
            if (this.parser.commandType() == CommandType.L_COMMAND) {
                String symbol = this.parser.symbol();
                this.symbolTable.addEntry(symbol, pc);

            } else {
                pc++;
            }
            this.parser.advance();
        }
        this.parser = new Parser(inputFile);
        try {
            FileWriter fileWriter = new FileWriter("output.hack");
            BufferedWriter writer = new BufferedWriter(fileWriter);
            while (this.parser.hasMoreLines()) {
                String binaryInstruction = "";
                CommandType commandType = this.parser.commandType();
                if (commandType == CommandType.C_COMMAND) {
                    binaryInstruction = this.code.parseCCommand(parser.dest(), parser.comp(), parser.jump());
                } else if (commandType == CommandType.L_COMMAND) {
                    this.parser.advance();
                    continue;
                } else if (commandType == CommandType.A_COMMAND) {
                    if (this.parser.isSymbolNumeric(this.parser.symbol())) {
                        binaryInstruction = code.parseACommand(Integer.parseInt(this.parser.symbol()));
                    } else {
                        String symbol = this.parser.symbol();
                        if (!this.symbolTable.contains(symbol)) {
                            this.symbolTable.addEntry(symbol, freeAddress);
                            freeAddress++;
                        }
                        binaryInstruction = code.parseACommand(this.symbolTable.getAddress(symbol));
                    }
                }
                if (!binaryInstruction.isEmpty()) {
                    writer.write(binaryInstruction);
                }
                this.parser.advance();
                if (parser.hasMoreLines()) {
                    writer.newLine();
                }
                writer.flush();
            }
            writer.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        File inputFile = new File(args[0]);
        HackAssembler assembler = new HackAssembler(inputFile);
        assembler.assemble();
    }
}
