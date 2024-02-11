import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class MRClientJob {
    public static void main(String[] args) throws Exception {
        // Create Configuration and MR Job objects
        Configuration conf = new Configuration();
        //
//        conf.set("yarn.resourcemanager.address", "localhost:8050");
//        conf.set("fs.defaultFS","hdfs://localhost:9000");
        Job job = Job.getInstance(conf, "Join Student and Course");
        //
        job.setJarByClass(MRClientJob.class);

        job.setMapperClass(JoinMap.class);
        job.setReducerClass(JoinReduce.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
