package com.sdu.invertedindex;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashSet;
import java.util.Set;
import java.util.regex.Pattern;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.filecache.DistributedCache;

public class InvertedIndexMapper extends Mapper<LongWritable, Text, Text, IntWritable> {

    private Set<String> stopWords = new HashSet<String>();
    private Text wordKey = new Text();
    private static final IntWritable one = new IntWritable(1);
    private static final Pattern WORD_PATTERN = Pattern.compile("[^a-zA-Z]");

    @Override
    protected void setup(Context context) throws IOException, InterruptedException {
        Path[] cacheFiles = DistributedCache.getLocalCacheFiles(context.getConfiguration());
        if (cacheFiles != null && cacheFiles.length > 0) {
            String line;
            BufferedReader reader = new BufferedReader(new FileReader(cacheFiles[0].toString()));
            try {
                while ((line = reader.readLine()) != null) {
                    line = line.trim().toLowerCase();
                    if (!line.isEmpty()) {
                        stopWords.add(line);
                    }
                }
            } finally {
                reader.close();
            }
        }
    }

    @Override
    protected void map(LongWritable key, Text value, Context context)
            throws IOException, InterruptedException {
        String fileName = context.getInputSplit().toString();
        fileName = fileName.substring(fileName.lastIndexOf("/") + 1);
        int splitIndex = fileName.indexOf(".txt");
        if (splitIndex != -1) {
            fileName = fileName.substring(0, splitIndex + 4);
        }

        String line = value.toString().toLowerCase();
        String[] tokens = WORD_PATTERN.split(line);

        for (String token : tokens) {
            if (token.isEmpty()) {
                continue;
            }
            if (stopWords.contains(token)) {
                continue;
            }
            if (token.length() < 2) {
                continue;
            }
            wordKey.set(token + "#" + fileName);
            context.write(wordKey, one);
        }
    }
}
