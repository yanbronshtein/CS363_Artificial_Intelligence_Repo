import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.Writer;
import java.util.*;
import java.util.Map.Entry;


/**
 * This class performs the expectation Maximization Algorithm
 */
public class EM {
    /** Stores the number of iterations of the EM alg */
    public int iterations;
    /** threshold specified by the user for convergence of the EM alg */
    final double threshold;
    /* Helper array used for compute newParams  */
    public final int[] ops = {1, 2, 3, 4, 5};
    /**  */
    public final String[] knownData  = {"0,~,~", "1,~,~", "0,0,~", "0,1,~", "1,0,~", "1,1,~", "0,~,0", "0,~,1", "1,~,0", "1,~,1"};
    ArrayList<Double> logLikelihood;
    public HashMap<String, Double> startPriorProbMap;
    public File file;
    public String filenameStr;

    EM(double gender0, double weight0GivenGender0, double weight0GivenGender1, double height0GivenGender0, double height0GivenGender1, File file,
       double threshold, String filenameStr){
        //default constructor for EM class
        logLikelihood = new ArrayList<>();
        this.threshold = threshold;
        this.file = file;
        this.iterations = 0;
        this.filenameStr = filenameStr;

        startPriorProbMap = new HashMap<>();
        startPriorProbMap.put(knownData[0], gender0);
        startPriorProbMap.put(knownData[1], 1-gender0);

        startPriorProbMap.put(knownData[2], weight0GivenGender0);
        startPriorProbMap.put(knownData[3], 1-weight0GivenGender0);

        startPriorProbMap.put(knownData[4], weight0GivenGender1);
        startPriorProbMap.put(knownData[5], 1-weight0GivenGender1);

        startPriorProbMap.put(knownData[6], height0GivenGender0);
        startPriorProbMap.put(knownData[7], 1-height0GivenGender0);

        startPriorProbMap.put(knownData[8], height0GivenGender1);
        startPriorProbMap.put(knownData[9], 1-height0GivenGender1);

        mStep(this.startPriorProbMap, this.file);
    }

    private static HashMap<String, Double> cloneMap(HashMap<String, Double> dataMap) {
        HashMap<String, Double> newMap = new HashMap<>();
        for (Map.Entry<String, Double> entry: dataMap.entrySet()) {
            newMap.put(entry.getKey(), entry.getValue());
        }
        return newMap;

    }

    HashMap<String, Double> eStep(HashMap<String, Double> dataMap, HashMap<String, Double> priorProbMap){
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
                n = priorProbMap.get("0,~,~") * priorProbMap.get("0,1,~") * priorProbMap.get("0,~,1");
                d += priorProbMap.get("0,~,~") * priorProbMap.get("0,1,~") * priorProbMap.get("0,~,1") +
                        priorProbMap.get("1,~,~") * priorProbMap.get("1,1,~") * priorProbMap.get("1,~,1");

                double tempVal = (n/d) * expectedDataMap.get("-,1,1");
                if (expectedDataMap.containsKey("0,1,1")) {
                    expectedDataMap.put("0,1,1", expectedDataMap.get("0,1,1") + tempVal);
                }else {
                    expectedDataMap.put("0,1,1", tempVal);
                }

                double tempVal2 = (1 - (n/d)) * expectedDataMap.get("-,1,1");
                if (expectedDataMap.containsKey("1,1,1")) {

                    expectedDataMap.put("1,1,1", expectedDataMap.get("1,1,1") + tempVal2);
                }else {
                    expectedDataMap.put("1,1,1", tempVal2);
                }

            }

            else if (key.equals(entryOptions[1])){
                double d= 0, n;
                n = priorProbMap.get("0,~,~") * priorProbMap.get("0,1,~") * priorProbMap.get("0,~,0");
                d += priorProbMap.get("0,~,~") * priorProbMap.get("0,1,~") * priorProbMap.get("0,~,0") +
                        priorProbMap.get("1,~,~") * priorProbMap.get("1,1,~") * priorProbMap.get("1,~,0");

                double tempVal = (n/d) * expectedDataMap.get("-,1,0");
                if (expectedDataMap.containsKey("0,1,0")) {
                    expectedDataMap.put("0,1,0", expectedDataMap.get("0,1,0") + tempVal);
                }else {
                    expectedDataMap.put("0,1,0", tempVal);
                }

                double tempVal2 = (1 - (n/d)) * expectedDataMap.get("-,1,0");
                if (expectedDataMap.containsKey("1,1,0")) {

                    expectedDataMap.put("1,1,0", expectedDataMap.get("1,1,0") + tempVal2);
                }else {
                    expectedDataMap.put("1,1,0", tempVal2);
                }

            }
            else if (key.equals(entryOptions[2])){
                double d = 0, n;
                n = priorProbMap.get("0,~,~") * priorProbMap.get("0,0,~") * priorProbMap.get("0,~,0");
                d += priorProbMap.get("0,~,~") * priorProbMap.get("0,0,~") * priorProbMap.get("0,~,0") +
                        priorProbMap.get("1,~,~") * priorProbMap.get("1,0,~") * priorProbMap.get("1,~,0");

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
            else if (key.equals(entryOptions[3])) {
                double d = 0, n;
                n = priorProbMap.get("0,~,~") * priorProbMap.get("0,0,~") * priorProbMap.get("0,~,1");
                d += priorProbMap.get("0,~,~") * priorProbMap.get("0,0,~") * priorProbMap.get("0,~,1") +
                        priorProbMap.get("1,~,~") * priorProbMap.get("1,0,~") * priorProbMap.get("1,~,1");

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
            else {
                continue;
            }
        }
        return expectedDataMap;
    }

