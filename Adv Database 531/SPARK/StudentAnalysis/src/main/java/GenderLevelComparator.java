import scala.Tuple2;

import java.io.Serializable;
import java.util.Comparator;

public class GenderLevelComparator implements Comparator<Tuple2<String, Integer>>, Serializable {
    public int compare(Tuple2<String, Integer> o1, Tuple2<String, Integer> o2) {
        if (o1._1.equalsIgnoreCase("male")) {
            if (o2._1.equalsIgnoreCase("female")) return 1;
            else return o1._2.compareTo(o2._2);
        } else {
            if (o2._1.equalsIgnoreCase("male")) return -1;
            else return o1._2.compareTo(o2._2);
        }
    }
}
