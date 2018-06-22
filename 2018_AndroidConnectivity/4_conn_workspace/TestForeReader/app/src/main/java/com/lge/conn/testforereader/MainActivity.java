package com.lge.conn.testforereader;

import android.app.PendingIntent;
import android.net.Uri;
import android.nfc.NdefMessage;
import android.nfc.NdefRecord;
import android.nfc.NfcAdapter;
import android.nfc.tech.NfcA;
import android.os.Parcelable;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.content.*;
import android.util.Log;
import android.widget.TextView;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {
    NfcAdapter nfcAdapter;
    IntentFilter[] filters;
    PendingIntent pIntent;
    TextView infoTv;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        infoTv = findViewById(R.id.infoTv);
        nfcAdapter = NfcAdapter.getDefaultAdapter(this);
        if (nfcAdapter == null) {
            Toast.makeText(this, "NFC 지원안함", Toast.LENGTH_SHORT);
            finish();
        }

        Intent i = new Intent(this, this.getClass());
        i.setFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP);
        pIntent = PendingIntent.getActivity(this, 0, i, 0);

/*
        IntentFilter ndefF = new IntentFilter(NfcAdapter.ACTION_NDEF_DISCOVERED);
        try {
            ndefF.addDataType("text/plain");
        } catch (IntentFilter.MalformedMimeTypeException e) {
            e.printStackTrace();
        }

        IntentFilter ndefF_http = new IntentFilter(NfcAdapter.ACTION_NDEF_DISCOVERED);
        ndefF_http.addDataScheme("http");
        IntentFilter ndefF_https = new IntentFilter(NfcAdapter.ACTION_NDEF_DISCOVERED);
        ndefF_https.addDataScheme("https");
*/
        IntentFilter tagFilter = new IntentFilter(NfcAdapter.ACTION_TAG_DISCOVERED);

        filters = new IntentFilter[]{tagFilter};

}

    protected void onResume() {
        super.onResume();
        nfcAdapter.enableForegroundDispatch(this, pIntent, filters, null);
    }

    protected void onPause() {
        super.onPause();
        nfcAdapter.disableForegroundDispatch(this);
    }

    @Override
    protected void onNewIntent(Intent intent) {
        super.onNewIntent(intent);
        Log.i("INFO", "onNewIntent call...");
        processIntent(intent);
    }

    private void processIntent(Intent intent) {
        if (!intent.getAction().equals(NfcAdapter.ACTION_NDEF_DISCOVERED) &&
                !intent.getAction().equals(NfcAdapter.ACTION_TECH_DISCOVERED) &&
                !intent.getAction().equals(NfcAdapter.ACTION_TAG_DISCOVERED))
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
            //Intent i2 = new Intent(Intent.ACTION_VIEW, myUri);
            //startActivity(i2);
        }
        else {
            // unknown type
        }
    }

    private NdefMessage makeNdefMsg(String data, String pkg) {
        NdefRecord uriRec = NdefRecord.createUri(data);
        NdefRecord aarRec = NdefRecord.createApplicationRecord(pkg);
        NdefRecord[] recArr = new NdefRecord[]{uriRec, aarRec};
        NdefMessage ndefMsg = new NdefMessage(recArr);
        return ndefMsg;
    }
}
