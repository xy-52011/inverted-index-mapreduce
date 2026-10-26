package com.sdu.invertedindex;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class InvertedIndexReducer extends Reducer<Text, IntWritable, Text, Text> {

    private Text currentWord = new Text();
    private List<String> postingList = new ArrayList<String>();
    private int totalCount = 0;

    @Override
    protected void reduce(Text key, Iterable<IntWritable> values, Context context)
            throws IOException, InterruptedException {
        String[] parts = key.toString().split("#");
        if (parts.length != 2) {
            return;
        }
        String word = parts[0];
        String fileName = parts[1];

        if (currentWord.getLength() == 0) {
            currentWord.set(word);
        }

        if (!word.equals(currentWord.toString())) {
            emitResult(context);
            currentWord.set(word);
            postingList.clear();
            totalCount = 0;
        }

        int count = 0;
        for (IntWritable val : values) {
            count += val.get();
        }
        postingList.add("<" + fileName + "," + count + ">");
        totalCount += count;
    }

    @Override
    protected void cleanup(Context context) throws IOException, InterruptedException {
        if (currentWord.getLength() > 0) {
            emitResult(context);
        }
    }

    private void emitResult(Context context) throws IOException, InterruptedException {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < postingList.size(); i++) {
            if (i > 0) {
                sb.append(";");
            }
            sb.append(postingList.get(i));
        }
        sb.append(";<total,").append(totalCount).append(">.");
        context.write(currentWord, new Text(sb.toString()));
    }
}
