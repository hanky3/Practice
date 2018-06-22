package com.androidjava.app8.webintent;


import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.view.KeyEvent;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.View.OnKeyListener;
import android.widget.Button;
import android.widget.EditText;

	public class MyWebIntent extends Activity {
	   private EditText urlText;
	   private Button goButton;

	   @Override
	   public void onCreate(Bundle savedInstanceState) {
	      super.onCreate(savedInstanceState);
	      setContentView(R.layout.main); 

	      urlText = (EditText) findViewById(R.id.urlText); 
	      goButton = (Button) findViewById(R.id.goBtn);

	      goButton.setOnClickListener(new OnClickListener() { 
	         public void onClick(View view) {
	            openBrowser();
	         }
	      });
	      urlText.setOnKeyListener(new OnKeyListener() { 
	         public boolean onKey(View view, int keyCode, KeyEvent event) {
	            if (keyCode == KeyEvent.KEYCODE_ENTER) {
	               openBrowser();
	               return true;
	            }
	            return false;
	         }
	      });
	   }
	   

	   private void openBrowser() {
	      Uri uri = Uri.parse(urlText.getText().toString());
	      Intent intent = new Intent(Intent.ACTION_VIEW, uri);
	      startActivity(intent);
	   }
	   
	   
	}
