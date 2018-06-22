package com.lge.conn.testnfcwriter;

import android.app.PendingIntent;
import android.content.Intent;
import android.content.IntentFilter;
import android.nfc.FormatException;
import android.nfc.NdefMessage;
import android.nfc.NdefRecord;
import android.nfc.NfcAdapter;
import android.nfc.Tag;
import android.nfc.tech.Ndef;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.widget.Toast;

import java.io.IOException;

public class TagWriteActivity extends AppCompatActivity {
    NfcAdapter nfcAdapter;
    IntentFilter[] filters;
    PendingIntent pIntent;
    String data;
    int type;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_tag_write);

        nfcAdapter = NfcAdapter.getDefaultAdapter(this);
        if (nfcAdapter == null) {
            Toast.makeText(this, "NFC 지원안함", Toast.LENGTH_SHORT);
            finish();
        }
        Intent i = new Intent(this, this.getClass());
        i.setFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP);
        pIntent = PendingIntent.getActivity(this, 0, i, 0);

        data = getIntent().getStringExtra("value");
        type = getIntent().getIntExtra("type", 1);

        Log.i("INFO", "Write NFC Data : data - " + data + ", type - " + type);

        IntentFilter tagFilter = new IntentFilter(NfcAdapter.ACTION_TAG_DISCOVERED);
        filters = new IntentFilter[]{tagFilter};
    }

    @Override
    protected void onResume() {
        super.onResume();

        nfcAdapter.enableForegroundDispatch(this, pIntent, filters, null);
    }

    @Override
    protected void onNewIntent(Intent intent) {
        super.onNewIntent(intent);

        if (!intent.getAction().equals(NfcAdapter.ACTION_NDEF_DISCOVERED) &&
                !intent.getAction().equals(NfcAdapter.ACTION_TECH_DISCOVERED) &&
                !intent.getAction().equals(NfcAdapter.ACTION_TAG_DISCOVERED))
            return;

        Tag detectedTag = intent.getParcelableExtra(NfcAdapter.EXTRA_TAG);
        NdefMessage newMessage = makeNdefMsg(data, type);
        writeMessage(detectedTag, newMessage);
        finish();
        // writeMessage 함수호출
        // Tag 객체 구하고
    }

    @Override
    protected void onPause() {
        super.onPause();
        nfcAdapter.disableForegroundDispatch(this);
    }

    private void writeMessage(Tag detected, NdefMessage msg) {
        Ndef ndef = Ndef.get(detected);
        try {
            ndef.connect();

            if (!ndef.isWritable()) {
                Toast.makeText(this, "쓰기 안됨..", Toast.LENGTH_SHORT).show();
                return;
            }

            int tagSize = ndef.getMaxSize();
            int realData = msg.getByteArrayLength();
            if (realData > tagSize) {
                Toast.makeText(this, "쓰기 용량 초과..", Toast.LENGTH_SHORT).show();
                return;
            }

            Toast.makeText(this, "쓰기 시작..", Toast.LENGTH_SHORT).show();
            ndef.writeNdefMessage(msg);

        } catch (IOException e) {
            e.printStackTrace();
        } catch (FormatException ex) {
        }
    }

    private NdefMessage makeNdefMsg(String data, int type) {

        //NdefRecord record = NdefRecord.createApplicationRecord()
        NdefRecord record = null;
        if (type == 1) {
            record = NdefRecord.createMime("plain/text", data.getBytes());
        }
        else if (type == 2) {
            record = NdefRecord.createUri(data);
        }

        if (record == null)
            return null;

        NdefRecord[] recArr = new NdefRecord[]{record};
        NdefMessage msg = new NdefMessage(recArr);
        return msg;
    }
}
