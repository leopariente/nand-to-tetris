import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;

public class HackAssembler {
    private Parser parser;
    private Code code;
    private SymbolTable symbolTable;
    private int freeAddress = 16;
    private int pc = 0;

    public HackAssembler(File inputFile) {
        this.code = new Code();
        this.symbolTable = new SymbolTable();
        this.parser = new Parser(inputFile);
    }

    public void assemble() {
        try {
            FileWriter fileWriter = new FileWriter("output.hack");
            BufferedWriter writer = new BufferedWriter(fileWriter);
            while (this.parser.hasMoreLines()) {
                String binaryInstruction = "";
                CommandType commandType = this.parser.commandType();
                System.out.println(" Type: " + commandType);
                if (commandType == CommandType.C_COMMAND) {
                    String dest = this.code.dest(this.parser.dest());
                    String comp = this.code.comp(this.parser.comp());
                    String jump = this.code.jump(this.parser.jump());
                    binaryInstruction = "111" + comp + dest + jump;
                } else if (commandType == CommandType.L_COMMAND) {
                    String symbol = this.parser.symbol();
                    this.symbolTable.addEntry(symbol, pc);
                } else if (commandType == CommandType.A_COMMAND) {
                    if (this.parser.isSymbolNumeric(this.parser.symbol())) {
                        binaryInstruction = Integer.toBinaryString(Integer.parseInt(this.parser.symbol()));
                    } else {
                        String symbol = this.parser.symbol();
                        if (!this.symbolTable.contains(symbol)) {
                            this.symbolTable.addEntry(symbol, freeAddress);
                            freeAddress++;
                        }
                    }
                }
                pc++;
                writer.write(binaryInstruction);
                writer.newLine();
                this.parser.advance();
                writer.flush();
            }
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
