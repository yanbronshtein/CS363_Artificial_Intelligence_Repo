import java.io.File;
import java.util.*;
import java.util.Map.Entry;

public class EM {

    public int iterations = 0;

    public char[] ops = new char[5];


    EM(double gender0, double weight0GivenGender0, double weight0GivenGender1, double height0GivenGender0, double height0GivenGender1, File filename){
        //default constructor for EM class
        List logLikelihood = new ArrayList();

        String[] knownData = new String[10];
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

        HashMap<String, Double> thetaDict = new HashMap<>();
        thetaDict.put(knownData[0], gender0);
        thetaDict.put(knownData[1], gender0 - 1);

        thetaDict.put(knownData[2], weight0GivenGender0);
        thetaDict.put(knownData[3], weight0GivenGender0 - 1);

        thetaDict.put(knownData[4], weight0GivenGender1);
        thetaDict.put(knownData[5], weight0GivenGender1 - 1);

        thetaDict.put(knownData[6], height0GivenGender0);
        thetaDict.put(knownData[7], height0GivenGender0 - 1);

        thetaDict.put(knownData[8], height0GivenGender1);
        thetaDict.put(knownData[9], height0GivenGender1 - 1);

//        System.out.println(knownValues.get("1,x,1"));

        mStep(thetaDict, filename);
        thetaDict.forEach((key, value) -> System.out.println(key +" : " + value));
//        System.out.println(initialValues[0].toString().equals("0,x,x"));
//        HashMap<String, Integer> dataMap = ReadFile.parseData(filename);
//        HashMap<String, Integer> expectedData = new HashMap(dataMap);    //contains the current frequencies for tuples
//        expectedData.forEach((key, value) -> System.out.println(key +" : " + value));


    }

    static HashMap<String, String> eStep(HashMap<String, Double> dataMap, HashMap<String, Double> thetaDict){
        HashMap<String, Double> expectedDataDict = new HashMap(dataMap);    //contains the current frequencies for tuples

        double d = 0;
        double n = 0;

        final String[] entryOptions = {
                "-,1,1",
                "-,1,0",
                "-,0,0",
                "-,0,1"
        };

        for(Map.Entry<String, Double> entry : dataMap.entrySet()) {
            String key = entry.getKey();
            Double value = entry.getValue();

            if (key.equals(entryOptions[0])){
                n = thetaDict.get("0,x,x") * thetaDict.get("0,1,x") * thetaDict.get("0,x,1");
                d += thetaDict.get("0,x,x") * thetaDict.get("0,1,x") * thetaDict.get("0,x,1");
                d += thetaDict.get("1,x,x") * thetaDict.get("1,1,x") * thetaDict.get("1,x,1");

                double tempVal = (n/d) * expectedDataDict.get("-,1,1");
                if (expectedDataDict.containsKey("0,1,1")) {
                    expectedDataDict.put("0,1,1", expectedDataDict.get("0,1,1") + tempVal);
                }else {
                    expectedDataDict.put("0,1,1", tempVal);
                }

                tempVal = (1 - (n/d)) * expectedDataDict.get("-,1,1");
                if (expectedDataDict.containsKey("1,1,1")) {

                    expectedDataDict.put("1,1,1", expectedDataDict.get("0,1,1") + tempVal);
                }else {
                    expectedDataDict.put("0,1,1", tempVal);
                }

            }

            else if (key.equals(entryOptions[1])){
                n = thetaDict.get("0,x,x") * thetaDict.get("0,1,x") * thetaDict.get("0,x,0");
                d += thetaDict.get("0,x,x") * thetaDict.get("0,1,x") * thetaDict.get("0,x,0");
                d += thetaDict.get("1,x,x") * thetaDict.get("1,1,x") * thetaDict.get("1,x,0");

                double tempVal = (n/d) * expectedDataDict.get("-,1,0");
                if (expectedDataDict.containsKey("0,1,0")) {
                    expectedDataDict.put("0,1,0", expectedDataDict.get("0,1,1") + tempVal);
                }else {
                    expectedDataDict.put("0,1,0", tempVal);
                }

                double tempVal2 = (1 - (n/d)) * expectedDataDict.get("-,1,0");
                if (expectedDataDict.containsKey("1,1,0")) {

                    expectedDataDict.put("1,1,0", expectedDataDict.get("1,1,1") + tempVal2);
                }else {
                    expectedDataDict.put("1,1,0", tempVal2);
                }

            }



            else if (key.equals(entryOptions[2])){
                n = thetaDict.get("0,x,x") * thetaDict.get("0,0,x") * thetaDict.get("0,x,0");
                d += thetaDict.get("0,x,x") * thetaDict.get("0,0,x") * thetaDict.get("0,x,0");
                d += thetaDict.get("1,x,x") * thetaDict.get("1,0,x") * thetaDict.get("1,x,0");

                double tempVal = (n/d) * expectedDataDict.get("-,0,0");
                if (expectedDataDict.containsKey("0,0,0")) {
                    expectedDataDict.put("0,0,0", expectedDataDict.get("0,0,0") + tempVal);
                }else {
                    expectedDataDict.put("0,0,0", tempVal);
                }

                double tempVal2 = (1 - (n/d)) * expectedDataDict.get("-,0,0");
                if (expectedDataDict.containsKey("1,0,0")) {

                    expectedDataDict.put("1,0,0", expectedDataDict.get("1,0,0") + tempVal2);
                }else {
                    expectedDataDict.put("1,0,0", tempVal2);
                }

            }



            else if (key.equals(entryOptions[3])){
                n = thetaDict.get("0,x,x") * thetaDict.get("0,0,x") * thetaDict.get("0,x,1");
                d += thetaDict.get("0,x,x") * thetaDict.get("0,0,x") * thetaDict.get("0,x,1");
                d += thetaDict.get("1,x,x") * thetaDict.get("1,0,x") * thetaDict.get("1,x,1");

                double tempVal = (n/d) * expectedDataDict.get("-,0,1");
                if (expectedDataDict.containsKey("0,0,1")) {
                    expectedDataDict.put("0,0,1", expectedDataDict.get("0,0,1") + tempVal);
                }else {
                    expectedDataDict.put("0,0,1", tempVal);
                }

                double tempVal2 = (1 - (n/d)) * expectedDataDict.get("-,0,1");
                if (expectedDataDict.containsKey("1,0,1")) {

                    expectedDataDict.put("1,0,1", expectedDataDict.get("1,0,1") + tempVal);
                }else {
                    expectedDataDict.put("1,0,1", tempVal);
                }

            }
            else {
                continue;
            }






        }

    }

