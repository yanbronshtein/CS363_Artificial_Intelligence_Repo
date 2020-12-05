import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.Writer;
import java.util.*;
import java.util.Map.Entry;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class EM {

    public int iterations = 0;
    double threshold;
    public int[] ops = {1, 2, 3, 4, 5};
    public String[] knownData  = new String[10];
    ArrayList<Double> logLikelihood = new ArrayList<>();
    public HashMap<String, Double> thetaMap;
    EM(double gender0, double weight0GivenGender0, double weight0GivenGender1, double height0GivenGender0, double height0GivenGender1, File filename,
       double threshold){
        //default constructor for EM class
        List<Double> logLikelihood = new ArrayList<>();
        this.threshold = threshold;
        knownData[0] = "0,x,x";
        knownData[1] = "1,x,x";
        knownData[2] = "0,0,x";
        knownData[3] = "0,1,x";
        knownData[4] = "1,0,x";
        knownData[5] = "1,1,x";
        knownData[6] = "0,x,0";
        knownData[7] = "0,x,1";
        knownData[8] = "1,x,0";
        knownData[9] = "1,x,1";

        thetaMap = new HashMap<>();
        thetaMap.put(knownData[0], gender0);
        thetaMap.put(knownData[1], 1-gender0);

        thetaMap.put(knownData[2], weight0GivenGender0);
        thetaMap.put(knownData[3], 1-weight0GivenGender0);

        thetaMap.put(knownData[4], weight0GivenGender1);
        thetaMap.put(knownData[5], 1-weight0GivenGender1);

        thetaMap.put(knownData[6], height0GivenGender0);
        thetaMap.put(knownData[7], 1-height0GivenGender0);

        thetaMap.put(knownData[8], height0GivenGender1);
        thetaMap.put(knownData[9], 1-height0GivenGender1);

//        System.out.println(knownValues.get("1,x,1"));

        mStep(filename);
//        thetaMap.forEach((key, value) -> System.out.println(key +" : " + value));
//        System.out.println(initialValues[0].toString().equals("0,x,x"));
//        HashMap<String, Integer> dataMap = ReadFile.parseData(filename);
//        HashMap<String, Integer> expectedData = new HashMap(dataMap);    //contains the current frequencies for tuples
//        expectedData.forEach((key, value) -> System.out.println(key +" : " + value));


    }

    private static HashMap<String, Double> cloneMap(HashMap<String, Double> dataMap) {
        HashMap<String, Double> newMap = new HashMap<>();
        for (Map.Entry<String, Double> entry: dataMap.entrySet()) {
            newMap.put(entry.getKey(), entry.getValue());
        }
        return newMap;

    }

    HashMap<String, Double> eStep(HashMap<String, Double> dataMap){
        HashMap<String, Double> expectedDataMap = cloneMap(dataMap);

        double d = 0, n;

        final String[] entryOptions = {
                "-,1,1",
                "-,1,0",
                "-,0,0",
                "-,0,1"
        };

        for(Map.Entry<String, Double> entry : dataMap.entrySet()) {
            String key = entry.getKey();

            if (key.equals(entryOptions[0])){
                n = thetaMap.get("0,x,x") * thetaMap.get("0,1,x") * thetaMap.get("0,x,1");
                d += thetaMap.get("0,x,x") * thetaMap.get("0,1,x") * thetaMap.get("0,x,1");
                d += thetaMap.get("1,x,x") * thetaMap.get("1,1,x") * thetaMap.get("1,x,1");

                double tempVal = (n/d) * expectedDataMap.get("-,1,1");
                if (expectedDataMap.containsKey("0,1,1")) {
                    expectedDataMap.put("0,1,1", expectedDataMap.get("0,1,1") + tempVal);
                }else {
                    expectedDataMap.put("0,1,1", tempVal);
                }

                tempVal = (1 - (n/d)) * expectedDataMap.get("-,1,1");
                if (expectedDataMap.containsKey("1,1,1")) {

                    expectedDataMap.put("1,1,1", expectedDataMap.get("0,1,1") + tempVal);
                }else {
                    expectedDataMap.put("0,1,1", tempVal);
                }

            }

            else if (key.equals(entryOptions[1])){
                n = thetaMap.get("0,x,x") * thetaMap.get("0,1,x") * thetaMap.get("0,x,0");
                d += thetaMap.get("0,x,x") * thetaMap.get("0,1,x") * thetaMap.get("0,x,0");
                d += thetaMap.get("1,x,x") * thetaMap.get("1,1,x") * thetaMap.get("1,x,0");

                double tempVal = (n/d) * expectedDataMap.get("-,1,0");
                if (expectedDataMap.containsKey("0,1,0")) {
                    expectedDataMap.put("0,1,0", expectedDataMap.get("0,1,1") + tempVal);
                }else {
                    expectedDataMap.put("0,1,0", tempVal);
                }

                double tempVal2 = (1 - (n/d)) * expectedDataMap.get("-,1,0");
                if (expectedDataMap.containsKey("1,1,0")) {

                    expectedDataMap.put("1,1,0", expectedDataMap.get("1,1,1") + tempVal2);
                }else {
                    expectedDataMap.put("1,1,0", tempVal2);
                }

            }
            else if (key.equals(entryOptions[2])){
                n = thetaMap.get("0,x,x") * thetaMap.get("0,0,x") * thetaMap.get("0,x,0");
                d += thetaMap.get("0,x,x") * thetaMap.get("0,0,x") * thetaMap.get("0,x,0");
                d += thetaMap.get("1,x,x") * thetaMap.get("1,0,x") * thetaMap.get("1,x,0");

                double tempVal = (n/d) * expectedDataMap.get("-,0,0");
                if (expectedDataMap.containsKey("0,0,0")) {
                    expectedDataMap.put("0,0,0", expectedDataMap.get("0,0,0") + tempVal);
                }else {
                    expectedDataMap.put("0,0,0", tempVal);
                }

                double tempVal2 = (1 - (n/d)) * expectedDataMap.get("-,0,0");
                if (expectedDataMap.containsKey("1,0,0")) {

                    expectedDataMap.put("1,0,0", expectedDataMap.get("1,0,0") + tempVal2);
                }else {
                    expectedDataMap.put("1,0,0", tempVal2);
                }

            }
//            else if (key.equals(entryOptions[3])) {
            else {
                n = thetaMap.get("0,x,x") * thetaMap.get("0,0,x") * thetaMap.get("0,x,1");
                d += thetaMap.get("0,x,x") * thetaMap.get("0,0,x") * thetaMap.get("0,x,1");
                d += thetaMap.get("1,x,x") * thetaMap.get("1,0,x") * thetaMap.get("1,x,1");

                double tempVal = (n / d) * expectedDataMap.get("-,0,1");
                if (expectedDataMap.containsKey("0,0,1")) {
                    expectedDataMap.put("0,0,1", expectedDataMap.get("0,0,1") + tempVal);
                } else {
                    expectedDataMap.put("0,0,1", tempVal);
                }

                double tempVal2 = (1 - (n / d)) * expectedDataMap.get("-,0,1");
                if (expectedDataMap.containsKey("1,0,1")) {

                    expectedDataMap.put("1,0,1", expectedDataMap.get("1,0,1") + tempVal);
                } else {
                    expectedDataMap.put("1,0,1", tempVal);
                }

            }
        }
        return expectedDataMap;
    }

    void mStep(File filename){
        HashMap<String, Double> dataMap = ReadFile.parseData(filename);
        HashMap<String, Double> expectedData = eStep(dataMap);

        int opIndex = -1;

        HashMap<String, Double> newParamMap = computeNewParams(expectedData, new HashMap<String, Double>(), opIndex);

        iterations ++;

        boolean hasConverged = hasConverged(dataMap, newParamMap);

        if (hasConverged){
            writeToCSV(logLikelihood);
        }
        else{
            mStep(filename);
        }

    }



    private boolean hasConverged(HashMap<String, Double> dataMap,
                                 HashMap<String, Double> newParamMap) {
        double logLikelihoodCurrentParam = 0, logLikelihoodNewParam = 0;

        for (Map.Entry<String, Double> entry: dataMap.entrySet()) {
            String key = entry.getKey();
            String[] tokenizedKeyStr = key.split(",");
            String gender = tokenizedKeyStr[0];
            String weight = tokenizedKeyStr[1];
            String height = tokenizedKeyStr[2];

            double priorProb = 0, newProb = 0;

            if (gender.equals("-")) {
                priorProb += thetaMap.get("0,x,x") * thetaMap.get("0,"+weight+",x") *
                        thetaMap.get("0,x,"+height);
                priorProb += thetaMap.get("1,x,x") * thetaMap.get("0,"+weight+",x") *
                        thetaMap.get("1,x,"+height);

                newProb += newParamMap.get("0,x,x") * newParamMap.get("0," + weight +",x") *
                        thetaMap.get("0,x," + height);

                newProb += newParamMap.get("1,x,x") * newParamMap.get("1," + weight +",x") *
                        newParamMap.get("1,x," + height);

            } else {
                priorProb = thetaMap.get(gender + ",x,x") *
                        thetaMap.get(gender + "," + weight +",x") * thetaMap.get(gender + ",x," +height);
                newProb = newParamMap.get(gender + ",x,x") *
                        newParamMap.get(gender + "," + weight +",x") * newParamMap.get(gender + ",x," +height);

            }
            logLikelihoodCurrentParam += Math.log(priorProb) * dataMap.get(key);
            logLikelihoodNewParam += Math.log(newProb) * dataMap.get(key);

        }
        if (iterations == 1) {
            logLikelihood.add(logLikelihoodCurrentParam);
        }
        logLikelihood.add(logLikelihoodNewParam);

        double diff = Math.abs(logLikelihoodNewParam - logLikelihoodCurrentParam);

        return diff < threshold;
    }

    private HashMap<String, Double> computeNewParams(HashMap<String, Double> expectedDataMap,
                                                     HashMap<String, Double> newParamMap, int opIndex) {
//        HashMap<String, Double> newParams = null;
        double n = 0;
        double d = 0;

        if (opIndex +1 >= ops.length){
            return newParamMap;
        }

        opIndex += 1;



        for(Entry<String, Double> entry : expectedDataMap.entrySet()){
            String key = entry.getKey();
            Double value = entry.getValue();
            String[] tokenizedStr = key.split(",");
            String gender = tokenizedStr[0];
            String weight = tokenizedStr[1];
            String height = tokenizedStr[2];

            if (!gender.equals("-")){
                switch (ops[opIndex]) {
                    case 1:
                        d += expectedDataMap.get(key);
                        if (gender.equals("0")) {
                            n += expectedDataMap.get(key);
                        }
                        break;
                    case 2:
                        if (gender.equals("0")) {
                            d += expectedDataMap.get(key);
                            if (weight.equals("1")) {
                                n += expectedDataMap.get(key);
                            }

                        }
                        break;
                    case 3:
                        if (gender.equals("1")) {
                            d += expectedDataMap.get(key);
                            if (weight.equals("0")) {
                                n += expectedDataMap.get(key);
                            }

                        }
                        break;
                    case 4:
                        if (gender.equals("0")) {
                            d += expectedDataMap.get(key);
                            if (height.equals("0")) {
                                n += expectedDataMap.get(key);
                            }

                        }
                        break;

//                else if(ops[opIndex].equals("TWO")){
                    case 5:
                        if (gender.equals("1")) {
                            d += expectedDataMap.get(key);
                            if (height.equals("0")) {
                                n += expectedDataMap.get(key);
                            }

                        }
                        break;
                }
            }
        }
        
        switch (ops[opIndex]) {
            case 1:
                newParamMap.put(knownData[0] ,(n/d));
                newParamMap.put(knownData[1] ,1 -(n/d));
            case 2:
                newParamMap.put(knownData[2] ,(n/d));
                newParamMap.put(knownData[3] ,1 -(n/d));
            case 3:
                newParamMap.put(knownData[4] ,(n/d));
                newParamMap.put(knownData[5] ,1 -(n/d));
            case 4:
                newParamMap.put(knownData[6] ,(n/d));
                newParamMap.put(knownData[7] ,1 -(n/d));
            case 5:
                newParamMap.put(knownData[8] ,(n/d));
                newParamMap.put(knownData[9] ,1 -(n/d));
        }

        return computeNewParams(expectedDataMap, newParamMap, opIndex);
    }

    void writeToCSV(ArrayList<Double> logLikelihood) {
        String eol = System.getProperty("line.separator");

        try (Writer writer = new FileWriter("graph1.csv")) {
            for (Double elem: logLikelihood) {
                writer.append(Double.toString(elem))
                        .append(',')
                        .append(eol);
            }
        } catch (IOException ex) {
            ex.printStackTrace(System.err);
        }
    }

    public String escapeSpecialCharacters(String data) {
        String escapedData = data.replaceAll("\\R", " ");
        if (data.contains(",") || data.contains("\"") || data.contains("'")) {
            data = data.replace("\"", "\"\"");
            escapedData = "\"" + data + "\"";
        }
        return escapedData;
    }


    public static void main(String[] args) {
        EM em10 = new EM(0.7,0.8,0.4,0.7,
                0.3, new File("hw2dataset_10.txt"), 0.0001);

    }
}