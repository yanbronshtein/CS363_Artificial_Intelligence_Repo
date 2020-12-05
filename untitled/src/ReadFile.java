import java.io.File;  // Import the File class
import java.io.FileNotFoundException;  // Import this class to handle errors
import java.util.HashMap;
import java.util.Scanner; // Import the Scanner class to read text files

public class ReadFile {

    private static HashMap<String, Integer> parseData(File file) {
        HashMap<String, Integer> dataMap = new HashMap<>();
        try {
            Scanner myReader = new Scanner(file);
            while (myReader.hasNextLine()) {
                String line = myReader.nextLine();
                String[] tokenized_Line = line.trim().split("\\s+");
                if (!tokenized_Line[0].equals("Gender")) {
                    DataSetObj temp = new DataSetObj(tokenized_Line[0], tokenized_Line[1], tokenized_Line[2]);
                    int frequency = 0;
                    String tupleStr = temp.tupleStr;

                    if (dataMap.containsKey(tupleStr)) {
                        frequency = dataMap.get(tupleStr) + 1;
                        dataMap.put(tupleStr, frequency);
                    } else {
                        dataMap.put(tupleStr, 1);
                    }
                    System.out.println(frequency);
                }
            }
            myReader.close();
        } catch (FileNotFoundException e) {
            System.out.println("An error occurred.");
            e.printStackTrace();
        }
        return dataMap;
    }
    public static void main(String[] args) {

        parseData(new File("hw2dataset_10.txt"));
//        testMethod()
    }


    /**
     * This method teaches you how to code
     *
     * @param a yoyo var
     * @param b asdfasdf
     * @param casdfasdfasdfasdf
     * @param d asdfasdfasdfasdfasdf
     * @return dfasdfsasdfasdf
     */
    private static int testMethod(int a, int b, int c, int d) {
        return 3;
    }
}