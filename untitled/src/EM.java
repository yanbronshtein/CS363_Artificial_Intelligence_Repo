import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.Writer;
import java.util.*;
import java.util.Map.Entry;

public class EM {

    public int iterations;
    final double threshold;
    public final int[] ops = {1, 2, 3, 4, 5};
    public String[] knownData  = new String[10];
    ArrayList<Double> logLikelihood;
    public final HashMap<String, Double> startThetaMap;
    public File file;

    EM(double gender0, double weight0GivenGender0, double weight0GivenGender1, double height0GivenGender0, double height0GivenGender1, File file,
       double threshold){
        //default constructor for EM class
        logLikelihood = new ArrayList<>();
        this.threshold = threshold;
        this.file = file;
        this.iterations = 0;
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

        startThetaMap = new HashMap<>();
        startThetaMap.put(knownData[0], gender0);
        startThetaMap.put(knownData[1], 1-gender0);

        startThetaMap.put(knownData[2], weight0GivenGender0);
        startThetaMap.put(knownData[3], 1-weight0GivenGender0);

        startThetaMap.put(knownData[4], weight0GivenGender1);
        startThetaMap.put(knownData[5], 1-weight0GivenGender1);

        startThetaMap.put(knownData[6], height0GivenGender0);
        startThetaMap.put(knownData[7], 1-height0GivenGender0);

        startThetaMap.put(knownData[8], height0GivenGender1);
        startThetaMap.put(knownData[9], 1-height0GivenGender1);

        mStep(this.startThetaMap, this.file);
    }

    private static HashMap<String, Double> cloneMap(HashMap<String, Double> dataMap) {
        HashMap<String, Double> newMap = new HashMap<>();
        for (Map.Entry<String, Double> entry: dataMap.entrySet()) {
            newMap.put(entry.getKey(), entry.getValue());
        }
        return newMap;

    }

    HashMap<String, Double> eStep(HashMap<String, Double> dataMap, HashMap<String, Double> thetaMap){
        HashMap<String, Double> expectedDataMap = cloneMap(dataMap);


        final String[] entryOptions = {
                "-,1,1",
                "-,1,0",
                "-,0,0",
                "-,0,1"
        };

        for(Map.Entry<String, Double> entry : dataMap.entrySet()) {
            String key = entry.getKey();
            if (key.equals(entryOptions[0])){
                double d = 0 ,n;
                n = thetaMap.get("0,x,x") * thetaMap.get("0,1,x") * thetaMap.get("0,x,1");
                d += thetaMap.get("0,x,x") * thetaMap.get("0,1,x") * thetaMap.get("0,x,1");
                d += thetaMap.get("1,x,x") * thetaMap.get("1,1,x") * thetaMap.get("1,x,1");

                double tempVal = (n/d) * expectedDataMap.get("-,1,1");
                if (expectedDataMap.containsKey("0,1,1")) {
                    expectedDataMap.put("0,1,1", expectedDataMap.get("0,1,1") + tempVal);
                }else {
                    expectedDataMap.put("0,1,1", tempVal);
                }

                double tempVal2 = (1 - (n/d)) * expectedDataMap.get("-,1,1");
                if (expectedDataMap.containsKey("1,1,1")) {

                    expectedDataMap.put("1,1,1", expectedDataMap.get("0,1,1") + tempVal2);
                }else {
                    expectedDataMap.put("0,1,1", tempVal2);
                }

            }

            else if (key.equals(entryOptions[1])){
                double d= 0, n;
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
                double d = 0, n;
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
                double d = 0, n;
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

                    expectedDataMap.put("1,0,1", expectedDataMap.get("1,0,1") + tempVal2);
                } else {
                    expectedDataMap.put("1,0,1", tempVal2);
                }

            }
        }
        return expectedDataMap;
    }

    void mStep(HashMap<String, Double> thetaMap, File file){
        HashMap<String, Double> dataMap = ReadFile.parseData(file);
        HashMap<String, Double> expectedData = eStep(dataMap, thetaMap);

        HashMap<String, Double> tempMap = new HashMap<>();
        HashMap<String, Double> newParamMap = computeNewParams(expectedData, tempMap, -1);

        this.iterations ++;

        boolean hasConverged = hasConverged(dataMap, thetaMap, newParamMap);

        if (hasConverged){
            writeToCSV(logLikelihood);
        }
        else{
            mStep(newParamMap, file);
        }

    }



    private boolean hasConverged(HashMap<String, Double> dataMap, HashMap<String, Double> currParamMap,
                                 HashMap<String, Double> newParamMap) {

        double logLikelihoodCurrentParam = 0, logLikelihoodNewParam = 0;

        for (Map.Entry<String, Double> entry: dataMap.entrySet()) {
            String key = entry.getKey();
            String[] tokenizedKeyStr = key.split(",");
            String gender = tokenizedKeyStr[0];
            String weight = tokenizedKeyStr[1];
            String height = tokenizedKeyStr[2];

            double currProb = 0, newProb = 0;

            if (gender.equals("-")) {
                currProb += currParamMap.get("0,x,x") * currParamMap.get("0,"+weight+",x") *
                        currParamMap.get("0,x,"+height);
                currProb += currParamMap.get("1,x,x") * currParamMap.get("0,"+weight+",x") *
                        currParamMap.get("1,x,"+height);

                newProb += newParamMap.get("0,x,x") * newParamMap.get("0," + weight +",x") *
                        newParamMap.get("0,x," + height);

                newProb += newParamMap.get("1,x,x") * newParamMap.get("1," + weight +",x") *
                        newParamMap.get("1,x," + height);

            } else {
                currProb = currParamMap.get(gender + ",x,x") *
                        currParamMap.get(gender + "," + weight +",x") * currParamMap.get(gender + ",x," +height);
                newProb = newParamMap.get(gender + ",x,x") *
                        newParamMap.get(gender + "," + weight +",x") * newParamMap.get(gender + ",x," +height);

            }
            logLikelihoodCurrentParam += Math.log(currProb) * dataMap.get(key);
            logLikelihoodNewParam += Math.log(newProb) * dataMap.get(key);

        }
        if (this.iterations == 1) {
            this.logLikelihood.add(logLikelihoodCurrentParam);
        }
        this.logLikelihood.add(logLikelihoodNewParam);

        double diff = Math.abs(logLikelihoodNewParam - logLikelihoodCurrentParam);

        return diff <= threshold;
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
//            Double value = entry.getValue();
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