package com.lge.conn.testnfcreader;

import android.content.Intent;
import android.net.Uri;
import android.nfc.NdefMessage;
import android.nfc.NdefRecord;
import android.nfc.NfcAdapter;
import android.os.Parcelable;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

import java.net.URI;

public class MainActivity extends AppCompatActivity {
    TextView infoTv;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        infoTv = findViewById(R.id.infoTv);
        Intent intent = getIntent();
        processIntent(intent);
//        String action = intent.getAction();
//
//        infoTv.setText("수신 Action : " + action);
    }

    private void processIntent(Intent intent) {
        if (!intent.getAction().equals(NfcAdapter.ACTION_NDEF_DISCOVERED))
            return;

        Parcelable[] rawData = intent.getParcelableArrayExtra(NfcAdapter.EXTRA_NDEF_MESSAGES);
        // 1. NdefMessage
        NdefMessage ndefMsg = (NdefMessage) rawData[0];
        // 2. NdefRecord
        NdefRecord[] recArr = ndefMsg.getRecords();

        //String type = intent.getType();
        String dataType = new String(recArr[0].getType());
        if (dataType.equals("T")) {

            byte[] realData = recArr[0].getPayload();
            String strData = new String(realData, 3,  realData.length-3);
            //String typeStr = new String(type);
            infoTv.setText("Tag Data : " + strData + ", ");
        }
        else if (dataType.equals("U")) {
            Uri myUri = recArr[0].toUri();
            infoTv.setText("Uri Data : " + myUri.toString());
            Intent i2 = new Intent(Intent.ACTION_VIEW, myUri);
            startActivity(i2);
        }
        else {
            // unknown type
        }
    }
}
