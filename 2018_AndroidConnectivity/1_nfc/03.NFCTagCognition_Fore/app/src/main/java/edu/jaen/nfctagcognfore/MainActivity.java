package edu.jaen.nfctagcognfore;

import android.app.Activity;
import android.app.PendingIntent;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.IntentFilter.MalformedMimeTypeException;
import android.nfc.NdefMessage;
import android.nfc.NdefRecord;
import android.nfc.NfcAdapter;
import android.os.Bundle;
import android.os.Parcelable;
import android.widget.TextView;
import android.widget.Toast;

public class MainActivity extends Activity {
	TextView tv;
	NfcAdapter nAdapter;
	PendingIntent pIntent;
	IntentFilter[] filters;
	@Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        tv = new TextView(this);
        String action = getIntent().getAction();
        tv.setText(action);
        setContentView(tv);
        Toast.makeText(this, "onCreate", Toast.LENGTH_SHORT).show();
        
        nAdapter = NfcAdapter.getDefaultAdapter(this);
        
        Intent i = new Intent(this, MainActivity.class);
        i.setFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP);
        pIntent = PendingIntent.getActivity(this, 0, i, 0);
        
        IntentFilter filter = new IntentFilter(NfcAdapter.ACTION_NDEF_DISCOVERED);
        
        try {
        	filter.addDataType("*/*");
        } catch (MalformedMimeTypeException e) {
        	e.printStackTrace();
        	throw new RuntimeException("fail", e);
        }
        filters = new IntentFilter[] { filter, };
	}
	
	@Override
	protected void onResume() {
		// TODO Auto-generated method stub
		super.onResume();
		nAdapter.enableForegroundDispatch(this, pIntent, filters, null);
	}
	
	@Override
	protected void onPause() {
		// TODO Auto-generated method stub
		super.onPause();
		nAdapter.disableForegroundDispatch(this);
	}
	
	@Override
	protected void onNewIntent(Intent intent) {
		// TODO Auto-generated method stub
		super.onNewIntent(intent);
		String action = intent.getAction();
		//tv.setText("New Intent action : "+action);
		parseData(intent);
        
	}
	
	private void parseData(Intent intent){
		Parcelable[] data = intent.getParcelableArrayExtra(NfcAdapter.EXTRA_NDEF_MESSAGES);
		NdefMessage ndefM = (NdefMessage) data[0];
		NdefRecord ndefR = ndefM.getRecords()[0];
		byte[] byteArr = ndefR.getPayload();
		
		//String textData = new String(byteArr, 3, byteArr.length-3);
		tv.setText("nfc tag data : " +new String(byteArr));
		
	}

}
