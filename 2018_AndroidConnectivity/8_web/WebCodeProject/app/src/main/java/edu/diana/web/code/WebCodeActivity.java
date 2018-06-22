package edu.diana.web.code;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import android.app.Activity;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

public class WebCodeActivity extends Activity {
	TextView tv;

	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.main);
		tv = (TextView) findViewById(R.id.write);
		final EditText et = (EditText) findViewById(R.id.uri);
		Button b = (Button) findViewById(R.id.web);
		
		//test code
		et.setText("http://www.naver.com");

		b.setOnClickListener(new View.OnClickListener() {

			@Override
			public void onClick(View v) {
				
				String uri = et.getText().toString();
				Toast.makeText(WebCodeActivity.this, uri, 1).show();
				uri = (uri.startsWith("http://")) ? uri
						: "http://10.0.2.2:8080/" + uri;
				
				
				new ConnectTask().execute(uri);
			}
		});
	}

	class ConnectTask extends AsyncTask<String, String, String> {

		protected String doInBackground(String... arg) {
			HttpURLConnection con = null;
			;
			BufferedReader br = null;
			try {
				con = (HttpURLConnection) new URL(arg[0]).openConnection();
				br = new BufferedReader(new InputStreamReader(
						con.getInputStream()));
				String s = br.readLine();
				do {
					publishProgress("\n" + s);
					s = br.readLine();
				} while (s != null);
			} catch (MalformedURLException e) {
				e.printStackTrace();
			} catch (IOException e) {
				e.printStackTrace();
			} finally {
				try {
					if (br != null)
						br.close();
					if (con != null)
						con.disconnect();
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
			return null;
		}

		@Override
		protected void onProgressUpdate(String... values) {
			tv.append(values[0]);
			super.onProgressUpdate(values);
		}
	}
}