    void mStep(HashMap<String, Double> thetaMap, File file){
        HashMap<String, Double> dataMap = ReadFile.parseData(file);
        HashMap<String, Double> expectedData = eStep(dataMap, thetaMap);

        HashMap<String, Double> tempMap = new HashMap<>();
        HashMap<String, Double> newParamMap = calculateNewParameters(expectedData, tempMap, -1);

        this.iterations ++;

        boolean hasConverged = hasConverged(dataMap, thetaMap, newParamMap);

        if (hasConverged){
            System.out.println("Iterations:" + this.iterations);
            printFinalProbabilities(newParamMap);
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
                currProb += currParamMap.get("0,~,~") * currParamMap.get("0,"+weight+",~") *
                        currParamMap.get("0,~,"+height) +
                        currParamMap.get("1,~,~") * currParamMap.get("1,"+weight+",~") *
                        currParamMap.get("1,~,"+height);

                newProb += newParamMap.get("0,~,~") * newParamMap.get("0," + weight +",~") *
                        newParamMap.get("0,~," + height) +
                        newParamMap.get("1,~,~") * newParamMap.get("1," + weight +",~") *
                        newParamMap.get("1,~," + height);

            } else {
                currProb = currParamMap.get(gender + ",~,~") *
                        currParamMap.get(gender + "," + weight +",~") * currParamMap.get(gender + ",~," +height);
                newProb = newParamMap.get(gender + ",~,~") *
                        newParamMap.get(gender + "," + weight +",~") * newParamMap.get(gender + ",~," +height);

            }
            logLikelihoodCurrentParam += Math.log(currProb) * dataMap.get(key);
            logLikelihoodNewParam += Math.log(newProb) * dataMap.get(key);

        }
        if (this.iterations == 1) {
            this.logLikelihood.add(logLikelihoodCurrentParam);
        }
        this.logLikelihood.add(logLikelihoodNewParam);

        double diff = Math.abs(logLikelihoodCurrentParam - logLikelihoodNewParam);


        return diff <= threshold;
    }

    private HashMap<String, Double> calculateNewParameters(HashMap<String, Double> expectedDataMap,
                                                           HashMap<String, Double> newParamMap, int opIndex) {
        double n = 0;
        double d = 0;

        if (opIndex +1 >= ops.length){
            return newParamMap;
        }

        opIndex += 1;



        for(Entry<String, Double> entry : expectedDataMap.entrySet()){
            String key = entry.getKey();
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
                            if (weight.equals("0")) {
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

                    case 5:
                        if (gender.equals("1")) {
                            d += expectedDataMap.get(key);
                            if (height.equals("0")) {
                                n += expectedDataMap.get(key);
                            }

                        }
                        break;
                    default:
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
            default:
                break;
        }

        return calculateNewParameters(expectedDataMap, newParamMap, opIndex);
    }

    void printFinalProbabilities(HashMap<String, Double> finalParamMap) {
        for (Map.Entry<String, Double> entry: finalParamMap.entrySet()) {
            if (entry.getKey().equals(knownData[0])) {
                System.out.println("P(gender=0):" + entry.getValue());
            }
            else if (entry.getKey().equals(knownData[1])) {
                System.out.println("P(gender=1):" + entry.getValue());
            }
            else if (entry.getKey().equals(knownData[2])) {
                System.out.println("P(weight=0 | gender=0):" + entry.getValue());
            }
            else if (entry.getKey().equals(knownData[3])) {
                System.out.println("P(weight=1 | gender=0):" + entry.getValue());
            }
            else if (entry.getKey().equals(knownData[4])) {
                System.out.println("P(weight=0 | gender=1):" + entry.getValue());
            }
            else if (entry.getKey().equals(knownData[5])) {
                System.out.println("P(weight=1 | gender=1):" + entry.getValue());
            }
            else if (entry.getKey().equals(knownData[6])) {
                System.out.println("P(height=0 | gender=0):" + entry.getValue());
            }
            else if (entry.getKey().equals(knownData[7])) {
                System.out.println("P(height=1 | gender=0):" + entry.getValue());
            }
            else if (entry.getKey().equals(knownData[8])) {
                System.out.println("P(height=0 | gender=1):" + entry.getValue());
            }
            else {
                System.out.println("P(height=1 | gender=1):" + entry.getValue());
            }
        }
    }

    void writeToCSV(ArrayList<Double> logLikelihood) {
        String eol = System.getProperty("line.separator");

        try (Writer writer = new FileWriter(this.filenameStr + ".csv")) {
            for (Double elem: logLikelihood) {
                writer.append(Double.toString(elem))
                        .append(',')
                        .append(eol);
            }
        } catch (IOException ex) {
            ex.printStackTrace(System.err);
        }
    }


    public static void main(String[] args) {
        EM em10 = new EM(0.7,0.8,0.4,0.7,
                0.3, new File("hw2dataset_10.txt"), 0.0001, "hw2dataset_10.txt");

        EM em30 = new EM(0.7,0.8,0.4,0.7,
                0.3, new File("hw2dataset_30.txt"), 0.0001, "hw2dataset_30.txt");

        EM em50 = new EM(0.7,0.8,0.4,0.7,
                0.3, new File("hw2dataset_50.txt"), 0.0001, "hw2dataset_50.txt");


        EM em70 = new EM(0.7,0.8,0.4,0.7,
                0.3, new File("hw2dataset_70.txt"), 0.0001, "hw2dataset_70.txt");


        EM em100 = new EM(0.7,0.8,0.4,0.7,
                0.3, new File("hw2dataset_100.txt"), 0.0001, "hw2dataset_100.txt");





    }
}