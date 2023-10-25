import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.StringTokenizer;

public class JoinReduce extends Reducer<Text, Text, Text, Text> {
    @Override
    protected void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
        String studentRec = "";
        List<String> courseList = new ArrayList();
        String cwid= "";
        //
        for (Text rec : values) {
            StringTokenizer itr = new StringTokenizer(rec.toString());
            cwid = itr.nextToken();
            String fInd = itr.nextToken();
            if (fInd.indexOf("CPSC") == 0) {
                courseList.add(rec.toString());
            } else {
                studentRec = rec.toString();
            }
        }
        //
        for (String c : courseList) {
            String value = studentRec + " " + c;
            context.write(new Text(cwid), new Text(value));
        }
    }
}
