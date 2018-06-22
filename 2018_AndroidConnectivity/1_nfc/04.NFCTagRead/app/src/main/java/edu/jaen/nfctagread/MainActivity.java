package edu.jaen.nfctagread;

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
        setContentView(tv);
        
        nAdapter = NfcAdapter.getDefaultAdapter(this);
        
        getNFCData(getIntent());
	}
	
	private void getNFCData(Intent intent) {
		// TODO Auto-generated method stub
		//System.out.println(getIntent().getAction());
		Toast.makeText(this, "수신 액션 : "+getIntent().getAction(), Toast.LENGTH_SHORT).show();
		if (NfcAdapter.ACTION_NDEF_DISCOVERED.equals(getIntent().getAction())) {
			Parcelable[] rawMsgs = intent
					.getParcelableArrayExtra(NfcAdapter.EXTRA_NDEF_MESSAGES);
			
			if (rawMsgs != null) {
				NdefMessage[] messages = new NdefMessage[rawMsgs.length];
				for (int i = 0; i < rawMsgs.length; i++) {
					messages[i] = (NdefMessage) rawMsgs[i];
				}
				byte[] payload = messages[0].getRecords()[0].getPayload();
				
				//test
//				System.out.println("id : " + new String(messages[0].getRecords()[0].getId()));
//				System.out.println("type : " + new String(messages[0].getRecords()[0].getType()));
//				System.out.println("getTnf : " + messages[0].getRecords()[0].getTnf());
				
				
				tv.append("\n"+new String(payload));
			}
		}
	}

	@Override
	protected void onResume() {
		// TODO Auto-generated method stub
		super.onResume();
		
		Intent i = new Intent(this, MainActivity.class);
		i.setFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP);
		pIntent = PendingIntent.getActivity(this, 0, i, 0);

		IntentFilter filter = new IntentFilter(NfcAdapter.ACTION_NDEF_DISCOVERED);
		filter.addAction(NfcAdapter.ACTION_TECH_DISCOVERED);
		filter.addAction(NfcAdapter.ACTION_TAG_DISCOVERED);
		

		try {
			filter.addDataType("*/*");
		} catch (MalformedMimeTypeException e) {
			e.printStackTrace();
			throw new RuntimeException("fail", e);
		}

		filters = new IntentFilter[] { filter };
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
		setIntent(intent);
		getNFCData(getIntent());
	}
}
