package edu.jaen.nfc.writer;

import android.app.Activity;
import android.app.AlertDialog;
import android.app.PendingIntent;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.IntentFilter.MalformedMimeTypeException;
import android.nfc.NdefMessage;
import android.nfc.NdefRecord;
import android.nfc.NfcAdapter;
import android.nfc.Tag;
import android.nfc.tech.Ndef;
import android.nfc.tech.NdefFormatable;
import android.os.Bundle;
import android.os.Parcelable;
import android.text.Editable;
import android.text.TextWatcher;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

import java.io.IOException;

public class WriteTagActivity extends Activity {

	private static final String TAG = "WriteTagActivity";
	private boolean mWriteMode = false;
	NfcAdapter mNfcAdapter;
	EditText etMsg;

	PendingIntent pIntent;
	IntentFilter[] mNdefFilters;

	/** Called when the activity is first created. */
	@Override
	public void onCreate(Bundle savedInstanceState) {

		super.onCreate(savedInstanceState);
		mNfcAdapter = NfcAdapter.getDefaultAdapter(this);

		setContentView(R.layout.main);

		findViewById(R.id.write_tag).setOnClickListener(
				new View.OnClickListener() {
					@Override
					public void onClick(View view) {
						mWriteMode = true;
						new AlertDialog.Builder(WriteTagActivity.this)
								.setTitle("Touch tag to write")
								.setOnCancelListener(
										new DialogInterface.OnCancelListener() {
											@Override
											public void onCancel(
													DialogInterface dialog) {
												mWriteMode = false;
												
											}
										}).create().show();
					}
				});

		// EditText 가져오기
		etMsg = ((EditText) findViewById(R.id.note));
		
		// Handle all of our received NFC intents in this activity.
		pIntent = PendingIntent.getActivity(this, 0, new Intent(this,
				getClass()).addFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP), 0);

		// Intent filters for reading a note from a tag or exchanging over p2p.
		IntentFilter ndefFilter = new IntentFilter(
				NfcAdapter.ACTION_NDEF_DISCOVERED);
		try {
			ndefFilter.addDataType("text/plain");
		} catch (MalformedMimeTypeException e) {
			e.printStackTrace();
		}
		mNdefFilters = new IntentFilter[] { ndefFilter };
	}

	@Override
	protected void onResume() {
		super.onResume();
		
		mNfcAdapter.enableForegroundDispatch(this, pIntent, mNdefFilters, null);
		
		if (NfcAdapter.ACTION_NDEF_DISCOVERED.equals(getIntent().getAction())) {
			NdefMessage[] messages = getNdefMessages(getIntent());
			byte[] payload = messages[0].getRecords()[0].getPayload();
			etMsg.append("\n"+new String(payload));
			setIntent(new Intent()); // Consume this intent.
		}
	}
	
	@Override
	protected void onPause() {
		// TODO Auto-generated method stub
		super.onPause();
		mNfcAdapter.disableForegroundDispatch(this);
	}

	@Override
	protected void onNewIntent(Intent intent) {
		// NDEF exchange mode
		if(mWriteMode && NfcAdapter.ACTION_NDEF_DISCOVERED.equals(intent.getAction())){
			Tag detectedTag = intent.getParcelableExtra(NfcAdapter.EXTRA_TAG);
			writeTag(makeNdefMessage(), detectedTag);
		} else if (!mWriteMode && NfcAdapter.ACTION_NDEF_DISCOVERED.equals(intent.getAction())) {
			NdefMessage[] msgs = getNdefMessages(intent);
			promptForContent(msgs[0]);
		} 
	}

	private void promptForContent(final NdefMessage msg) {
		new AlertDialog.Builder(this)
				.setTitle("새로운 Tag가 인식되었습니다.\n 읽으시겠습니까?")
				.setPositiveButton("Yes",
						new DialogInterface.OnClickListener() {
							@Override
							public void onClick(DialogInterface arg0, int arg1) {
								String body = new String(msg.getRecords()[0]
										.getPayload());
								etMsg.setText(body);

							}
						})
				.setNegativeButton("No", new DialogInterface.OnClickListener() {
					@Override
					public void onClick(DialogInterface arg0, int arg1) {

					}
				}).show();
	}

	private NdefMessage makeNdefMessage() {
		
		byte[] textBytes = etMsg.getText().toString().getBytes();
		NdefRecord textRecord = new NdefRecord(NdefRecord.TNF_MIME_MEDIA,
				"text/plain".getBytes(), new byte[] {}, textBytes);
		
		return new NdefMessage(new NdefRecord[] { textRecord });
	}

	private NdefMessage[] getNdefMessages(Intent intent) {
		// Parse the intent
		NdefMessage[] msgs = null;
		String action = intent.getAction();
		if (NfcAdapter.ACTION_NDEF_DISCOVERED.equals(action)) {
			Parcelable[] rawMsgs = intent
					.getParcelableArrayExtra(NfcAdapter.EXTRA_NDEF_MESSAGES);
			if (rawMsgs != null) {
				msgs = new NdefMessage[rawMsgs.length];
				for (int i = 0; i < rawMsgs.length; i++) {
					msgs[i] = (NdefMessage) rawMsgs[i];
				}
			} else {
				// Unknown tag type
				byte[] empty = new byte[] {};
				NdefRecord record = new NdefRecord(NdefRecord.TNF_UNKNOWN,
						empty, empty, empty);
				NdefMessage msg = new NdefMessage(new NdefRecord[] { record });
				msgs = new NdefMessage[] { msg };
			}
		} else {
			Log.d(TAG, "Unknown intent.");
			finish();
		}
		return msgs;
	}

	boolean writeTag(NdefMessage message, Tag tag) {

		int size = message.toByteArray().length;

		try {
			Ndef ndef = Ndef.get(tag);

			if (ndef != null) {

				ndef.connect();

				if (!ndef.isWritable()) {
					toast("Tag is read-only.");
					return false;
				}
				if (ndef.getMaxSize() < size) {
					toast("Tag capacity is " + ndef.getMaxSize()
							+ " bytes, message is " + size + " bytes.");
					return false;
				}

				ndef.writeNdefMessage(message);
				toast("Wrote message to pre-formatted tag.");

				// Ndef 객체의 makeReadOnly()를 사용하면 overwrite 안되게 설정이 가능하다.

				return true;
			} else {
				toast("Tag doesn't support NDEF.");
			}
		} catch (Exception e) {
			toast("Failed to write tag");
		}
		return false;
	}

	private void toast(String text) {
		Toast.makeText(this, text, Toast.LENGTH_SHORT).show();
	}
}