    void mStep(HashMap knownValues, File filename){
        HashMap dataMap = ReadFile.parseData(filename);
        HashMap expectedData = eStep(dataMap, knownValues);

        int opIndex = -1;

        HashMap newParamMap = computeNewParams(expectedData, opIndex);

        this.iterations += 1;

        boolean hasConverged = hasConverged(dataMap, knownValues, newParamMap);

        if (hasConverged){
            printResults(newParamMap);
        }
        else{
            mStep(newParamMap, filename);
        }

    }

    private void printResults(HashMap newParamMap) {
    }

    private boolean hasConverged(HashMap dataMap, HashMap knownValues, HashMap newParamMap) {
        float logLikelihoodCurrentParam = 0;
        float logLikelihoodNewParam = 0;

        dataMap.forEach((key, value) ->{

        });
    }

    private HashMap computeNewParams(HashMap expectedData, int opIndex) {
        HashMap newParams = null;
        double n = 0;
        double d = 0;

        ops = new char[]{'A', 'B', 'C', 'D', 'E'};


        if (opIndex +1 >= ops.length){
            return  newParams;
        }

        opIndex += 1;


//        expectedData.forEach((key, value) -> {
//            if(key.equals("-")) {
////                break;
//            } else{
//                if(ops[opIndex] == 'A'){
//                    d += expectedData.get(key);
//
//                }
//            }

    });





        while (expectedDataIterator.hasNext()){
        if(expectedData.containsKey("-")){
            continue;
        }
        else{
            if (ops[opIndex] == 'A'){
                d += expectedData(Double.parseDouble(expectedDataIterator.toString()));

            }
        }
    }

}


    public static void main(String[] args) {
        new EM(10,15,19,19,18, new File("hw2dataset_10.txt"));
    }
}