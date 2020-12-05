import java.io.File;  // Import the File class
import java.io.FileNotFoundException;  // Import this class to handle errors
import java.util.HashMap;
import java.util.Scanner; // Import the Scanner class to read text files

public class ReadFile {

    static HashMap<String, Double> parseData(File file) {
        HashMap<String, Double> dataMap = new HashMap<>();
        try {
            Scanner myReader = new Scanner(file);
            while (myReader.hasNextLine()) {
                String line = myReader.nextLine().trim().replaceAll("\\s", ",");
                if (!line.contains("Gender")) {
                    double value = 0;
                    if (dataMap.containsKey(line)) {
                        value = dataMap.get(line) + 1;
                        dataMap.put(line, value);
                    }else {
                        dataMap.put(line, 1.0);
                    }
                }
            }
            myReader.close();
        } catch (FileNotFoundException e) {
            System.out.println("An error occurred.");
            e.printStackTrace();
        }
        return dataMap;
    }

}