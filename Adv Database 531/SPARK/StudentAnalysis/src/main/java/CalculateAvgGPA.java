import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaPairRDD;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.api.java.function.Function;
import org.apache.spark.api.java.function.Function2;
import org.apache.spark.api.java.function.PairFunction;
import scala.Tuple2;

public class CalculateAvgGPA {
    public static void main(String[] args) {
        SparkConf sparkConf = new SparkConf()
                .setAppName("Example Spark App")
                .setMaster("local[10]");
        JavaSparkContext sparkContext = new JavaSparkContext(sparkConf);

        System.out.println("The default parallelism: " + sparkContext.defaultParallelism());

        // Loading the Student & Course datasets
        JavaRDD<String> studentRDD = sparkContext.textFile(args[0], 4);
        JavaRDD<String> courseRDD = sparkContext.textFile(args[1], 4);

        JavaRDD<String> femaleStudentRDD = studentRDD.filter(
                new Function<String, Boolean>() {
                    public Boolean call(String s) throws Exception {
                        String gender = s.split(" ")[3];
                        return gender.equalsIgnoreCase("female");
                    }
                }
        );

        JavaRDD<String> partialStudentRDD = studentRDD.map(
                new Function<String, String>() {
                    public String call(String s) throws Exception {
                        String cwid = s.split(" ")[0];
                        String fn = s.split(" ")[1];
                        String ln = s.split(" ")[2];
                        return cwid + " " + ln + ", " + fn;
                    }
                }
        );

        JavaPairRDD<String, String> femaleStudentPairRDD = femaleStudentRDD.mapToPair(
                new PairFunction<String, String, String>() {
                    public Tuple2<String, String> call(String s) throws Exception {
                        String cwid = s.split(" ")[0];
                        return new Tuple2(cwid, s);
                    }
                }
        );

        JavaPairRDD<String, String> coursePairRDD = courseRDD.mapToPair(
                new PairFunction<String, String, String>() {
                    public Tuple2<String, String> call(String s) throws Exception {
                        String cwid = s.split(" ")[0];
                        return new Tuple2(cwid, s);
                    }
                }
        );

        JavaPairRDD<String, Tuple2<String, String>> joinPairRDD = femaleStudentPairRDD.join(coursePairRDD, 6);

        JavaRDD<Tuple2<String, Tuple2<Float, Integer>>> eachGpaCntRdd = joinPairRDD.map(
                new Function<Tuple2<String, Tuple2<String, String>>, Tuple2<String, Tuple2<Float, Integer>>>() {
                    public Tuple2<String, Tuple2<Float, Integer>> call(Tuple2<String, Tuple2<String, String>> stringTuple2Tuple2) throws Exception {
                        String cwid = stringTuple2Tuple2._1;
                        String gpa = stringTuple2Tuple2._2._2.split(" ")[2];
                        return new Tuple2(cwid, new Tuple2(new Float(gpa), 1));
                    }
                }
        );

        JavaPairRDD<String, Tuple2<Float, Integer>> eachGpaCntPairRDD = eachGpaCntRdd.mapToPair(
                new PairFunction<Tuple2<String, Tuple2<Float, Integer>>, String, Tuple2<Float, Integer>>() {
                    public Tuple2<String, Tuple2<Float, Integer>> call(Tuple2<String, Tuple2<Float, Integer>> stringTuple2Tuple2) throws Exception {
                        return new Tuple2(stringTuple2Tuple2._1, stringTuple2Tuple2._2);
                    }
                }
        );

        JavaPairRDD<String, Tuple2<Float, Integer>> sumGpaCntPairRDD = eachGpaCntPairRDD.reduceByKey(
                new Function2<Tuple2<Float, Integer>, Tuple2<Float, Integer>, Tuple2<Float, Integer>>() {
                    public Tuple2<Float, Integer> call(Tuple2<Float, Integer> floatIntegerTuple2, Tuple2<Float, Integer> floatIntegerTuple22) throws Exception {
                        Float sumGpa = floatIntegerTuple2._1 + floatIntegerTuple22._1;
                        Integer cnt = floatIntegerTuple2._2 + floatIntegerTuple22._2;
                        return new Tuple2(sumGpa, cnt);
                    }
                }
        );

        JavaPairRDD<Tuple2<String, Integer>, String> genderLevelStudentPairRDD = studentRDD.mapToPair(
                new PairFunction<String, Tuple2<String, Integer>, String>() {
                    public Tuple2<Tuple2<String, Integer>, String> call(String s) throws Exception {
                        String gender = s.split(" ")[3];
                        Integer level = new Integer(s.split(" ")[4]);
                        return new Tuple2(new Tuple2(gender, level), s);
                    }
                }
        );

        JavaPairRDD<Tuple2<String, Integer>, String> sortedStudentPairRDD = genderLevelStudentPairRDD.sortByKey(new GenderLevelComparator());

        // studentRDD.saveAsTextFile(args[2]);
        femaleStudentRDD.saveAsTextFile(args[2]);
        partialStudentRDD.saveAsTextFile(args[3]);
        joinPairRDD.saveAsTextFile(args[4]);
        eachGpaCntRdd.saveAsTextFile(args[5]);
        sumGpaCntPairRDD.saveAsTextFile(args[6]);
        sortedStudentPairRDD.saveAsTextFile(args[7]);
    }
}
