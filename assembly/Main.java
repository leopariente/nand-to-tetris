import java.io.File;

public class Main {
    public static void main(String[] args) {
        File inputFile = new File(args[0]);
        HackAssembler assembler = new HackAssembler(inputFile);
        assembler.assemble();
    }
}
