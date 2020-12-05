public class DataSetObj {
    String gender;
    String weight;
    String height;
    String tupleStr;

    public String getGender() {
        return gender;
    }

    public String getWeight() {
        return weight;
    }

    public String getHeight() {
        return height;
    }

    public String getTupleStr() {
        return tupleStr;
    }

    public DataSetObj(String gender, String weight, String height) {
        this.tupleStr = gender + "," + weight + "," + height;
        this.gender = gender;
        this.weight = weight;
        this.height = height;
    }

    @Override
    public String toString() {
        return this.tupleStr;
    }

    //setter
//    public void DataSetObj(String gender, String weight, String height) {
//        this.gender = gender;
//        this.height = height;
//        this.weight = weight;
//        this.tupleStr = gender + " ," + weight + " ," + height;
//    }
    /**
     * Indicates whether some other object is "equal to" this one.
     *
     * @return true if objects are equal, false otherwise.
     */

    public boolean equals (DataSetObj b){
        if(b == null || b.getClass()!= this.getClass())
            return false;
        else if (this.gender == this.gender && this.height == b.height && this.weight == b.height)
            return true;
        return false;
    }


/**
 * Returns a hash code value for the object. This function is overriden
 * for the hash tables in my program to provide a unique hash code.
 *
 * @return integer hash code value
 */
//
//    @Override
//    public int hashCode(){
//
//    }





    /**
     * This function is used to compare HashMap Key's.
     *
     * @param gender: value of Gender
     * @param weight: value of Weight
     * @param height: value of Height
     * @return true if it is equal, false otherwise.
     */
}