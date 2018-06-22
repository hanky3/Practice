package edu.jaen.android.nfc.enablenfc;

import android.nfc.NfcAdapter;
import android.os.Bundle;
import android.provider.Settings;
import android.app.Activity;
import android.content.Intent;
import android.view.Menu;
import android.view.View;
import android.view.View.OnClickListener;

public class MainActivity extends Activity implements OnClickListener {

	NfcAdapter nfcAdapter;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		findViewById(R.id.enNfcBut).setOnClickListener(this);
		findViewById(R.id.enBeamBut).setOnClickListener(this);

		nfcAdapter = NfcAdapter.getDefaultAdapter(this);

	}

	@Override
	public void onClick(View v) {
		switch (v.getId()) {
		case R.id.enNfcBut:
			startActivity(new Intent(Settings.ACTION_NFC_SETTINGS));
			break;
		case R.id.enBeamBut:
			startActivity(new Intent(Settings.ACTION_NFCSHARING_SETTINGS));
			break;

		default:
			break;
		}

	}

}
