import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.*;
import org.apache.hadoop.hdfs.client.HdfsDataInputStream;
import org.apache.hadoop.hdfs.protocol.Block;
import org.apache.hadoop.hdfs.protocol.ExtendedBlock;
import org.apache.hadoop.hdfs.protocol.LocatedBlock;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.URI;
import java.util.List;

public class FileLevelAPI {

    public void createFile(String fileName) throws Exception {
        Configuration conf = new Configuration();
        FileSystem fs = FileSystem.get(conf);
        FSDataOutputStream out = fs.create(new Path(fileName));
        BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(out));
        //
        for (int i = 0; i < 20; i++) {
            bw.write("File Record " + i);
            bw.newLine();
        }
        bw.close();

    }

    public void readFile(String fileName) throws Exception {
        Configuration conf = new Configuration();
        FileSystem fs = FileSystem.get(conf);
        Path path = new Path(fileName);
        FileStatus fStatus = fs.getFileStatus(path);
        if (!fStatus.isDirectory()) {
            FSDataInputStream in = fs.open(path);
            InputStreamReader reader = new InputStreamReader(in);
            BufferedReader br = new BufferedReader(reader);
            String line = null;
            while ((line = br.readLine()) != null) {
                System.out.println(line);
            }
            // get block locations
            BlockLocation[] bLocations = fs.getFileBlockLocations(path, 0, 1000);
            for (BlockLocation bl : bLocations) {
                System.out.println("Name of Block(0)" + bl.getNames()[0]);
                System.out.println("Host of Block(0)" + bl.getHosts()[0]);
                System.out.println("Block Offset: " + bl.getOffset());
                System.out.println("Lenth of Data: " + bl.getLength());
            }
        } else {
            System.out.println("This is a directory.");
            FileStatus[] fStatuses = fs.listStatus(path);
        }
        //
        System.out.println("++++++++++++++++++");
        System.out.println("File Name: " + fStatus.getPath());
        System.out.println("File Block Size: " + fStatus.getBlockSize());
        System.out.println("File Size: " + fStatus.getLen());
        System.out.println("File Replication Factor: " + fStatus.getReplication());
        System.out.println("File Owner: " + fStatus.getOwner());
    }

    public void remoteReadFile(String fileName) throws Exception {
        Configuration conf = new Configuration();
        URI hostURI = URI.create(fileName);
        FileSystem fs = FileSystem.get(hostURI, conf);
        Path path = new Path(fileName);
        FSDataInputStream in = fs.open(path);
        InputStreamReader reader = new InputStreamReader(in);
        BufferedReader br = new BufferedReader(reader);
        String line = null;
        while ((line = br.readLine()) != null) {
            System.out.println(line);
        }
        //
        HdfsDataInputStream hdis = (HdfsDataInputStream) fs.open(path);
        List<LocatedBlock> lblocks = hdis.getAllBlocks();
        System.out.println("The number of blocks in the file: " + lblocks.size());
        for (LocatedBlock lblk : lblocks) {
            System.out.println("The Start Offset: " + lblk.getStartOffset());
            System.out.println("The Block Size: " + lblk.getBlockSize());
            System.out.println("The Block Type: " + lblk.getBlockType());
            System.out.println("The Block Token: " + lblk.getBlockToken());
            System.out.println("The Datanode Name: " + lblk.getLocations()[0].getHostName());
            ExtendedBlock eb = lblk.getBlock();
            System.out.println("The Block Name: " + eb.getBlockName());
            System.out.println("The Block Pool ID: " + eb.getBlockPoolId());
            System.out.println("The Block ID: " + eb.getBlockId());
            Block lb = eb.getLocalBlock();
            System.out.println("Number of Bytes: " + lb.getNumBytes());
        }
    }

    public static void main(String[] args) throws Exception {
        //new FileLevelAPI().createFile(args[0]);
        //new FileLevelAPI().readFile(args[0]);
        new FileLevelAPI().remoteReadFile(args[0]);
    }
}
