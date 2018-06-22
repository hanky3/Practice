package com.lge.conn.testnfcwriter;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;

public class MainActivity extends AppCompatActivity {
    EditText textEt;
    EditText urlEt;

    public final static int TEXT_MODE = 1;
    public final static int URL_MODE = 2;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        textEt = this.findViewById(R.id.textEt);
        urlEt = this.findViewById(R.id.urlEt);
    }

    public void writeTextData(View view) {
        String data = textEt.getText().toString();
        Intent intent = new Intent(this, TagWriteActivity.class);
        intent.putExtra("value", data);
        intent.putExtra("type", TEXT_MODE);
        startActivity(intent);
    }

    public void writeLinkData(View view) {
        String urlData = urlEt.getText().toString();
        Intent intent = new Intent(this, TagWriteActivity.class);
        intent.putExtra("value", urlData);
        intent.putExtra("type", URL_MODE);
        startActivity(intent);
    }
}
