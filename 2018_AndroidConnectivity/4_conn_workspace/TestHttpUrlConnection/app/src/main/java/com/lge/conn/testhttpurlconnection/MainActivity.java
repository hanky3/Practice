package com.lge.conn.testhttpurlconnection;

import android.content.Context;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

public class MainActivity extends AppCompatActivity {
    EditText urlEt;
    TextView resultTv;
    Context context;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        urlEt = findViewById(R.id.urlEt);
        resultTv = findViewById(R.id.resultTv);
        context = this.getApplicationContext();
    }

    public void onDataSearch(View view) {
        String url = urlEt.getText().toString();
        Log.e("INFO", "URL - " + url);

        //Toast.makeText(this, "데이터 조회 start..", Toast.LENGTH_SHORT).show();
        new MyHttpProcessTask().execute(url);
    }

    class MyHttpProcessTask extends AsyncTask<String, String, String> {
        @Override
        protected String doInBackground(String... strings) {
            String url = strings[0];
            StringBuilder sb = new StringBuilder();

            try {
                URL myUrl = new URL(url);
                HttpURLConnection urlConn = (HttpURLConnection)myUrl.openConnection();
                BufferedReader input =new BufferedReader(new InputStreamReader(urlConn.getInputStream(), "utf-8"));

                String msg = input.readLine();
                while ((msg =input.readLine()) != null) {
                    //Log.e("INFO", msg);
                    //publishProgress(msg);
                    sb.append(msg+"\n");
                }
                input.close();
            } catch (MalformedURLException e) {
                e.printStackTrace();
            } catch (IOException ex) {
                ex.printStackTrace();
            }

            return sb.toString();
        }

        @Override
        protected void onProgressUpdate(String... values) {
            super.onProgressUpdate(values);
            //resultTv.append(values[0] + "\n");
        }

        @Override
        protected void onPostExecute(String s) {
            super.onPostExecute(s);
            resultTv.append(s);
            Toast.makeText(context, "데이터 조회 완료..", Toast.LENGTH_SHORT).show();
        }
    };
}
